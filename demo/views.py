import struct

from django.shortcuts import render
from dwebsocket.decorators import accept_websocket,require_websocket
from django.http import HttpResponse
import time
import json
import pandas as pd
from demo.dataSource import DataSource
import random
from django.shortcuts import render
from django.http import JsonResponse
import redis
# Create your views here.
staus = ''
clients = []


def index(request):
    return render(request, 'index.html')

def index2(request):
    return render(request, 'index2.html')
# @accept_websocket
# def echo(request):
#     if request.is_websocket:#如果是webvsocket
#         lock = threading.RLock() #rlock线程锁
#         try:
#             lock.acquire()#抢占资源
#             clients.append(request.websocket)#把websocket加入到clients
#             print(clients)
#             for message in request.websocket:
#                 if not message:
#                     break
#                 for client in clients:
#                     client.send(message)
#         finally:
#             clients.remove(request.websocket)
#             lock.release()#释放锁

def modify_message(message):
    return message.lower()


# @accept_websocket
# def echo(request):
#     if not request.is_websocket():#判断是不是websocket连接
#         try:#如果是普通的http方法
#             message = request.GET['message']
#             return HttpResponse(message)
#         except:
#             return render(request,'index.html')
#     else:
#         for message in request.websocket:
#             request.websocket.send(message)#发送消息到客户端
#
@accept_websocket
def echo(request):
    if request.is_websocket():#判断是不是websocket连接
        for message in request.websocket:
            # while 1:
                sendNumber(request)
    else:
        try:#如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request,'index.html')

def sendNumber(request):
    # request.websocket.send(str(1111))
    df = pd.read_csv('../data/result-relation.csv')
    df.drop({'Unnamed: 0'}, axis=1, inplace=True)
    for i in range(len(df)):
        result = pd.DataFrame(df.iloc[i]).to_dict('dict')
        request.websocket.send(str(result[i]))  # 发送消息到客户端
        time.sleep(2)

def getSource(request):
    # text.dumps(list)
    data = {'name': '你爹'}  # 返回给客户端的数据
    if request.method == "POST":
        print(request.POST)  # 查看客户端发来的请求内容
        return JsonResponse(request.POST,safe=False)  # 通过 django内置的Json格式 丢给客户端数据


@require_websocket
def echo_once(request):
    message = request.websocket.wait()
    request.websocket.send(message)


@accept_websocket
def echo_relationship(request):
    if request.is_websocket():#判断是不是websocket连接
        for message in request.websocket:
            send_relation_message(request)  # 发送消息到客户端
    else:
        try:#如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request,'index.html')

def preprocess_data():
    # json_data = json.load('/Users/maicius/code/ShowQQ/data.json')
    with open('/Users/maicius/code/ShowQQ/final_data.json', 'r', encoding='utf-8') as r:
        data = json.load(r)
    data_df = pd.DataFrame(data)
    data_df = data_df.sort_values(by='date')
    return data_df


def send_relation_message(request):
    data_df = preprocess_data()
    date_list = data_df['date'].values

    for date in date_list:
        result = pd.DataFrame(data_df[data_df['date'] == date])
        friend_df = pd.DataFrame(result['friend_list'].values[0])
        if friend_df.shape != (0, 0):
            friend_df.columns = ['source_name', 'source_id','source_img', 'target_name', 'target_id', 'target_img']
            send_list = []
            for item in friend_df.values:
                send_data = dict(date=date, source_name=item[0],source_img=item[2], target_name=item[3], target_img=item[5])
                send_list.append(send_data)

            print(send_list)
            # request.websocket.send(json.dumps(send_list))  # 发送消息到客户端
            # time.sleep(0.6)

