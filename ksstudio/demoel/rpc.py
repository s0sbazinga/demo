#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc
import eldemo

global_medlink = eldemo.GlobalMedLink('./del-data/')
class RequestHandler(pyjsonrpc.HttpRequestHandler):

  @pyjsonrpc.rpcmethod
  def medlink(self, orig_file_path, ner_file_path):
      return global_medlink.med_link.mdel(orig_file_path,
                                          ner_file_path)


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('0.0.0.0', 9090),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
http_server.serve_forever()
