from server import HttpServer
from config import parseConfig



if __name__ == '__main__':
    host, port, root, max_threads = parseConfig()
    server = HttpServer(host, port, root, max_threads)
    server.listenAndServe()
    