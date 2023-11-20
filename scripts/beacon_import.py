from pymongo import MongoClient
from requests import Response
from bioblend.galaxy import GalaxyInstance
from typing import Any, Dict, List
import argparse
import json
import logging
from dataclasses import dataclass
import sys
import re


class MissingFieldException(Exception):
    """
    Exception for a missing field in a dict
    """
    pass


#This is shared 
@dataclass

class GalaxyDataset:
    """
    Representation of a galaxy dataset

    Contains attributes that are used in the scope of this script which is only a subset of
    attributes returned by the galaxy api
    """
    name: str
    id: str
    uuid: str
    extension: str
    reference_name: str

    def __init__(self, info: Dict):
        """
        Constructs a GalaxyDataset from a dictionary

        Raises MissingFieldException if an expected key is missing from the given info
        """
        for key in ["name", "id", "uuid", "extension", "metadata_dbkey"]:
            # check for exceptions instead of silently using default
            if not key in info:
                raise MissingFieldException(f"key \"{key}\" not defined")

        self.name = info["name"]
        self.id = info["id"]
        self.uuid = info["uuid"]
        self.extension = info["extension"]
        self.reference_name = info["metadata_dbkey"]


## This is Shared
def set_up_galaxy_instance(galaxy_url: str, galaxy_key: str) -> GalaxyInstance:
    """
    Returns a galaxy instance with the given URL and api key.
    Exits immediately if either connection or authentication to galaxy fails.

        Parameters:
            galaxy_url (str): Base URL of a galaxy instance
            galaxy_key (str): API key with admin privileges

        Returns:
            gi (GalaxyInstance): Galaxy instance with confirmed admin access to the given galaxy instance
    """

    logging.info(f"trying to connect to galaxy at {galaxy_url}")

    # configure a galaxy instance with galaxy_url and api_key
    try:
        gi = GalaxyInstance(galaxy_url, key=galaxy_key)
    except Exception as e:
        # if galaxy_url does not follow the scheme <protocol>://<host>:<port>, GalaxyInstance attempts guessing the URL
        # this exception is thrown when neither "http://<galaxy_url>:80" nor "https://<galaxy_url>:443" are accessible
        logging.critical(f"failed to guess URL from \"{galaxy_url}\" - {e}")
        exit(2)

    # test network connection and successful authentification
    try:
        response = gi.make_get_request(galaxy_url + "/api/whoami")
        content = json.loads(response.content)

        # this request should not fail
        if response.status_code != 200:
            logging.critical(
                f"connection test failed - got HTTP status \"{response.status_code}\" with message \"{content['err_msg']}\"")
            exit(2)

        logging.info(f"connection successful - logged in as user \"{content['username']}\"")

    except Exception as e:
        # if the network connection fails, GalaxyInstance will throw an exception
        logging.critical(f"exception during connection test - \"{e}\"")
        exit(2)

    # test connection with a GET to /api/whoami

    # TODO do the test
    # resp = gi.make_get_request(galaxy_url+ "/api/whoami")
    # resp = gi.make_get_request(galaxy_url + "/api/configuration?keys=allow_user_deletion").content
    return gi

#This is Shared
def string_as_bool(string: Any) -> bool:
    """
    Returns the bool value corresponding to the given value

    used to typesave the api responses
    """
    if str(string).lower() in ("true", "yes", "on", "1"):
        return True
    else:
        return False

def get_beacon_histories(gi: GalaxyInstance) -> List[str]:
    """
    Fetches beacon history IDs from galaxy

        Parameters:
            gi (GalaxyInstance): galaxy instance from which to fetch history IDs

        Returns:
            beacon_histories (List[str]): IDs of all histories that should be imported to beacon
    """
    # history ids will be collected in this lsit
    history_ids: List[str] = []

    # get histories from galaxy api
    # URL is used because the name filter is not supported by bioblend as of now
    response: Response = gi.make_get_request(f"{gi.base_url}/api/histories?q=name&qv=Beacon%20Export%20%F0%9F%93%A1&all=true&deleted=false")

    # check if the reuest was successful
    if response.status_code != 200:
        logging.critical("failed to get histories from galaxy")
        logging.critical(f"got status {response.status_code} with content {response.content}")
        exit(2)

    # retrieve histories from response body
    histories: List[Dict] = json.loads(response.content)

    # for each history double check if the user has beacon sharing enabled
    for history in histories:
        history_details: Dict[str, Any] = gi.histories.show_history(history["id"])
        user_details: Dict[str, Any] = gi.users.show_user(history_details["user_id"])

        # skip adding the history if beacon_enabled is not set for the owner account
        history_user_preferences: Dict[str, str] = user_details["preferences"]
        if "beacon_enabled" not in history_user_preferences or not string_as_bool(history_user_preferences["beacon_enabled"]):
            continue

        history_ids.append(history["id"])

    return history_ids


