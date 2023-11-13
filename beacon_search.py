from pymongo import MongoClient
import argparse
import pprint

def beacon_query():
    parser = argparse.ArgumentParser(description="Query Beacon Database")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Sub-parser for command "Beacon Sequence Queries"
    parser_sequence = subparsers.add_parser('sequence_queries')
    parser_sequence.add_argument('-c', '--collection', type=str, default='', help="The targeted beacon collection")
    parser_sequence.add_argument('-d', '--dataset', type=str, default='', help="The targeted beacon dataset from the desired collection")
    parser_sequence.add_argument('-I', '--db_ip', type=str, default='127.0.0.1', help='Input MongoDB IP address')
    parser_sequence.add_argument("-P", "--db-port", type=int, default="27017", dest="database_port", help="port of the beacon database")
    parser_sequence.add_argument("-r", "--referenceName", type=str, default='', help='Reference name')
    parser_sequence.add_argument("-s", "--start", type=int, default='', help='Start')
    parser_sequence.add_argument("-a", "--alternateBases", type=str, default='', help='Alternate Bases')
    parser_sequence.add_argument("-rb", "--referenceBases", type=str, default='', help='Reference Bases')
    parser_sequence.add_argument("-id", "--datasetIds", type=str, default='', help='dataset Id')

    # Sub-parser for command "Beacon Range Queries"
    parser_range = subparsers.add_parser('range_queries')
    parser_range.add_argument('-c', '--collection', type=str, default='', help="The targeted beacon collection")
    parser_range.add_argument('-d', '--dataset', type=str, default='', help="The targeted beacon dataset from the desired collection")
    parser_range.add_argument('-I', '--db_ip', type=str, default='127.0.0.1', help='Input MongoDB IP address')
    parser_range.add_argument("-P", "--db-port", type=int, default="27017", dest="database_port", help="port of the beacon database")
    parser_range.add_argument("-r", "--referenceName", type=str, default='', help='Reference name')
    parser_range.add_argument("-s", "--start", type=int, default='', help='Start')
    parser_range.add_argument("-e", "--end", type=int, default='', help='END')
    parser_range.add_argument("-a", "--alternateBases", type=str, default='', help='Alternate Bases')
    parser_range.add_argument("-rb", "--variantType", type=str, default='', help='Variant Type')
    parser_range.add_argument("-id", "--aminoacidChange", type=str, default='', help='Aminoacid Change')
    parser_range.add_argument("-max", "--variantMinLength", type=int, default='', help='Variant Minimum Length')
    parser_range.add_argument("-min", "--variantMaxLength", type=int, default='', help='variant Maximum Length')

    # Sub-parser for command "Beacon GeneId Queries"
    parser_gene = subparsers.add_parser('gene_id_queries')
    parser_gene.add_argument('-c', '--collection', type=str, default='', help="The targeted beacon collection")
    parser_gene.add_argument('-d', '--dataset', type=str, default='', help="The targeted beacon dataset from the desired collection")
    parser_gene.add_argument('-I', '--db_ip', type=str, default='127.0.0.1', help='Input MongoDB IP address')
    parser_gene.add_argument("-P", "--db-port", type=int, default="27017", dest="database_port", help="port of the beacon database")
    parser_gene.add_argument("-g", "--geneId", type=str, default='', help='Gene ID')
    parser_gene.add_argument("-a", "--alternateBases", type=str, default='', help='Alternate Bases')
    parser_gene.add_argument("-rb", "--variantType", type=str, default='', help='Variant Type')
    parser_gene.add_argument("-id", "--aminoacidChange", type=str, default='', help='Aminoacid Change')
    parser_gene.add_argument("-max", "--variantMinLength", type=int, default='', help='Variant Minimum Length')
    parser_gene.add_argument("-min", "--variantMaxLength", type=int, default='', help='variant Maximum Length')

    # Sub-parser for command "Beacon Bracket Queries"
    parser_bracket = subparsers.add_parser('bracket_queries')
    parser_bracket.add_argument('-c', '--collection', type=str, default='', help="The targeted beacon collection")
    parser_bracket.add_argument('-d', '--dataset', type=str, default='', help="The targeted beacon dataset from the desired collection")
    parser_bracket.add_argument('-I', '--db_ip', type=str, default='127.0.0.1', help='Input MongoDB IP address')
    parser_bracket.add_argument("-P", "--db-port", type=int, default="27017", dest="database_port", help="port of the beacon database")
    parser_bracket.add_argument("-r", "--referenceName", type=str, default='', help='Reference name')
    parser_bracket.add_argument("-s-min", "--start-minimum", type=int, default='', help='Start Minimum')
    parser_bracket.add_argument("-s-max", "--start-maximum", type=int, default='', help='Start maximum')
    parser_bracket.add_argument("-e-min", "--end-minimum", type=int, default='', help='END Minimum')
    parser_bracket.add_argument("-e-max", "--end-maximum", type=int, default='', help='END maximum')
    parser_bracket.add_argument("-rb", "--variantType", type=str, default='', help='Variant Type')

    args = parser.parse_args()

    client = MongoClient(args.db_ip, args.database_port)
    db = client.cnv
    sample = db.sample1

    # Example query based on command
    if args.command == 'sequence_queries':
        for v in sample.find({'start': args.start, 'end': args.end}):
            pprint.pprint(v)
    elif args.command == 'range_queries':
        # Add logic for range_queries
        pass
    elif args.command == 'gene_id_queries':
        # Add logic for gene_id_queries
        pass
    elif args.command == 'bracket_queries':
        # Add logic for bracket_queries
        pass

if __name__ == "__main__":
    beacon_query()

#    client = MongoClient("127.0.0.1", 27017)
#    db = client.cnv
#    sample = db.sample1
    
    #sample.find({'start': 11744914})
    
    
#    for v in sample.find({'start': 11744914, 'end': 11748800}):
#        pprint.pprint(v)

#pprint.pprint(sample.find_one()) 
#print(sample.list_collection_names())
#if __name__ == "__main__":
#    beacon_query()