import socket

HOST = 'localhost'
PORT = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    request = b"HEAD /httptest/dir2/ HTTP/1.1\r\n\r\n"
    # request = b"GET /test.txt HTTP/1.1\r\nHost: wiki.com\r\n\r\n"
    s.sendall(request)
    while True:
        data = s.recv(1024)
        if data:
            print(f"Received {data}")
        else:
            break
