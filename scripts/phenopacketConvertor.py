#this script is for generate phenopacket from metadata for given biosample
import pandas as pd
import yaml
import argparse
import json

def phenopacketConvertor():
    parser = argparse.ArgumentParser(description='Input arguments')
    parser.add_argument('-i', '--input_meta_file', type=str, default='', help='Input metadata file')
    parser.add_argument('-b', '--biosample', type=str, default='', help='Biosample ID')
    parser.add_argument('-s', '--schema', type=str, default='', help='schema YAML file')
    parser.add_argument('-o', '--output', type=str, default='', help='schema YAML file')
    args = parser.parse_args()
    if args.input_meta_file == '':
        print('Input meta file')
        parser.print_help()
        exit(1)
    if args.biosample == '':
        print('Add database name')
        parser.print_help()
        exit(1)
    if args.schema == '':
        print('Add variant file name')
        parser.print_help()
        exit(1)
    sex_dict = {"female": {"id": "PATO:0020002", "label": "female genotypic sex"},
                "male": {"id": "PATO:0020001", "label": "male genotypic sex"}}
    
    meta=pd.read_csv(args.input_meta_file)
    
    try:
        index = list(meta[meta["SAMPLE_NAME"] == args.biosample].index)[0]
    except IndexError:
        print(f'Biosample {args.biosample} not found in the metadata.')
        exit(1)
    
    with open(args.schema, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        yaml_data["biosamples"][0]["externalReferences"][0]["id"] = "biosample:"+meta.loc[index,"BIOSAMPLE_ID"]
        yaml_data["id"] = meta.loc[index,"SAMPLE_NAME"]
        yaml_data["individual_id"] = "onekgind-"+meta.loc[index, "SAMPLE_NAME"]
        yaml_data["subject"]["id"] = "onekgind-"+meta.loc[index, "SAMPLE_NAME"]
        yaml_data["subject"]["sex"] = sex_dict[meta.loc[index,"SEX"]]
        with open(args.output, "w") as outfile:
            print("1")
            json.dump(yaml_data, outfile, indent=2)

if __name__ == "__main__":
    phenopacketConvertor()