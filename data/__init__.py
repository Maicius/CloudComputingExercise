import pandas as pd
import json
from copy import deepcopy


def read_data_from_json():
    data_c9 = pd.DataFrame(open_file('../data/c9_company_date_result.json'))
    data_985 = pd.DataFrame(open_file('../data/p985_company_date_result.json'))
    data_basic = pd.DataFrame(open_file('../data/basic_company_date_result.json'))
    data_top = pd.DataFrame(open_file('../data/top_company_date_result.json'))
    data_211 = pd.DataFrame(open_file('../data/p211_company_date_result.json'))
    print(data_c9.shape)
    print(data_211.shape)
    print(data_basic.shape)
    all_date_df = pd.DataFrame(
        pd.concat([data_c9['name'], data_985['name'], data_211['name'], data_top['name'], data_basic['name']], axis=0))
    all_date_df = all_date_df.groupby(['name']).sum().reset_index()
    all_date_df['value'] = 0

    concat_c9 = concat_df(deepcopy(all_date_df), deepcopy(data_c9), 'c9')
    concat_985 = concat_df(deepcopy(all_date_df), deepcopy(data_985), '985')
    concat_211 = concat_df(deepcopy(all_date_df), deepcopy(data_211), '211')
    concat_top = concat_df(deepcopy(all_date_df), deepcopy(data_top), 'top')
    concat_basic = concat_df(deepcopy(all_date_df), deepcopy(data_basic), 'basic')

    result_df = pd.DataFrame(pd.concat([deepcopy(all_date_df), concat_c9['c9'], concat_985['985'],
                                        concat_211['211'], concat_top['top'], concat_basic['basic']], axis=1))

    result_df.to_csv("../data/result_json.csv")
    pass


def open_file(filename):
    with open(filename, 'r', encoding='utf-8') as r:
        data = r.readlines()
        data = json.loads("".join(deepcopy(data)))
        return data

def calculate_all():
    data = open_file('../data/all_date.json')
    data_df = pd.DataFrame(data)
    data_df['c9'] = round(data_df['c9'] / 9, 2)
    data_df['985'] = round(data_df['p985'] / 20, 2)
    data_df['211'] = round(data_df['p211'] / 17, 2)
    data_df['top'] = round(data_df['top'] / 12, 2)
    data_df['basic'] = round(data_df['basic'] / 12, 2)
    data_df.to_csv("../data/result_json.csv")

def concat_df(first, second, type):
    first['value'] = 0
    second = pd.concat([first, second], axis=0)
    result = second.groupby(['name'])['value'].sum().reset_index()
    first[type] = result['value']

    return deepcopy(first)


if __name__ == '__main__':
    calculate_all()
