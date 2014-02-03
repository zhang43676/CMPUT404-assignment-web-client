#!/usr/bin/env python
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        if not port:
            port = 80
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    def get_code(self, data):
        return int(data.split(' ',2)[1])

    def get_headers(self,data):
        return data.split("\r\n\r\n")[0]

    def get_body(self, data):
        return data.split('\r\n\r\n',2)[1]

    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        parseUrl = urlparse(url)
        s = self.connect(parseUrl.hostname, parseUrl.port)
        message = "GET %s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nConnection: close\r\n\r\n" % (parseUrl.path, parseUrl.hostname)
        s.send(message)
        response = self.recvall(s)
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPRequest(code, body)
    
    def POST(self, url, args=None):
        if (args != None):
            Postcontent = urllib.urlencode(args)
        else:
            Postcontent = ""
        Postcontent_length = len(Postcontent)        
        parseUrl = urlparse(url)
        s = self.connect(parseUrl.hostname, parseUrl.port)
        message = "POST %s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: %d\r\n\r\n%s\r\n" % (parseUrl.path, parseUrl.hostname, Postcontent_length, Postcontent)
        s.send(message)
        message = self.recvall(s)
        code = self.get_code(message)
        body = self.get_body(message)
        return HTTPRequest(code, body)

    def command(self, command, url, args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print ( command, sys.argv[1] )    