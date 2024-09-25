from flask import Flask, render_template, request, jsonify
import vlc
import pyautogui  # Importing pyautogui for mouse control
import keyboard    # Importing keyboard to send key commands
import socket
import threading

# DNS server to resolve remote.local to 127.0.0.1
def handle_dns_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 53))  # Bind to localhost on port 53

    print("DNS Server running...")

    while True:
        data, addr = sock.recvfrom(512)  # Receive DNS request
        print("Received DNS request from", addr)

        # Create a DNS response with remote.local resolved to 127.0.0.1
        response = bytearray(data)
        response[2] = 0x81  # Set response flag
        response[3] = 0x80  # Set response flag
        response[7] = 1  # Set number of answers to 1

        # Add the answer section (remote.local -> 127.0.0.1)
        response.extend(data[12:])  # Copy the question section
        response.extend(b'\xc0\x0c')  # Pointer to the domain name
        response.extend(b'\x00\x01')  # Type A
        response.extend(b'\x00\x01')  # Class IN
        response.extend(b'\x00\x00\x00\x3c')  # TTL 60 seconds
        response.extend(b'\x00\x04')  # Data length
        response.extend(b'\x7f\x00\x00\x01')  # 127.0.0.1

        sock.sendto(response, addr)  # Send response back to client

def run_dns_server():
    thread = threading.Thread(target=handle_dns_request)
    thread.daemon = True
    thread.start()

# Initialize Flask app
app = Flask(__name__)
media_player = vlc.MediaPlayer()  # Create VLC media player instance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    action = request.json.get('action')

    # VLC Controls using keyboard shortcuts
    if action == "play_pause":
        keyboard.press_and_release('space')  # Play/Pause
    elif action == "volume_up":
        keyboard.press_and_release('up')  # Volume Up
    elif action == "volume_down":
        keyboard.press_and_release('down')  # Volume Down
    elif action == "fast_forward":
        keyboard.press_and_release('right')  # Fast Forward
    elif action == "rewind":
        keyboard.press_and_release('left')  # Rewind
    elif action == "left_click":
        pyautogui.click()  # Left mouse click
    elif action == "right_click":
        pyautogui.rightClick()  # Right mouse click
    elif action == "move":
        x_offset = request.json.get('x_offset', 0)
        y_offset = request.json.get('y_offset', 0)
        move_cursor(x_offset, y_offset)  # Move cursor according to the offset
    elif action == "send_text":
        text = request.json.get('text')
        pyautogui.typewrite(text)  # Simulate typing the text
    elif action == "clear_text":
        keyboard.press_and_release('backspace')  # Delete last character
    elif action == "tab":
        keyboard.press_and_release('tab')  # Simulate Tab key press

    return jsonify({"status": "success"})

# Function to move cursor
def move_cursor(x_offset, y_offset):
    x, y = pyautogui.position()  # Get current cursor position
    pyautogui.moveTo(x + x_offset, y + y_offset)  # Move cursor

if __name__ == '__main__':
    run_dns_server()  # Start the DNS server
    app.run(host='0.0.0.0', port=5000)  # Start the Flask app
