##read params
## process
## Return dataframe

from webbrowser import get
import yaml
import os
import pandas as pd
import argparse

def read_yaml(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config



def get_data(config_path):
    config = read_yaml(config_path)
    data_path = config['data_source']['s3_source']
    df = pd.read_csv(data_path, sep=',', encoding='utf-8')
    return df


#data fetced



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    df = get_data(config_path = parsed_args.config)
    print(df.columns)
