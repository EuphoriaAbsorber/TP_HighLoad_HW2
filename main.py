from server import HttpServer

HOST = '127.0.0.1'
PORT = 5500
ROOT = './'

if __name__ == '__main__':
    server = HttpServer(HOST, PORT, ROOT)
    server.listenAndServe()
    