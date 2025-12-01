import os
from pathlib import Path

from dotenv import load_dotenv

client_env_path = Path(os.getcwd()) / ".client.env"
server_env_path = Path(os.getcwd()) / ".server.env"


def load_env_vars():
    load_dotenv(client_env_path, override=False)
    load_dotenv(server_env_path, override=False)
