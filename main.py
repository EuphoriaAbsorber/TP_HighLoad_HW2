from server import HTTPServer

HOST = '127.0.0.1'
PORT = 5500

if __name__ == '__main__':
    server = HTTPServer(HOST, PORT)
    server.ListenAndServe()
    