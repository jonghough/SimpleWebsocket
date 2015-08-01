SimpleWebsocket
===============

A minimal Python Websocket client.

The purpose is to create a minimal, easy to read, easy to use Python-based websocket client. Essentially still a work in progress but works for most purposes.

TODOs
=====

Currently still very much under construction. The main outstanding issues are:
* Handle secure wss connections, including certificates;
* Cleanup initial header for making connections to servers other than websocket.org;
* Handle on_message, on_close, on_error etc. callbacks;
* Handle data;
* Check protocol conformity.
