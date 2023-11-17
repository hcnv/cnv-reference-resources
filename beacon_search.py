from pymongo import MongoClient
import argparse
import pprint

def beacon_query():
    parser = argparse.ArgumentParser(description="Query Beacon Database")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Sub-parser for command "Beacon Sequence Queries"
    parser_sequence = subparsers.add_parser('sequence_queries')
    parser_sequence.add_argument('-c', '--collection', type=str, default='', dest='collection', help="The targeted beacon collection")
    parser_sequence.add_argument('-d', '--dataset', type=str, default='', dest='dataset', help="The targeted beacon dataset from the desired collection")
    parser_sequence.add_argument('-I', '--db-ip', type=str, default='127.0.0.1', dest='db_ip', help='Input MongoDB IP address')
    parser_sequence.add_argument("-P", "--db-port", type=int, default="27017", dest='db_port', dest="database_port", help="port of the beacon database")
    parser_sequence.add_argument("-rn", "--referenceName", type=str, default='', dest='referenceName', help='Reference name')
    parser_sequence.add_argument("-s", "--start", type=int, default='', dest='start', help='Start')
    parser_sequence.add_argument("-ab", "--alternateBases", type=str, default='', dest='alternateBases', help='Alternate Bases')
    parser_sequence.add_argument("-rb", "--referenceBases", type=str, default='', dest='referenceBases', help='Reference Bases')
    parser_sequence.add_argument("-id", "--datasetIds", type=str, default='', dest='datasetIds', help='dataset Id') # optional

    # Sub-parser for command "Beacon Range Queries"
    parser_range = subparsers.add_parser('range_queries')
    parser_range.add_argument('-c', '--collection', type=str, default='', dest='collection', help="The targeted beacon collection")
    parser_range.add_argument('-d', '--dataset', type=str, default='', dest='dataset', help="The targeted beacon dataset from the desired collection")
    parser_range.add_argument('-I', '--db-ip', type=str, default='127.0.0.1', dest='db_ip', help='Input MongoDB IP address')
    parser_range.add_argument("-P", "--db-port", type=int, default="27017", dest="db_port", help="port of the beacon database")
    parser_range.add_argument("-rn", "--referenceName", type=str, default='', dest='referenceName', help='Reference name')
    parser_range.add_argument("-s", "--start", type=int, default='', dest='start', help='Start')
    parser_range.add_argument("-e", "--end", type=int, default='', dest='end', help='END')
    parser_range.add_argument("-ab", "--alternateBases", type=str, default='', dest='alternateBases', help='Alternate Bases') #
    parser_range.add_argument("-v", "--variantType", type=str, default='', dest='variantType', help='Variant Type')
    parser_range.add_argument("-ac", "--aminoacidChange", type=str, default='', dest='aminoacidChange', help='Aminoacid Change')
    parser_range.add_argument("vmax", "--variantMinLength", type=int, default='', dest='variantMinLength', help='Variant Minimum Length')
    parser_range.add_argument("vmin", "--variantMaxLength", type=int, default='', dest='variantMaxLength', help='variant Maximum Length')

    # Sub-parser for command "Beacon GeneId Queries"
    parser_gene = subparsers.add_parser('gene_id_queries')
    parser_gene.add_argument('-c', '--collection', type=str, default='', dest='collection', help="The targeted beacon collection")
    parser_gene.add_argument('-d', '--dataset', type=str, default='', dest='dataset', help="The targeted beacon dataset from the desired collection")
    parser_gene.add_argument('-I', '--db-ip', type=str, default='127.0.0.1', dest='db_ip', help='Input MongoDB IP address')
    parser_gene.add_argument("-P", "--db-port", type=int, default="27017", dest="db_port", help="port of the beacon database")
    parser_gene.add_argument("-g", "--geneId", type=str, default='', dest='geneId', help='Gene ID')
    parser_gene.add_argument("-ab", "--alternateBases", type=str, default='', dest='alternateBases', help='Alternate Bases')
    parser_gene.add_argument("-v", "--variantType", type=str, default='', dest='variantType', help='Variant Type')
    parser_gene.add_argument("-ac", "--aminoacidChange", type=str, default='', dest='aminoacidChange', help='Aminoacid Change')
    parser_gene.add_argument("vmax", "--variantMinLength", type=int, default='', dest='variantMinLength', help='Variant Minimum Length')
    parser_gene.add_argument("vmin", "--variantMaxLength", type=int, default='', dest='variantMaxLength', help='variant Maximum Length')

    # Sub-parser for command "Beacon Bracket Queries"
    parser_bracket = subparsers.add_parser('bracket_queries')
    parser_bracket.add_argument('-c', '--collection', type=str, default='', dest='collection', help="The targeted beacon collection")
    parser_bracket.add_argument('-d', '--dataset', type=str, default='', dest='dataset', help="The targeted beacon dataset from the desired collection")
    parser_bracket.add_argument('-I', '--db-ip', type=str, default='127.0.0.1', dest='db_ip', help='Input MongoDB IP address')
    parser_bracket.add_argument("-P", "--db-port", type=int, default="27017", dest="db_port", help="port of the beacon database")
    parser_bracket.add_argument("-rn", "--referenceName", type=str, default='', dest='referenceName', help='Reference name')
    parser_bracket.add_argument("-smin", "--start-minimum", type=int, default='', dest='start_minimum', help='Start Minimum')
    parser_bracket.add_argument("-smax", "--start-maximum", type=int, default='', dest='start_maximum', help='Start maximum')
    parser_bracket.add_argument("-emin", "--end-minimum", type=int, default='', dest='end_minimum', help='END Minimum')
    parser_bracket.add_argument("-emax", "--end-maximum", type=int, default='', dest='end_maximum', help='END maximum')
    parser_bracket.add_argument("-v", "--variantType", type=str, default='', dest='variantType', help='Variant Type')

    args = parser.parse_args()


    #  query sequence_queries
    if args.command == 'sequence':
        client = MongoClient(args.db_ip, args.db_port)
        db = client[args.collection]
        sample = db[args.dataset]
        query = {
              'referenceName': args.referenceName,
              'start': args.start,
              'alternateBases': args.alternateBases,
              'referenceBases': args.referenceBases,
              'datasetIds': args.datasetIds
                }
        # Create a new dictionary with non-empty and non-default values
        filtered_query = {key: value for key, value in query.items() if value}
