import socket
from urllib.parse import urlparse

class HttpRequest:
    def __init__(self, method, path, headers, body):
        self.method = method
        self.path = urlparse(path).path
        self.headers = headers
        self.body = body
    def print(self):
        print(self.method, self.path, self.headers, self.body)

class HTTPResponse:
    def __init__(self, code, status, headers=None, body=None):
        self.code = code
        self.status = status
        self.headers = headers
        self.body = body
    def print(self):
        print(self.code, self.status, self.headers, self.body)

class HTTPServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def listenAndServe(self):
        print("Starting server...")
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()

            while True:
                conn, client_addr = serv_sock.accept()
                print('Connected by', client_addr)
                self.serveClient(conn)

        except KeyboardInterrupt:
            serv_sock.close()
            print("server has been stopped")
      

    def serveClient(self, conn):
        if conn:
            conn.close()

    def serveClient(self, conn):
        try:
            print("try parse")
            req = self.parseRequest(conn)
            print("req parsed")
            print(req.method)
            req.print
        except Exception as e:
            print(e)
            pass

        if conn:
            conn.close()

    def parseRequest(self, conn):
        rawFile = conn.makefile('r')
        reqInfo = rawFile.readline().split()
        if len(reqInfo) != 3:
            return HTTPResponse(403, 'Wrong path string')
        method, path, _ = reqInfo
        if method != 'GET' and method != 'HEAD':
            return HTTPResponse(405, 'Method Not Allowed')
        headers = {}
        while True:
            str = rawFile.readline()
            if str in ('\n', '\r\n', ''):
                break
            Hlist = str.split(':')
            HName = Hlist[0]
            HVal = ''.join(Hlist[0:])
            headers[HName] = HVal
        rawFile.close()
        return HttpRequest(method, path, headers, None)