def get_datasets(gi: GalaxyInstance, history_id: str) -> List[GalaxyDataset]:
    """
    Fetches a given histories datasets from galaxy

        Parameters:
            gi (GalaxyInstance): galaxy instance to be used for the request
            history_id (str): (encoded) ID of the galaxy history

        Returns:
            datasets (List[GalaxyDataset]): list of all datasets in the given history
    """

    # datasets = gi.histories.show_matching_datasets(history_id)

    datasets: List[GalaxyDataset] = []

    offset: int = 0
    limit: int = 500

    # galaxy api uses paging for datasets. This while loop continuously retrieves pages of *limit* datasets
    # The loop breaks the first time an empty page comes up
    while True:
        # TODO extensions only allow one entry atm
        # retrieve a list of datasets from the galaxy api
        api_dataset_list = gi.datasets.get_datasets(
            history_id=history_id,
            deleted=False,
            extension=["json", "json_bgzip"],
            limit=limit,
            offset=offset
        )

        # each api_dataset_list_entry is a dictionary with the fields:
        #    "id", "name", "history_id", "hid", "history_content_type", "deleted", "visible",
        #    "type_id", "type", "create_time", "update_time", "url", "tags", "dataset_id",
        #    "state", "extension", "purged"
        for api_dataset_list_entry in api_dataset_list:
            dataset_info = gi.datasets.show_dataset(dataset_id=api_dataset_list_entry["id"])

            # read dataset information from api
            try:
                dataset = GalaxyDataset(dataset_info)
            except MissingFieldException as e:
                # the exception is thrown by the constructor of GalaxyDataset which checks if all keys that are used
                # actually exists
                logging.warning(
                    f"not reading dataset {api_dataset_list_entry['id']} because {e} from api response")

            # filter for valid human references
            match = re.match(r"(GRCh\d+|hg\d+).*", dataset.reference_name)
            if match is None:
                # skip datasets with unknown references
                logging.warning(
                    f"not reading dataset {dataset.name} with unknown reference \"{dataset.reference_name}\"")
                continue

            # set reference name to the first match group
            #
            # THIS WILL REMOVE PATCH LEVEL FROM THE REFERENCE
            # therefore all patch levels will be grouped under the major version of the reference
            dataset.reference_name = match.group(1)

            datasets.append(dataset)
        offset += limit

        # no entries left
        if len(api_dataset_list) == 0:
            break

    # return the finished dataset list
    return datasets


def download_dataset(gi: GalaxyInstance, dataset: GalaxyDataset, filename: str) -> None:
    """
    Downloads a dataset from galaxy to a given path

        Parameters:
            gi (GalaxyInstance): galaxy instance to download from
            dataset (GalaxyDataset): the dataset to download
            filename (str): output filename including complete path

        Returns:
            Nothing

    """
    try:
        gi.datasets.download_dataset(dataset.id, filename, use_default_filename=False)
    except Exception as e:
        # TODO catch exceptions
        logging.critical(f"something went wrong while downloading file - {e} filename:{filename}")


