# Remote Control Web App

This is a Python Flask-based web application that allows users to control their computer remotely via a web interface. With this app, you can move the mouse, simulate key presses (like Tab, Backspace), control media in VLC, and send text input to the computer—all from a browser on your phone or any other device connected to the same local network.

## Features

- **Mouse Controls**: Move the mouse cursor using arrow buttons, simulate left and right clicks.
- **Keyboard Input**: Send text input to the computer, use Tab, Backspace, and Enter keys.
- **Media Controls**: Control VLC media player with play/pause, volume up/down, fast forward, and rewind functionality.
- **Backspace**: Erase the last character in a text input field.
- **Tab Button**: Simulate the Tab key press to move between input fields.
- **Web-based Interface**: Access the app using a browser on any device connected to the same network.

### Requirements
- Python 3.x
- Flask
- PyAutoGUI
- keyboard module
