#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# In routing.py
from channels.routing import route
from myapp.consumers import ws_message

channel_routing = [
    route("websocket.receive", ws_message),
]