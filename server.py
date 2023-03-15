import socket
from urllib.parse import urlparse
from urllib.parse import unquote
import mimetypes
import os

from datetime import datetime

import multiprocessing
import threading
import queue
import signal

class HttpRequest:
    def __init__(self, method, path, headers, body):
        self.method = method
        self.path = urlparse(path).path
        self.headers = headers
        self.body = body
    def print(self):
        print(self.method, self.path, self.headers, self.body)

class HttpResponse:
    def __init__(self, code, status, headers):
        self.code = code
        self.status = status
        self.headers = headers
    def print(self):
        print(self.code, self.status, self.headers, self.body)

class HttpServer:
    def __init__(self, host, port, rootDir, maxThreads, maxConns, maxCPUs):
        self.host = host
        self.port = port
        self.root = rootDir
        self.maxThreads = maxThreads
        self.maxConns = maxConns
        self.maxCPUs = maxCPUs
        self.taskQueue = queue.SimpleQueue()

    def threadWork(self):
        while True:
            conn = self.taskQueue.get()
            if conn:
                self.serveClient(conn)
                conn.close()

    def listenAndServe(self):
        print("Settings: ", self.host, self.port, self.root, self.maxThreads)
        print("Starting server...")
        
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # семейство протоколов 'Интернет' (INET), тип передачи данных 'потоковый' (TCP)
        cpu_count = min(multiprocessing.cpu_count(), self.maxCPUs)
        pids = []
        print("number of cpus", cpu_count)

        try:
            serv_sock.bind((self.host, self.port))
            serv_sock.listen()
            for _ in range(cpu_count):
                pid = os.fork()
                if pid != 0:
                    print('Новый процесс: ', pid)
                    pids.append(pid)
                    for _ in range(self.maxThreads):
                        t = threading.Thread(target=self.threadWork, daemon=True)
                        t.start()
                    pids.append(pid)
                    while True:
                        conn, _ = serv_sock.accept() # blocking
                        self.taskQueue.put(conn)
        except KeyboardInterrupt:
            serv_sock.close()
            for pid in pids:
                os.kill(pid, signal.SIGTERM)
            print("server has been stopped")
      
    def serveClient(self, conn):
        try:
            req = self.parseRequest(conn)
            resp, filePath = self.serveRequest(req)
            self.sendResponse(conn, resp)
            if type(req) == HttpRequest and req.method == 'GET' and filePath != "": # response body
                file = open(filePath, 'rb')
                conn.sendfile(file)
                file.close()
        except Exception as e:
            print("ERROR: ", e)

        if conn:
            conn.close()

    def parseRequest(self, conn):
        rawFile = conn.makefile('r')
        reqInfo = rawFile.readline().split()
        headers = [
                   ('Server', 'HW2-Server'),
                   ('Date', datetime.now()),
                   ('Connection', 'close')
                   ]     
        if len(reqInfo) != 3:
            return HttpResponse(403, 'Wrong path string', headers)
        method, path, _ = reqInfo
        if method != 'GET' and method != 'HEAD':
            return HttpResponse(405, 'Method Not Allowed', headers)
        if path.find('/../') != -1:
            return HttpResponse(403, 'Wrong path string', headers)
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

    def serveRequest(self, req):
        if (type(req) != HttpRequest):
            return req, ""
        headers = [
                   ('Server', 'HW2-Server'),
                   ('Date', datetime.now()),
                   ('Connection', 'close')
                   ]
        GettingIndexFile = False
        urlPath = unquote(req.path)
        filePath = self.root + urlPath
        if req.path[-1] == '/' and req.path.count('.') == 0:
            filePath = self.root + urlPath + 'index.html'
            GettingIndexFile = True
        try:
            file = open(filePath, 'rb')
        except:
            if GettingIndexFile:
                return HttpResponse(403, 'Forbidden', headers), ""
            else:
                return HttpResponse(404, 'Not Found', headers), ""

        contentType, _ = mimetypes.guess_type(filePath, strict=True)
        fileType = filePath.split('.')[-1]
        if fileType == "swf":
            contentType = "application/x-shockwave-flash"
        headers.insert(-1, ('Content-Type', contentType))
        headers.insert(-1, ('Content-Length', str(os.path.getsize(filePath))))
        file.close()
        return HttpResponse(200, 'OK', headers), filePath

    def sendResponse(self, conn, resp):
        ans = conn.makefile('w')
        ans.write(f'HTTP/1.1 {resp.code} {resp.status}\r\n')
        for (HName, HVal) in resp.headers:
            ans.write(f'{HName}: {HVal}\r\n')
        ans.write('\r\n')
        ans.close()
        return