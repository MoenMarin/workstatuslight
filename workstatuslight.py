#!/usr/bin/env python3

from queue import Queue, Empty
import socket
import threading

import colorsys
import math
import time
import socket
from datetime import datetime
from unicornhatmini import UnicornHATMini

print(
    """Asbjørn's Work Status Light @ Moen Marin AS
Press Ctrl+C to exit!
"""
)


# address and port is arbitrary
def handle_msgs(msg_queue: Queue, host="127.0.0.1", port=60260):
    # create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        print("[+] Listening on {0}:{1}".format(host, port))
        sock.listen(5)
        # permit to access
        conn, addr = sock.accept()

        with conn as c:
            # display the current time
            time = datetime.now().ctime()
            print("[+] Connecting by {0}:{1} ({2})".format(addr[0], addr[1], time))

            while True:
                request = c.recv(4096)
                if not request:
                    print("[-] Not Received")
                    break
                incoming = request.decode("utf-8").strip()

                try:
                    msg_queue.put_nowait(incoming)
                except Empty:
                    print("unable to put to queue..")
                    continue

                print("[+] Received", repr(incoming))

                response = f"Bye bye: {incoming}\r\n"
                c.sendall(response.encode("utf-8"))
                print("[+] Sending to {0}:{1}".format(addr[0], addr[1]))


def main():
    q = Queue()
    tcp_server = threading.Thread(target=handle_msgs, args=(q, "0.0.0.0", 1111))
    tcp_server.start()

    unicornhatmini = UnicornHATMini()
    unicornhatmini.set_brightness(1.0)
    unicornhatmini.set_rotation(0)
    u_width, u_height = unicornhatmini.get_shape()

    # Generate a lookup table for 8-bit hue to RGB conversion
    hue_to_rgb = []

    for i in range(0, 360):
        hue_to_rgb.append(colorsys.hsv_to_rgb(i / 359.0, 1, 1))

    WORKING_STATUSES = {"busy": (255, 0, 0), "thinking": (255, 165, 0), "available": (0, 255, 0), "custom": (0, 0, 0), "pink": (255, 20, 147)}

    def set_working_status(status: str):
        if status not in WORKING_STATUSES:
            print(f"Fucktard - not a defined status! status={status}")
            return

        color_code = WORKING_STATUSES.get(status)
        for y in range(u_height):
            for x in range(u_width):
                r = color_code[0]
                g = color_code[1]
                b = color_code[2]
                unicornhatmini.set_pixel(x, y, r, g, b)

    try:
        while True:
            try:
                incoming_msg = q.get_nowait()
                set_working_status(incoming_msg)
            except Empty:
                pass

            unicornhatmini.show()
            time.sleep(1.0 / 60.0)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
