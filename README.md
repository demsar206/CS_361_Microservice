# Encryptor Microservice

This service receives a message and delivers back an encrypted message.

## Overview

Encryptor Service handles message encryption and decryption between the client and the microservice.

## Client Setup

- Set up a socket connection to the microservice.
- Use `socket.connect()` with the microservice's host and port.

## Sending a Request

1. Encode the request message into JSON.
2. Use `socket.send()` to send the encoded message to the microservice.

### See the microservice-demo for an example.

Here is a UNL sequence diagram:

![img.png](img.png)
