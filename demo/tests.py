import json
import pandas as pd
import redis

df=pd.read_csv('./cvs/result.csv')
df.drop({'Unnamed: 0'}, axis=1, inplace=True)
# file = open('datatime.txt','w')
# file.write(str(pd.DataFrame(df['name']).to_dict('list')))
print(df['985'].max)
# print(df)
# print(len(df))
# print(df)
# result = df.to_dict('list')
# result = pd.DataFrame(df.iloc[0]).to_dict('dict')
# print(str(result[0]))
# print(json.dumps(result))