def import_to_mongodb(datafile_path):
    """
    Import a dataset to beacon

        Parameters:
            BFF_files (dict): key is the file name, and value is full path to the Beacon friendly files

        Returns:
            Nothing

        Note:
            This function uses MongoDB from the beacon2-ri-api package found at https://github.com/EGA-archive/beacon2-ri-api/tree/master/deploy

            The connection settings are configured by ENVIRONMENT_VARIABLE or  "default value" if not set (not sure about the values need to check)

                host: DATABASE_URL / "???",
                port: DATABASE_PORT / "???",
                user: DATABASE_USER / ???",
                password: DATABASE_PASSWORD / beacon",
                database: DATABASE_NAME / mongodb",

    """
    # Import  BFF files
    try:
        with open(datafile_path, "r") as json_file:
            variants = json.load(json_file)
        return variants
    except FileNotFoundError as e:
        print(f"File not found: {datafile_path}")
        logging.info(f"File not found: {datafile_path}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        logging.info(f"JSON decoding error: {e}")


# Function to read JSON data from a file
def read_json_file(file_path):
    try:
        with open(file_path, "r") as json_file:
            variants = json.load(json_file)
        return variants
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        logging.info(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        logging.info(f"JSON decoding error: {e}")


def connect_arguments(parser):
    connection_group = parser.add_argument_group("Connection to MongoDB")
    connection_group.add_argument("-H", "--db-host", type=str, default="127.0.0.1", dest="database_host", help="Hostname/IP of the beacon database")
    connection_group.add_argument("-P", "--db-port", type=int, default=27017, dest="database_port", help="Port of the beacon database")
    
    advance_connection_group = parser.add_argument_group("Addvanced Connection to MongoDB")
    advance_connection_group.add_argument('-a', '--advance-connection', action="store_true", dest="advance", default=False, help="Connect to beacon database with authentication")
    advance_connection_group.add_argument("-A", "--db-auth-source", type=str, metavar="ADMIN", default="", dest="Database_auth_source", help="auth source for the beacon database")
    advance_connection_group.add_argument("-U", "--db-user", type=str, default="", dest="database_user", help="Login user for the beacon database")
    advance_connection_group.add_argument("-W", "--db-password", type=str, default="", dest="database_password", help="Login password for the beacon database")
    advance_connection_group.add_argument("-N", "--db-name", type=str, default="", dest="database_name", help="Name of the beacon database")

    # arguments controlling galaxy connection
    galaxy_connection_group = parser.add_argument_group("Connection to Galaxy")
    galaxy_connection_group.add_argument('-g', '--galaxy', action="store_true", dest="galaxy", default=False, help="Import data from Galaxy")
    galaxy_connection_group.add_argument("-u", "--galaxy-url", type=str, default="", dest="galaxy_url", help="Galaxy hostname or IP")
    galaxy_connection_group.add_argument("-k", "--galaxy-key", type=str, default="", dest="galaxy_key", help="API key of a galaxy user WITH ADMIN PRIVILEGES")
    
    # 
    database_group = parser.add_argument_group("Database Configuration")
    database_group.add_argument("-d", "--database ", type=str, default="", dest="database", help="The targeted beacon database")
    database_group.add_argument("-c", "--collection", type=str, default="", dest="collection", help="The targeted beacon collection from the desired database")
    #

def connect_to_mongodb(args):
    # Connect to MongoDB database with authentication
    if args.advance:
        # check advanced input for connection
        advanced_required_args = ['database_auth_source', 'database_user', 'database_password', 'database_name']
        if any(getattr(args, arg)  == "" for arg in advanced_required_args):
            for arg in advanced_required_args:
                if not getattr(args, arg):
                    print(f"Missing value -> {arg}. Use -h or --help for usage details.")
                    logging.info(f"Missing value -> {arg}")
            parser.print_help()
            sys.exit(1)
        # Connect to MongoDB database with authentication
        client = MongoClient(f"mongodb://{args.database_user}:{args.database_password}@{args.database_host}:{args.database_port}/{args.collection}?authSource={args.database_auth_source}")
    else:
        # Connect to MongoDB database without authentication
        client = MongoClient(args.database_host, args.database_port)
    return client

def clear_collections(db, args):
    """
    Clears collections in the MongoDB database based on the provided arguments.

    Parameters:
        db (MongoClient): MongoDB client connected to the database.
        args (Namespace): Parsed command-line arguments.

    Returns:
        bool: True if collections are cleared successfully, False otherwise.
    """
    existing_names = db.list_collection_names()

    if args.clear_all:
        # Clear all collections
        for name in existing_names:
            try:
                db[name].drop()
            except Exception as e:
                print(f'Warning: Failed to clear collection {name}. Error: {e}')
                logging.info(f'Warning: Failed to clear collection {name}. Error: {e}')
                return False
        return True

    elif args.clear_coll:
        # Clear a specific collection
        for name in existing_names:
            if name == args.removed_col_name:
                try:
                    db[name].drop()
                except Exception as e:
                    print(f'Warning: Failed to clear collection {name}. Error: {e}')
                    logging.info(f'Warning: Failed to clear collection {name}. Error: {e}')
                    return False
        return True

    return False  # No action specified

def MongoDBimporter():
    parser = argparse.ArgumentParser(description="Input arguments")
    connect_arguments(parser)
    beacon_import = parser.add_argument_group("Import Json Arguments")
    beacon_import.add_argument("-i", "--input_json_file", type=str, default="", help="Input the local path to the JSON file or it's name on your Galaxy Hitory to import to beacon")
    # store origin
    store_origin = parser.add_argument_group("store origin")
    store_origin.add_argument("-s", "--store-origins", default=False, dest="store_origins", action="store_true", help="Make a local file containing variantIDs with the dataset they stem from")
    store_origin.add_argument("-o", "--origins-file", type=str, metavar="", default="/tmp/variant-origins.txt", dest="origins_file", help="Full file path of where variant origins should be stored (if enabled)")
    # arguments controlling output
    control_output = parser.add_argument_group("control output")
    control_output.add_argument('-D', '--debug', action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.WARNING)
    control_output.add_argument('-V', '--verbose', dest="loglevel", const=logging.INFO, help="Be verbose", action="store_const")
    # Clear beacon database
    clear_beacon = parser.add_argument_group("Clear beacon database")
    clear_beacon.add_argument('-ca', '--clearAll', action="store_true", dest="clear_all", default=False, help="Delete all data before the new import")
    clear_beacon.add_argument('-cc', '--clearColl', action="store_true", dest="clear_coll", default=False, help="Delete specific collection before the new import")
    clear_beacon.add_argument("-r", "--removeCollection", type=str, default="", dest="removed_coll_name", help="Define the collection name for deletion")
    args = parser.parse_args()
    
    # check inputs
    required_args = ['database', 'collection', 'database_host', 'database_port','input_json_file']
    for arg in required_args:
        if not getattr(args, arg):
            print(f"Missing value -> {arg}. Use -h or --help for usage details.")
            logging.info(f"Missing value -> {arg}")
            parser.print_help()
            sys.exit(1)
    
    # connect to beacon 
    client= connect_to_mongodb(args)
    db = client[args.database]
    collection = db[args.collection]
    
    clear_collections(db, args)
    
    
    
    # connect to Galaxy instance 
    if args.galaxy:
        # Check galaxy inputs to connect to Galaxy
        galaxy_args = ['galaxy_url', 'galaxy_key']
        if any(getattr(args, arg) == "" for arg in galaxy_args):
            for arg in galaxy_args:
                if not getattr(args, arg):
                    print(f"Missing value -> {arg}. Use -h or --help for usage details.")
                    logging.info(f"Missing value -> {arg}")
            parser.print_help()
            sys.exit(1)
    
        gi = set_up_galaxy_instance(args.galaxy_url, args.galaxy_key)
    
        if args.store_origins:
            if os.path.exists(args.origins_file):
                os.remove(args.origins_file)
            # open a file to store variant origins
            try:
                variant_origins_file = open(args.origins_file, "a")
            except:
                print(f"Can not open origins_file {args.origins_file}")
                logging.info(f"Can not open origins_file {args.origins_file}")
                sys.exit(1)
    
        path_dict = {f"{args.input_json_file}": f"/tmp/{args.input_json_file}_file-"}
        # load data from beacon histories
        for history_id in get_beacon_histories(gi):
            for dataset in get_datasets(gi, history_id):
                logging.info(f"next file is {dataset.name}")
                name = dataset.name.split('.')[0]
                path = path_dict[name] + dataset.uuid
                download_dataset(gi, dataset, path)
                variants = import_to_mongodb(path)
                if args.store_origins:
                    persist_variant_origins(dataset.id, path, variant_origins_file)
    
    else:
        variants = read_json_file(args.input_json_file)
    
    if variants is not None:
        for v in variants:
            vid = collection.insert_one(v).inserted_id
            vstr = f"refvar-{vid}"
            collection.update_one({"_id": vid}, {"$set": {"id": vstr}})
            print(f"==> inserted {vstr}")

MongoDBimporter()
