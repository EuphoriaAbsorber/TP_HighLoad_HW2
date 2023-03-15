from server import HttpServer
from config import parseConfig



if __name__ == '__main__':
    host, port, root, maxThreads, maxConns, maxCPUs = parseConfig()
    server = HttpServer(host, port, root, maxThreads,  maxConns, maxCPUs)
    server.listenAndServe()
    