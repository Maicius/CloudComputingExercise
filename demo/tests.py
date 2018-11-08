import json
import pandas as pd
import redis

df = pd.read_table('D:\\Git\\CloudComputingExercise\\demo\\text\\relationship.txt', sep=",", header=None,
                       names=["source_name", "source_id", "target_name", "target_id"])
df.drop({'source_id','target_id'}, axis=1, inplace=True)
for i in range(len(df)):
    result = pd.DataFrame(df.iloc[i]).to_dict('dict')
    request.websocket.send(str(result[i]))  # 发送消息到客户端
    time.sleep(2)

# file = open('datatime.txt','w')
# file.write(str(pd.DataFrame(df['date']).to_dict('list')))
# print(df['985'].max)
print(result[0])
# print(len(df))
# print(df)
# result = df.to_dict('list')
# result = pd.DataFrame(df.iloc[0]).to_dict('dict')
# print(str(result[0]))
# print(text.dumps(result))
