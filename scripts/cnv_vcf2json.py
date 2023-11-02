import argparse
import json
from vcfConverter import vcfConverter



def vcfImporter():
    parser = argparse.ArgumentParser(description='Input arguments')
    parser.add_argument('-v','--vcf_file_path', type=str, default='',help='Input a file path to the VCF file to process. e.g. data/HG00096.cnv.vcf')
    parser.add_argument('-d','--def_file_path', type=str, default='', help='Input a file path to the yaml file as a definition file to process. e.g. data/definition_cnv.yaml')
    parser.add_argument('-jn','--json_file_name', type=str, default='',help='Name the output json file. e.g. HG00096')
    parser.add_argument('-jp','--json_file_path', type=str, default='',help='Input a directory path of output json file. e.g. data/')
    args = parser.parse_args()
    if args.vcf_file_path == '':
        print('Input VCF file')
        parser.print_help()
        exit(1)
    if args.def_file_path == '':
        print('Input yaml file')
        parser.print_help()
        exit(1)
    if args.json_file_name == '':
        print('Input json file name')
        parser.print_help()
        exit(1)
    if args.json_file_path == '':
        print('Input json file directory')
        parser.print_help()
        exit(1)
    converter = vcfConverter(vcf_file=args.vcf_file_path)
    beacon_struct = converter.convertVariants(def_file=args.def_file_path)
    json_file_path=f'{args.json_file_path}{args.json_file_name}.json'
    with open(json_file_path, "w") as outfile:
        json.dump(beacon_struct, outfile)

vcfImporter()
