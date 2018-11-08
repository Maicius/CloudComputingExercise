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
    df = pd.read_csv('D:\\Git\\CloudComputingExercise\\demo\\cvs\\resul.csv')
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

def send_relation_message(request):
    df = pd.read_table('D:\\Git\\CloudComputingExercise\\demo\\text\\relationship.txt', sep=",", header=None,
                       names=["source_name", "source_id", "target_name", "target_id"])
    df.drop({'source_id', 'target_id'}, axis=1, inplace=True)
    # result = pd.DataFrame(df.iloc[0]).to_dict('dict')
    # request.websocket.send(json.dumps(result[0]))
    for i in range(len(df)):
        result = pd.DataFrame(df.iloc[i]).to_dict('dict')
        request.websocket.send(json.dumps(result[i]))  # 发送消息到客户端
        time.sleep(2)