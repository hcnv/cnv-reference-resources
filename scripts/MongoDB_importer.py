from pymongo import MongoClient
import argparse
import json

def MongoDBimporter():
    parser = argparse.ArgumentParser(description='Input arguments')
    parser.add_argument('-i', '--input_json_file', type=str, default='', help='Input a file path to the JSON file to import')
    parser.add_argument('-d', '--database_name', type=str, default='', help='Name the created MongoDB database')
    parser.add_argument('-v', '--variant_file_name', type=str, default='', help='Name the Variant file in the MongoDB database')
    parser.add_argument('-I', '--MongoDB_IP_address', type=str, default='localhost', help='Input MongoDB IP address')
    parser.add_argument("-P", "--db-port", type=int, default="27017", dest="database_port", help="port of the beacon database")
    args = parser.parse_args()
    if args.input_json_file == '':
        print('Input JSON file')
        parser.print_help()
        exit(1)
    if args.database_name == '':
        print('Add database name')
        parser.print_help()
        exit(1)
    if args.variant_file_name == '':
        print('Add variant file name')
        parser.print_help()
        exit(1)
    if args.MongoDB_IP_address == '':
        print('Input MongoDB IP address')
        parser.print_help()
        exit(1)
    
    db_client = MongoClient(args.MongoDB_IP_address,args.database_port)
    database = db_client[args.database_name]
    var_coll = database[args.variant_file_name]
    
    # Function to read JSON data from a file
    def read_json_file(file_path):
        try:
            with open(file_path, 'r') as json_file:
                variants = json.load(json_file)
                return variants
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
    
    variants = read_json_file(args.input_json_file)
    if variants is not None:
        for v in variants:
            vid = var_coll.insert_one(v).inserted_id
            vstr = f'refvar-{vid}'
            var_coll.update_one({'_id': vid}, {'$set': {'id': vstr}})
            print(f'==> inserted {vstr}')

MongoDBimporter()
