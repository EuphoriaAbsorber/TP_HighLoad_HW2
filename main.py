from server import HttpServer
from config import parseConfig



if __name__ == '__main__':
    host, port, root, maxThreads, maxConns = parseConfig()
    server = HttpServer(host, port, root, maxThreads,  maxConns)
    server.listenAndServe()
    