#        if not args.datasetIds: 
#            query= {'referenceName': args.referenceName, 'start': args.start, 'alternateBases':args.alternateBases , 'referenceBases':args.referenceBases}
#        else:
#            query= {'referenceName': args.referenceName, 'start': args.start, 'alternateBases':args.alternateBases , 'referenceBases':args.referenceBases, 'datasetIds': args.datasetIds}
        for v in sample.find(filtered_query):
            pprint.pprint(v)
    #  query range_queries
    
    elif args.command == 'range':
        if args.command == 'range':
        client = MongoClient(args.db_ip, args.db_port)
        db = client[args.collection]
        sample = db[args.dataset]
        query = {
              'referenceName': args.referenceName,
              'start': args.start,
              'end': args.end,
              'variantType': args.variantType,
              'alternateBases': args.alternateBases,
              'aminoacidChange':args.aminoacidChange,
              'variantMinLength':args.variantMinLength,
              'variantMaxLength':args.variantMaxLength
                }
        # Create a new dictionary with non-empty and non-default values
        filtered_query = {key: value for key, value in query.items() if value}
#        if not args.alternateBases, args.variantType, args.aminoacidChange, args.variantMinLength, args.variantMaxLength: 
#            query= {'referenceName': args.referenceName, 'start': args.start, 'end':args.end}
#        elif not args.variantType, args.aminoacidChange, args.variantMinLength, args.variantMaxLength: 
#            query= {'referenceName': args.referenceName, 'start': args.start, 'end':args.end, 'alternateBases':args.alternateBases}
#        elif not args.alternateBases, args.aminoacidChange, args.variantMinLength, args.variantMaxLength:
#            query= {'referenceName': args.referenceName, 'start': args.start, 'end':args.end, 'variantType':args.variantType}
#        elif not args.alternateBases, args.aminoacidChange, args.variantMaxLength:
#            query= {'referenceName': args.referenceName, 'start': args.start, 'end':args.end, 'variantType':args.variantType, 'variantMinLength':args.variantMinLength}
#        elif not args.alternateBases, args.aminoacidChange:
#            query= {'referenceName': args.referenceName, 'start': args.start, 'end':args.end, 'variantType':args.variantType, 'variantMinLength':args.variantMinLength, 'variantMaxLength':args.variantMaxLength}
#        elif not args.variantType, args.alternateBases, args.variantMinLength, args.variantMaxLength: 
#            query= {'referenceName': args.referenceName, 'start': args.start, 'end':args.end, 'aminoacidChange':args.aminoacidChange}
        for v in sample.find(filtered_query):
            pprint.pprint(v)
    
    #  query gene_id_queries
    elif args.command == 'gene_id':
        if args.command == 'gene_id':
        client = MongoClient(args.db_ip, args.db_port)
        db = client[args.collection]
        sample = db[args.dataset]
        query = {
              'geneId': args.geneId,
              'variantType': args.variantType,
              'alternateBases': args.alternateBases,
              'aminoacidChange':args.aminoacidChange,
              'variantMinLength':args.variantMinLength,
              'variantMaxLength':args.variantMaxLength
                }
        # Create a new dictionary with non-empty and non-default values
        filtered_query = {key: value for key, value in query.items() if value}
