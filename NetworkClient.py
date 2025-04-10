import socket
import base64
from PIL import Image
import io
import config
import random as rd

class Move:
    def __init__(self, player, first, second):
        self.player = player
        self.first = first
        self.second = second

    def __str__(self):
        return f"{self.player}: {self.first} & {self.second}"

def connect_to_server(hostname, port, team_name, logo_path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))

    s.sendall(bytes([1]))  # Send version byte
    if s.recv(1)[0] != 1:
        raise Exception("Outdated server")

    with open(logo_path, "rb") as image_file:
        img = Image.open(image_file)
        img = img.resize((256, 256))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

    encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')

    s.sendall((team_name + "\n" + encoded_image + "\n").encode('utf-8'))

    info = s.recv(1)[0]
    player_number = info & 3
    time_limit = info // 4

    s.sendall(bytes([0]))
    s.recv(1)

    print(f"Player number: {player_number}, Time limit: {time_limit}")
    return s, player_number, time_limit

def send_move(s, move):
    """Sends a move as a sequence of bytes over a socket, preserving leading zeros."""
    #m = str(move.player) + str(move.first + 8) + str(mosecond + 8) 
    m = ((move.first))+(move.second+8)
    m_bytes = bytes([m])
    print(move, m, m_bytes)

    print(f"Sending bytes: {m_bytes}")
    s.sendall(m_bytes)


def receive_move(s):
    #201 --> dran
    #207 --> invalid
    #208 --> to late
    #needs manual int slicing

   
    player = s.recv(1)[0]
    print("receive_move:player -->",player)
    
    if player == 201: # Your Turn
        return True
    elif player == 207: # Invalid Turn
        return False
    elif player == 208: # Timed Out
        return False
    else:
        print(player)
        player_data = [int(str(player)[i]) for i in range(len(str(player)))]
        first = player_data[1]-8
        second = player_data[2]-8
        return Move(player_data[0], first, second)

# Example usage:
if __name__ == "__main__":
    conf = config.get_config()
    s, player_number, time_limit = connect_to_server(conf["server_host"], conf["server_port"], conf["team_name"], conf["logo_path"])
    #input()
    print("Start")
    while True:
        update = receive_move(s)
        match update:
            case True:
                print("Movin")
                send_move(s,Move(player_number,1,1))
                #input("Presskey to continue")
                send_move(s,Move(player_number,1,-1))
            case False:
                print("Error")
            case _:
                print("Other Moves")
                print(update)
