"""Date-Time Server (date-timeserver.py).

Listens on TCP port 2905 and responds to client connections with the current
formatted system date and time followed by CRLF.

Contract & Preconditions:
    - Precondition Source Line 24: `soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
      creates a TCP socket.
    - Precondition Source Line 25: `soc.bind((socket.gethostname(), 2905))` binds to port 2905.
    - Precondition Source Line 26: `soc.listen(5)` listens with a backlog queue of 5.
    - Precondition Source Line 28: `clientsocket, addr = soc.accept()` accepts incoming connection.
    - Precondition Source Line 31: `currentTime = time.ctime(time.time()) + "\r\n"` creates formatted time.
    - Precondition Source Line 32: `clientsocket.send(currentTime.encode("ascii"))` transmits ASCII bytes.
    - Precondition Source Line 33: `clientsocket.close()` closes connection.

Representative Result:
    Input: Controlled timestamp 1700000000.0 (UTC: 2023-11-15 03:43:20)
    Operation: `time.ctime(1700000000.0) + "\r\n"` encoded to ASCII.
    Expected Output: `time.ctime(1700000000.0).encode("ascii") + b"\r\n"`
    Example (UTC): b"Wed Nov 15 03:43:20 2023\r\n"
"""

import socket
import time

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((socket.gethostname(), 2905))
soc.listen(5)
while True:
    clientsocket, addr = soc.accept()

    print("estavlishes  a connection from %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    clientsocket.send(currentTime.encode("ascii"))
    clientsocket.close()
