DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 5500
DEFAULT_ROOT = '.'
DEFAULT_MAX_THREADS = 256


def parseConfig():
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    root = DEFAULT_ROOT
    max_threads = DEFAULT_MAX_THREADS

    try:
        file = open('etc/httpd.conf', 'r')
    except:
        return host, port, root, max_threads
    while True:
        str = file.readline()
        if str in ('\n', '\r\n', ''):
            break
        key, val = str.split()
        if key == 'document_root':
            root = val
        elif key == 'thread_limit':
            max_threads = int(val)
        elif key == 'host':
            port = val
        elif key == 'port':
            port = int(val)

    return host, port, root, max_threads