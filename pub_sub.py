

import time
import json
import socket
import threading

from utils import message_callback

class PubSub:
    """
        A Publish-Subscribe class that mimics the MQTT protocol
    """

    PUBLISH_DELIMITER = '|^|'
    SUBSCRIBE_DELIMITER = '^||'
    UNSUBSCRIBE_DELIMITER = '||^'

    def __init__(self, host='127.0.0.1', port=8888):
        """
        :param host: name of the host on which the pub_sub_service is being run
                     Should be an IpV4 address
        :param port: the port number on which the pub_sub_service is running

        ###############################################################################
        ------------------------------- Future Update ---------------------------------
        :param self_aware: flag that determines whether or not the pub_sub will see the 
                           publishes it makes to topics it is subscribed to. 
                           If the self_aware flag is True, then it will see the publish,
                           else, it won't see the publish

        """

        self.conn = self.make_socket(host, port)
        self.topics = set()

        self.message_callback = message_callback
        
        self.listener_thread = threading.Thread(target=self.listener, daemon=True)
        self.listener_thread.start()


    @staticmethod
    def make_socket(host, port):
        """
        Helper function to effect socket onject creation.
        Other socket options should be added here

        """
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.connect((host, port))

        return sock


    def listener(self):
        """
        Background thread that listens for incoming messages 
        i.e messages that have been published to topics the
        pub_sub client is subscribed to.

        """

        while 1:
            recv_msg = self.conn.recv(1024)
            if recv_msg:
                self.message_callback(recv_msg)
        
        # Be nice on the CPU
        time.sleep(0.5)
        
        return


    def publish(self, topic, msg):
        """
        Function to effect publishing of messages
        
        :param topic: the topic to send the message to
        :param msg: the message to send on that topic.

        """
        
        msg = str(msg) if type(msg) in [int, str] else msg.decode() if type(msg) == bytes else None

        try:
            assert msg
        except AssertionError:
            raise Exception(f"Unsupported message of type {type(msg).__name__}")
        else:
            payload = str(topic) + self.__class__.PUBLISH_DELIMITER + msg
            payload = payload.encode()

            self.conn.sendall(payload)

        return


    def modify_subscription(self, topic, type_='subscribe'):
        
        delimiter = self.__class__.SUBSCRIBE_DELIMITER

        if type_ == 'unsubscribe':
            delimiter = self.__class__.UNSUBSCRIBE_DELIMITER
        
        if isinstance(topic, str):
            self.topics.add(topic)
            _ = topic + delimiter
            self.conn.sendall(_.encode())

        elif isinstance(topic, list):
            if not all(list(map(lambda i: isinstance(i, str), topic))):
                raise Exception("Topic names must be strings")

            for i in topic:
                self.topics.add(i)
                _ = i + delimiter
                self.conn.sendall(_.encode())            

        else:
            raise Exception("Subscriptions must be strings or a list of strings")

    def subscribe(self, topic):
        """
        Function to effect subscribing to topics
        
        :param topic: the name of the topic to subscribe to

        """

        self.modify_subscription(topic)



    def unsubscribe(self, topic):
        """
        Function to effect unsubscribing from topics
        
        :param topic: the name of the topic to unsubscribe from
        
        """

        self.modify_subscription(topic, type_='unsubscribe')



    def __repr__(self):
        """
        Convinience function that returns an API-like description
        of the instance.
        """        
        client = {
            'subscribed_topics': list(self.topics),
        }

        return json.dumps(client)
        



        
