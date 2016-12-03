#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc

http_client = pyjsonrpc.HttpClient(
    url = "http://127.0.0.1:9090",
)
print http_client.call("add", 1, 2)
# Result: 3

# It is also possible to use the *method* name as *attribute* name.
print http_client.add(1, 2)
# Result: 3

# Notifications send messages to the server, without response.
http_client.notify("add", 3, 4)