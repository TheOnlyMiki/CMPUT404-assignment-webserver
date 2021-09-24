#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

import os.path

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode( 'utf-8' ).split()
        
        respond_list = { 200: 'HTTP/1.1 200 OK\r\n',
                         404: 'HTTP/1.1 404 Not Found\r\n',
                         405: 'HTTP/1.1 405 Method Not Allowed\r\n',
                         302: 'HTTP/1.1 302 Found\r\n' }

        respond_type = 200
        path = 'www' + self.data[ 1 ]

        # If not GET command, then all respond 405 code.
        if self.data[ 0 ] != 'GET':
            respond_type = 405
        # If there has .. include the path, it was redirection to other path, don't deal with it, just respond 404 code.
        elif '..' in self.data[ 1 ]:
            respond_type = 404
        # Then check the path is valid or not.
        else:
            # If the path is vaild, and if endwith /, adding index.html to it. 
            if path[ -1 ] == '/' and os.path.isdir( path ):
                path += 'index.html'
            # If the path is direction but without /, like ../deep without / (../deep/index.html)
            elif os.path.isdir( path + '/' ):
                respond_type = 302
            # If the file is invaild, like not find or not exist
            elif os.path.isfile( path ) == False:
                respond_type = 404

        # If the respond still 200 OK, then is pass
        if respond_type == 200:
            context = ""
            file = open( path, 'r' )
            for line in file:
                context += line

            # Get the text type of the file. which is the end name of that file.
            text_type = path.split( '/' )[ -1 ].split( '.' )[ -1 ]
            # Modify the respond message for the request (Headed and include the file context of html or css).
            respond_list[ 200 ] += 'Content-Type: text/' + text_type + '; charset=utf-8\r\n\r\n' + context

        # Respond the request.
        self.request.sendall( bytearray( respond_list[ respond_type ], 'utf-8' ) )

        return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
