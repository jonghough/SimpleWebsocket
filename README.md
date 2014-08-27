SimpleWebsocket
===============

An implementation of the Websocket protocol for clients in Python, made as simple as possible.
Written for Python 2.7.

TODOs
=====

Currently still very much under construction. The main outstanding issues are:
* Handle secure wss connections, including certificates;
* Cleanup initial header for making connections to servers other than websocket.org;
* Handle on_message, on_close, on_error etc. callbacks;
* Handle data;
* Check protocol conformity.
