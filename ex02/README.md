# Assignment 2
## Requirements
To run the application, `openssl` should be installed (the cli tool).

Furthermore, `python-cryptography` must be installed. To prevent a mess on your machine you should use a virtual environment for python. The easiest way to set it up is to do the following:
```bash
cd ex02 && python -m venv . && source bin/activate && pip install -r requirements.txt
```
## Usage
The server should be started before the client. The server must be run like this:
```bash
server.py LISTEN_ADDRESS LISTEN_PORT CONNECTION_ADDRESS CONNECTION_PORT
```
where `LISTEN_ADDRESS`:`LISTEN_PORT` is where the server should listen for the client and `CONNECTION_ADDRESS`:`CONNECTION_PORT` is where the server should tunnel the traffic to.

The client is used like this:
```bash
client.py SERVER_ADDRESS SERVER_PORT LISTEN_ADDRESS LISTEN_PORT
```
where `SERVER_ADDRESS`:`SERVER_PORT` is where the server listens for the client and `LISTEN_ADDRESS`:`LISTEN_PORT` is where the client should should listen for connections.
## Demo
A short [asciinema](https://github.com/asciinema/asciinema) demo:
[![asciicast](https://asciinema.org/a/363289.svg)](https://asciinema.org/a/363289)
