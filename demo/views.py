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
import random

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

def get_send_data():
    df = pd.read_csv('/Users/maicius/code/ShowQQ/data/result_json.csv')
    df.drop({'Unnamed: 0'}, axis=1, inplace=True)
    result = pd.DataFrame(df.iloc[0]).to_dict('dict')
    return result

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
            sendNumber(request)
    else:
        try:#如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request,'index.html')

def sendNumber(request):
    while(1):
        data = get_send_data()
        if len(data) > 0:
            request.websocket.send(str(data))  # 发送消息到客户端

def getSource(request):
    # json.dumps(list)
    data = {'name': 'test'}  # 返回给客户端的数据
    if request.method == "POST":
        print(request.POST)  # 查看客户端发来的请求内容
        return JsonResponse(request.POST,safe=False)  # 通过 django内置的Json格式 丢给客户端数据


@require_websocket
def echo_once(request):
    message = request.websocket.wait()
    request.websocket.send(message)