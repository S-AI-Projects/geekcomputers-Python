import socket


def date_timeclient(host=None, port=2905, socket_factory=None):
    """
    Connect to a date-time server and receive current server time.

    Contract:
      Preconditions:
        - Line 3: `soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)` socket initialization.
        - Line 4: `soc.connect((host, 2905))` connects to date-time service port 2905.
        - Line 5: `recmsg = soc.recv(1024)` receives up to 1024 bytes.
        - Line 6: `soc.close()` releases network socket resources.
        - Line 7: `recmsg.decode("ascii")` decodes ASCII byte payload.
      Returns:
        - Formatted time message: "The time got from the server is %s" % decoded_time
    """
    if host is None:
        host = socket.gethostname()

    soc = socket_factory() if socket_factory is not None else socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.connect((host, port))
        recmsg = soc.recv(1024)
    finally:
        soc.close()

    formatted = "The time got from the server is %s" % recmsg.decode("ascii")
    print(formatted)
    return formatted


def main():
    date_timeclient()


if __name__ == "__main__":
    main()
