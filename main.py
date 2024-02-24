import socket
import json
import threading

# Definujte broadcast adresu a port
def udp_handshake():
    timeout=0
    answered = False
    broadcast_address = '<broadcast>'
    port = 9876

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sock.settimeout(5)

    sock.bind(('0.0.0.0', port))
    ip_address = socket.gethostbyname('')
    addresses = []
    handshake_addresses = []
    addresses.append(ip_address)

    message = {"command":"hello","peer_id":"sembera-peer1"}
    message_as_bytes = json.dumps(message).encode("utf-8")
    sock.sendto(message_as_bytes, (broadcast_address, port))
    print(message, "\n")

    while True:
        try:
            # dokoncit reseni, kdyz prijde udp handsake od nekoho ciziho
            data, address = sock.recvfrom(port)
            if address not in addresses and data == "ok":
                data = data.decode()
                print(data, "\n")
                threading.Thread(target=tcp_start, args=address).start()
                addresses.append(address)
                answered = True
            elif address not in addresses and data == "hello":
                handshake_addresses.append(address)
                message = {"status":"ok","peer_id":"sembera-peer1"}
                message_as_bytes = json.dumps(message).encode("utf-8")
                sock.sendto(message_as_bytes, (address, port))
            elif address in handshake_addresses:
                threading.Thread(target=tcp_history, args=address).start()

        except socket.timeout:
            timeout += 1
            if timeout > 5 and not answered:
                print("No response received within the timeout period.\n")
                sock.close()
                break




def tcp_start(address):
    tcp_handshake(address)

def tcp_handshake(address):
    pass

def tcp_history(address):
    pass

def send_message():
    pass


if __name__ == '__main__':
    udp_handshake()


