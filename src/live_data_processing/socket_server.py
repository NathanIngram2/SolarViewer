# -*- coding: utf-8 -*-
"""
File: socket_server.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2024-03-30
Description: Recieve data from Raspberry Pi via socket, store as a pickle.


Copyright (C) 2023  Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import socket
import pickle
import matplotlib.pyplot as plt
import time


HOST = '192.168.1.2'
#HOST = 'localhost'
PORT = 65432

def socket_recieve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    data = []
    while True:
        d = conn.recv(1024)
        if not d:
            break
        data.append(d)
    data = b"".join(data)
    conn.close()
    return pickle.loads(data)

"""
print("Waiting until start message recieved")
recieved = socket_recieve()
while recieved["id"] != "s":
    recieved = socket_recieve()
print("Start recieved")
"""

while True:
    r = socket_recieve()
    print("Recieved packet with ID " + r["id"])
    if r["id"] == "b":
        break
    with open(f"./pickles/{time.time()}.pickle", 'wb') as handle:
        pickle.dump(r, handle)
    


