import json
import pandas as pd

def preprocess_data():
    # json_data = json.load('/Users/maicius/code/ShowQQ/data.json')
    with open('/Users/maicius/code/ShowQQ/data.json', 'r', encoding='utf-8') as r:
        data = json.load(r)
    data_df = pd.DataFrame(data)
    data_df = data_df.sort_values(by='date')
    date_list = data_df['date'].values

    for date in date_list:
        result = pd.DataFrame(data_df[data_df['date'] == date])
        friend_df = pd.DataFrame(result['friend_list'].values[0])
        if friend_df.shape != (0, 0):
            friend_df.columns = ['source_name', 'source_id', 'target_name', 'target_id']
            friend_df.drop(['source_id', 'target_id'], inplace=True, axis=1)
            for item in friend_df.values:
                send_data = dict(source_name=item[0], target_name=item[1])
                print(json.dumps(send_data))
            # print(friend_df.shape)
    return data_df

if __name__ == "__main__":
    preprocess_data()