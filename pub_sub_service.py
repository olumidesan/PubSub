


import socket 
import threading
import time

from collections import defaultdict

# Honestly, random delimiters :P
PUBLISH_DELIMITER = '|^|'
SUBSCRIBE_DELIMITER = '^||'
UNSUBSCRIBE_DELIMITER = '||^'

subscriptions = defaultdict(set)

# Change this as per your spec
address = ('127.0.0.1', 8888)

def worker(client_socket, addr):
    """Worker thread where each connection from the pub_subs is run"""

    while True:
        data = client_socket.recv(1024)
        if data:
            data = data.decode()
            if data.endswith(SUBSCRIBE_DELIMITER):
                subscriptions[client_socket].add(data.strip(SUBSCRIBE_DELIMITER))
                continue
            
            elif data.endswith(UNSUBSCRIBE_DELIMITER):
                subscriptions[client_socket].remove(data.strip(UNSUBSCRIBE_DELIMITER))
                continue

            topic, message = data.split(PUBLISH_DELIMITER)
            for i,j in subscriptions.items():
                if topic in j:
                    i.sendall(message.encode())

        time.sleep(0.5)


def pub_sub():
    """Main PubSub Service"""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen()

    print('-'*50)
    print(f"PubSub Service started on {address}")
    print('-'*50)
    while 1:
        conn, addr = sock.accept()
        if conn:
            pub_sub_thread = threading.Thread(target=worker, args=(conn, addr))
            pub_sub_thread.start()

        # Again, be nice on the CPU.
        time.sleep(0.5)


if __name__ == "__main__":
    pub_sub()
