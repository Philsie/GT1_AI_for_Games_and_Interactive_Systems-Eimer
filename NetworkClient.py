import socket
import base64
from PIL import Image
import io
import config
import random as rd

#%% Notes
"""
Ring numbers for moves:
    0(1(2(3(4)3)2)1)0
    0 is out of bounds
taken into account in send data to act like this:
    (0(1(2(3)2)1)0)

Moves encoded after testing:

        |Move        
Send    |From   |To     |Note
5       |3      |2      |Illegal (Server States -3 to -2)
6       |2      |1      |Works (Server States -2 to -1)
7       |1      |0      |Works (Server States -1 to 0)
8       |0      |1      |Works
9       |1      |2      |Works
10      |2      |3      |Works

"""
#%% Code
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

def send_move(s,start,end):
    """Sends a move as a sequence of bytes over a socket, preserving leading zeros."""    

    MoveLUT = [
    [None, 8   , None, None], # From 0
    [7   , None, 9   , None], # From 1
    [None, 6   , None, 10  ], # From 2
    [None, None, None, None]  # From 3
    ] 

    move = MoveLUT[start][end]
    if move != None:
        move_bytes = bytes([MoveLUT[start][end]])
        s.sendall(move_bytes)
        return True
    else:
        return False


def receive_move(s):
    #201 --> your turn
    #207 --> invalid
    #208 --> to late
    #else ... might follow example in send moves
    recieved = s.recv(1)[0]    
    
    if recieved == 201: # Your Turn
        return True
    elif recieved == 207: # Invalid Turn
        return False
    elif recieved == 208: # Timed Out
        return False
    else:
        return "Fallback"
        # WIP

# Example usage:
if __name__ == "__main__":
    print("\n"*25) # Temp console clear for testing
    conf = config.get_config()
    s, player_number, time_limit = connect_to_server(conf["server_host"], conf["server_port"], conf["team_name"], conf["logo_path"])
    #input()
    print("Start")
    while True:
        update = receive_move(s)
        match update:
            case True:
                print("Movin")
                send_move(s,1,2)
                send_move(s,2,3)
            case False:
                print("Error")
            case _:
                print("Other Moves")
                print(update)
