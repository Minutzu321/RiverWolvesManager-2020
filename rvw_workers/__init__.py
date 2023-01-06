import os
from socket import *
from struct import unpack
import rvw_panopticon
import time

class ServerProtocol:
    def __init__(self):
        self.socket = None
        self.output_dir = '.'
        self.file_num = 1

    def listen(self, server_ip, server_port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((server_ip, server_port))
        self.socket.listen(1)

    def handle_packets(self):
        print('Packets handler started')
        try:
            while True:
                (connection, addr) = self.socket.accept()
                try:
                    bs = connection.recv(4)
                    cit = int.from_bytes(bs,byteorder='big')
                    print(cit)
                    rasp = connection.recv(cit)
                    # rvw_panopticon.feed_robot = rasp.decode("utf-8")
                finally:
                    connection.shutdown(SHUT_WR)
                    connection.close()
        finally:
            self.close()

    def handle_images(self):
        print("Image handler started")
        try:
            while True:
                (connection, addr) = self.socket.accept()
                try:
                    while True:
                        dk = ""
                        start = time.time()
                        cati = connection.recv(4)
                        cati = int.from_bytes(cati,byteorder='big')
                        if cati != 0:
                            print("atati: "+str(cati))
                            while len(dk) != cati:
                                rasp = connection.recv(cati)
                                dk += rasp.decode("utf-8")
                            rvw_panopticon.feed_robot = dk
                            print(len(rvw_panopticon.feed_robot))
                            stop=time.time()
                            print('timp: '+str(stop-start))
                except:
                    connection.shutdown(SHUT_WR)
                    connection.close()
                    print('closed')
        finally:
            self.close()

    def close(self):
        self.socket.close()
        self.socket = None