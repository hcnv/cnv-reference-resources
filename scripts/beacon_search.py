from pymongo import MongoClient
import argparse
import pprint

def beacon_query():
    parser = argparse.ArgumentParser(description="Query Beacon Database")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Sub-parser for command "Beacon Sequence Queries"
    parser_sequence = subparsers.add_parser('sequence')
    parser_sequence.add_argument('-c', '--database', type=str, default='', dest='database', help="The targeted beacon database")
    parser_sequence.add_argument('-d', '--dataset', type=str, default='', dest='dataset', help="The targeted beacon dataset from the desired database")
    parser_sequence.add_argument('-I', '--db-ip', type=str, default='127.0.0.1', dest='db_ip', help='Input MongoDB IP address')
    parser_sequence.add_argument("-P", "--db-port", type=int, default=27017, dest='db_port', help="port of the beacon database")
    parser_sequence.add_argument("-rn", "--referenceName", type=str, default='', dest='referenceName', help='Reference name')
    parser_sequence.add_argument("-s", "--start", type=int, default=None, dest='start', help='Start')
    parser_sequence.add_argument("-ab", "--alternateBases", type=str, default='', dest='alternateBases', help='Alternate Bases')
    parser_sequence.add_argument("-rb", "--referenceBases", type=str, default='', dest='referenceBases', help='Reference Bases')
    parser_sequence.add_argument("-id", "--datasetIds", type=str, default='', dest='datasetIds', help='dataset Id')  # optional
    
    # Sub-parser for command "Beacon Range Queries"
    parser_range = subparsers.add_parser('range')
    parser_range.add_argument('-c', '--database', type=str, default='', dest='database', help="The targeted beacon database")
    parser_range.add_argument('-d', '--dataset', type=str, default='', dest='dataset', help="The targeted beacon dataset from the desired database")
    parser_range.add_argument('-I', '--db-ip', type=str, default='127.0.0.1', dest='db_ip', help='Input MongoDB IP address')
    parser_range.add_argument("-P", "--db-port", type=int, default="27017", dest="db_port", help="port of the beacon database")
    parser_range.add_argument("-rn", "--referenceName", type=str, default='', dest='referenceName', help='Reference name')
    parser_range.add_argument("-s", "--start", type=int, default=None, dest='start', help='Start')
    parser_range.add_argument("-e", "--end", type=int, default=None, dest='end', help='END')
    parser_range.add_argument("-ab", "--alternateBases", type=str, default='', dest='alternateBases', help='Alternate Bases') #
    parser_range.add_argument("-v", "--variantType", type=str, default='', dest='variantType', help='Variant Type')
    parser_range.add_argument("-ac", "--aminoacidChange", type=str, default='', dest='aminoacidChange', help='Aminoacid Change')
    parser_range.add_argument("-vmax", "--variantMinLength", type=int, default=None, dest='variantMinLength', help='Variant Minimum Length')
    parser_range.add_argument("-vmin", "--variantMaxLength", type=int, default=None, dest='variantMaxLength', help='variant Maximum Length')

    # Sub-parser for command "Beacon GeneId Queries"
    parser_gene = subparsers.add_parser('gene')
    parser_gene.add_argument('-c', '--database', type=str, default='', dest='database', help="The targeted beacon database")
    parser_gene.add_argument('-d', '--dataset', type=str, default='', dest='dataset', help="The targeted beacon dataset from the desired database")
    parser_gene.add_argument('-I', '--db-ip', type=str, default='127.0.0.1', dest='db_ip', help='Input MongoDB IP address')
    parser_gene.add_argument("-P", "--db-port", type=int, default="27017", dest="db_port", help="port of the beacon database")
    parser_gene.add_argument("-g", "--geneId", type=str, default='', dest='geneId', help='Gene ID')
    parser_gene.add_argument("-ab", "--alternateBases", type=str, default='', dest='alternateBases', help='Alternate Bases')
    parser_gene.add_argument("-v", "--variantType", type=str, default='', dest='variantType', help='Variant Type')
    parser_gene.add_argument("-ac", "--aminoacidChange", type=str, default='', dest='aminoacidChange', help='Aminoacid Change')
    parser_gene.add_argument("-vmax", "--variantMinLength", type=int, default=None, dest='variantMinLength', help='Variant Minimum Length')
    parser_gene.add_argument("-vmin", "--variantMaxLength", type=int, default=None, dest='variantMaxLength', help='variant Maximum Length')

    # Sub-parser for command "Beacon Bracket Queries"
    parser_bracket = subparsers.add_parser('bracket')
    parser_bracket.add_argument('-c', '--database', type=str, default='', dest='database', help="The targeted beacon database")
    parser_bracket.add_argument('-d', '--dataset', type=str, default='', dest='dataset', help="The targeted beacon dataset from the desired database")
    parser_bracket.add_argument('-I', '--db-ip', type=str, default='127.0.0.1', dest='db_ip', help='Input MongoDB IP address')
    parser_bracket.add_argument("-P", "--db-port", type=int, default="27017", dest="db_port", help="port of the beacon database")
    parser_bracket.add_argument("-rn", "--referenceName", type=str, default='', dest='referenceName', help='Reference name')
    parser_bracket.add_argument("-smin", "--start-minimum", type=int, default=None, dest='start_minimum', help='Start Minimum')
    parser_bracket.add_argument("-smax", "--start-maximum", type=int, default=None, dest='start_maximum', help='Start maximum')
    parser_bracket.add_argument("-emin", "--end-minimum", type=int, default=None, dest='end_minimum', help='END Minimum')
    parser_bracket.add_argument("-emax", "--end-maximum", type=int, default=None, dest='end_maximum', help='END maximum')
    parser_bracket.add_argument("-v", "--variantType", type=str, default='', dest='variantType', help='Variant Type')

    args = parser.parse_args()
    
    
    # query sequence_queries
    if args.command == 'sequence':
        if args.database   == '':
            print('Missing value -> database')
            parser_sequence.print_help()
            exit(1)
        if args.dataset  == '':
            print('Missing value -> dataset')
            parser_sequence.print_help()
            exit(1)
        if args.db_ip == '':
            print('Missing value -> db_ip')
            parser_sequence.print_help()
            exit(1)
        if args.db_port is None:
            print('Missing value -> db_port')
            parser_sequence.print_help()
            exit(1)
        if args.referenceName   == '':
            print('Missing value -> referenceName')
            parser_sequence.print_help()
            exit(1)
        if args.start is None:
            print('Missing value -> start')
            parser_sequence.print_help()
            exit(1)
        if args.alternateBases is None:
            print('Missing value -> alternateBases')
            parser_sequence.print_help()
            exit(1)
        if args.referenceBases is None:
            print('Missing value -> referenceBases')
            parser_sequence.print_help()
            exit(1)
        query = {
            'referenceName': args.referenceName,
            'start': args.start,
            'alternateBases': args.alternateBases,
            'referenceBases': args.referenceBases,
            'datasetIds': args.datasetIds
        }
        # MongoDB connection
        client = MongoClient(args.db_ip, args.db_port)
        db = client[args.database]
        sample = db[args.dataset]
    # query range_queries
    elif args.command == 'range':
        if args.database  == '':
            print('Missing value -> database')
            parser_range.print_help()
            exit(1)
        if args.dataset == '':
            print('Missing value -> dataset')
            parser_range.print_help()
            exit(1)
        if args.db_ip == '':
            print('Missing value -> db_ip')
            parser_range.print_help()
            exit(1)
        if args.db_port is None:
            print('Missing value -> db_port')
            parser_range.print_help()
            exit(1)
        if args.referenceName   == '':
            print('Missing value -> referenceName')
            parser_range.print_help()
            exit(1)
        if args.start is None:
            print('Missing value -> start')
            parser_range.print_help()
            exit(1)
        if args.end is None:
            print('Missing value -> end')
            parser_range.print_help()
            exit(1)
        query = {
            'referenceName': args.referenceName,
            'start': args.start,
            'end': args.end,
            'variantType': args.variantType,
            'alternateBases': args.alternateBases,
            'aminoacidChange': args.aminoacidChange,
            'variantMinLength': args.variantMinLength,
            'variantMaxLength': args.variantMaxLength
        }
        # MongoDB connection
        client = MongoClient(args.db_ip, args.db_port)
        db = client[args.database]
        sample = db[args.dataset]
    # query gene_id_queries
    elif args.command == 'gene':
        if args.database  == '':
            print('Missing value -> database')
            parser_gene.print_help()
            exit(1)
        if args.dataset == '':
            print('Missing value -> dataset')
            parser_gene.print_help()
            exit(1)
        if args.db_ip == '':
            print('Missing value -> db_ip')
            parser_gene.print_help()
            exit(1)
        if args.db_port is None:
            print('Missing value -> db_port')
            parser_gene.print_help()
            exit(1)
        if args.geneId == '':
            print('Missing value -> geneId')
            parser_gene.print_help()
            exit(1)
        query = {
            'geneId': args.geneId,
            'variantType': args.variantType,
            'alternateBases': args.alternateBases,
            'aminoacidChange': args.aminoacidChange,
            'variantMinLength': args.variantMinLength,
            'variantMaxLength': args.variantMaxLength
        }
        # MongoDB connection
        client = MongoClient(args.db_ip, args.db_port)
        db = client[args.database]
        sample = db[args.dataset]
    # query bracket_queries
    elif args.command == 'bracket':
        if args.database  == '':
            print('Missing value -> database')
            parser_bracket.print_help()
            exit(1)
        if args.dataset == '':
            print('Missing value -> dataset')
            parser_bracket.print_help()
            exit(1)
        if args.db_ip == '':
            print('Missing value -> db_ip')
            parser_bracket.print_help()
            exit(1)
        if args.db_port is None:
            print('Missing value -> db_port')
            parser_bracket.print_help()
            exit(1)
        if args.referenceName  == '':
            print('Missing value -> referenceName')
            parser_bracket.print_help()
            exit(1)
        if args.start_minimum is None:
            print('Missing value -> start_minimum')
            parser_bracket.print_help()
            exit(1)
        if args.start_maximum is None:
            print('Missing value -> start_maximum')
            parser_bracket.print_help()
            exit(1)
        if args.end_minimum is None:
            print('Missing value -> end_minimum')
            parser_bracket.print_help()
            exit(1)
        if args.end_maximum is None:
            print('Missing value -> end_maximum')
            parser_bracket.print_help()
            exit(1)
        query = {
            'referenceName': args.geneId,
            'start': {'$gte': args.start_minimum, '$lte': args.start_maximum},
            'end': {'$gte': args.end_minimum, '$lte': args.end_maximum},
            'variantType': args.variantType
        }
        # MongoDB connection
        client = MongoClient(args.db_ip, args.db_port)
        db = client[args.database]
        sample = db[args.dataset]
    # Create a new dictionary with non-empty and non-default values
    filtered_query = {key: value for key, value in query.items() if value}
    for v in sample.find(filtered_query):
        pprint.pprint(v)

if __name__ == "__main__":
    beacon_query()
