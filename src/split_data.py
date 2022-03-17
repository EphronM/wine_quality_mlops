# split raw data
# savein data/processed folder

import os
import argparse
from random import random
import pandas as pd
from sklearn.model_selection import train_test_split
from get_data import read_yaml, get_data


def split_and_save(config_path):
    config = read_yaml(config_path)
    train_path = config['split_data']['train_path']
    test_path = config['split_data']['test_path']
    split_ratio = config['split_data']['test_size']
    raw_data_path = config['load_data']['raw_dataset_csv']
    random_state = config['base']['random_state']
    df = pd.read_csv(raw_data_path, sep=',', encoding='utf-8')

    train, test = train_test_split(
        df,
        test_size=split_ratio,
        random_state=random_state
        ) 
    train.to_csv(train_path, sep=',',index=False, encoding='utf-8')
    test.to_csv(test_path, sep=',',index=False, encoding='utf-8')


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()

    split_and_save(config_path = parsed_args.config)