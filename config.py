# config.py

import os

SERVER_HOST = os.environ.get("SERVER_HOST", "localhost")
SERVER_PORT = int(os.environ.get("SERVER_PORT", 22135))
TEAM_NAME = os.environ.get("TEAM_NAME", "MyDefaultTeam3")
LOGO_PATH = os.environ.get("LOGO_PATH", "Logo.png")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

def get_config():
    return {
        "server_host": SERVER_HOST,
        "server_port": SERVER_PORT,
        "team_name": TEAM_NAME,
        "logo_path": LOGO_PATH,
        "debug": DEBUG,
    }

if __name__ == "__main__":
    print(get_config())