#        if not args.alternateBases, args.variantType, args.aminoacidChange, args.variantMinLength, args.variantMaxLength: 
#            query= {'geneId': args.geneId}
#        elif not args.variantType, args.aminoacidChange, args.variantMinLength, args.variantMaxLength: 
#            query= {'geneId': args.geneId, 'alternateBases':args.alternateBases}
#        elif not args.alternateBases, args.aminoacidChange, args.variantMinLength, args.variantMaxLength:
#            query= {'geneId': args.geneId, 'variantType':args.variantType}
#        elif not  args.alternateBases, args.variantMinLength, args.variantMaxLength: 
#            query= {'geneId': args.geneId, 'variantType':args.variantType 'aminoacidChange':args.aminoacidChange}
#        elif not args.alternateBases, args.aminoacidChange, args.variantMaxLength:
#            query= {'geneId': args.geneId, 'variantType':args.variantType, 'variantMinLength':args.variantMinLength}
#        elif not args.alternateBases, args.aminoacidChange, args.variantMinLength:
#            query= {'geneId': args.geneId, 'variantType':args.variantType, 'variantMaxLength':args.variantMaxLength}
#        elif not  args.alternateBases, args.variantMaxLength: 
#            query= {'geneId': args.geneId, 'variantType':args.variantType 'aminoacidChange':args.aminoacidChange, 'variantMinLength':args.variantMinLength}
#        elif not args.alternateBases, args.aminoacidChange:
#            query= {'geneId': args.geneId, 'variantType':args.variantType, 'variantMinLength':args.variantMinLength, 'variantMaxLength':args.variantMaxLength}
#        elif not args.alternateBases:
#            query= {'geneId': args.geneId, 'variantType':args.variantType, 'aminoacidChange':args.aminoacidChange, 'variantMinLength':args.variantMinLength, 'variantMaxLength':args.variantMaxLength}
#        elif not args.variantType, args.alternateBases, args.variantMinLength, args.variantMaxLength: 
#            query= {'geneId': args.geneId, 'aminoacidChange':args.aminoacidChange}
        for v in sample.find(filtered_query):
            pprint.pprint(v)
    #  query bracket_queries
    elif args.command == 'bracket':
        if args.command == 'bracket':
        client = MongoClient(args.db_ip, args.db_port)
        db = client[args.collection]
        sample = db[args.dataset]
        query = {
              'referenceName': args.geneId,
              'start': args.start_minimum,
              'start': args.start_maximum,
              'end':args.end_minimum,
              'end':args.end_maximum,
              'variantType':args.variantType
                }
        # Create a new dictionary with non-empty and non-default values
        filtered_query = {key: value for key, value in query.items() if value}
#        if not args.variantType: 
#            query= {'referenceName': args.referenceName, 'start': args.start_minimum, 'start': args.start_maximum, 'end':args.end_minimum, 'end':args.end_maximum}
#        else: 
#            query= {'referenceName': args.referenceName, 'start': args.start_minimum, 'start': args.start_maximum, 'end':args.end_minimum, 'end':args.end_maximum, 'variantType':args.variantType}
        for v in sample.find(filtered_query):
            pprint.pprint(v)

if __name__ == "__main__":
    beacon_query()