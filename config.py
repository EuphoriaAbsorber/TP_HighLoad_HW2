DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8080
DEFAULT_ROOT = '.'
DEFAULT_MAX_THREADS = 256
DEFAULT_MAX_CONNECTIONS = 100


def parseConfig():
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    root = DEFAULT_ROOT
    maxThreads = DEFAULT_MAX_THREADS
    maxConns = DEFAULT_MAX_CONNECTIONS
    try:
        file = open('etc/httpd.conf', 'r')
    except:
        return host, port, root, maxThreads, maxConns
    while True:
        str = file.readline()
        if str in ('\n', '\r\n', ''):
            break
        key, val = str.split()
        if key == 'document_root':
            root = val
        elif key == 'thread_limit':
            maxThreads = int(val)
        elif key == 'host':
            port = val
        elif key == 'port':
            port = int(val)

    return host, port, root, maxThreads, maxConns