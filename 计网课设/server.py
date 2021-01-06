import socket
import random
import time           

def server(port): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # host = socket.gethostname()
    # ip = socket.gethostbyname(host)
    s.bind(("127.0.0.1", port))
    while True:
        data,addr = s.recvfrom(1024)
        print(addr)
        s.sendto('welcome!'.encode('utf-8'), addr)
        time.sleep(0.01)
    s.close()

def main():
    port = random.randint(50000-1,50010)
    print(port)
    server(port)
        
if __name__ == "__main__":
    main()
    