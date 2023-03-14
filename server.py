import socket

class HTTPServer:
  def __init__(self, host, port):
    self._host = host
    self._port = port

  def ListenAndServe(self):
    print("Starting server...")
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

    try:
      serv_sock.bind((self._host, self._port))
      serv_sock.listen()

      while True:
        #conn, _ = serv_sock.accept()
        conn, client_addr = serv_sock.accept()
        print('Connected by', client_addr)
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
        self.serveClient(conn)

    except KeyboardInterrupt:
        serv_sock.close()
      

  def serveClient(self, conn):
    if conn:
      conn.close()
