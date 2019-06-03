# PubSub
A minimalist publish-subscribe protocol

## Requirements
- Python 3.6+

## Usage
- Start the PubSub service first by running ```pub_sub_service.py```. Don't forget to change the host-port tuple of the address to match your spec.

- Create a pub_sub client: 
  ```c = PubSub(host='localhost', port=8008)```

- Add a callback function to run whenever a message is received (The function should take only one argument -> the received message):
  
 ```
    def custom_callback(message):
        print(f"I, {message}, am the received message)
 ```
      c.message_callback = custom_callback

- Subscribe to a topic (or a list of topics):
  ```c.subscribe("foo")```;
  ```c.subscribe(["foo", "bar", "eggs"])```
  
- Unsubscribe from a topic or list of topics:
  ```c.unsubscribe("foo")```;
  ```c.unsubscribe(["foo", "bar", "eggs"])```
  
- Publish a message to a specific topic (currently, only bytes and strings are supported as messages):
  ```c.publish("spam", "I am a pub-sub message")```;
  ```c.publish("eggs", bytes.fromhex("7E04087E"))```

## Future Updates
- Wildcard Topic subscription (like the standard MQTT)
- Clean-up of non-active sockets on the main pub_sub_service(```.py```)
