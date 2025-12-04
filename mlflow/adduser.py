import os
from pathlib import Path

from dotenv import load_dotenv
from mlflow import MlflowClient
from mlflow.server.auth.client import AuthServiceClient
from mlflow.server.auth.entities import ExperimentPermission

new_user_env_path = Path(os.getcwd()) / "config" / ".new-user.env"
env_path = Path(os.getcwd()) / ".env"

load_dotenv(env_path, override=False)
load_dotenv(new_user_env_path, override=False)

user = {
    "username": os.environ["NEW_USER"],
    "password": os.environ["NEW_USER_PASSWORD"],
    "experiment": os.environ["NEW_USER_EXPERIMENT"],
    "permission": os.environ["NEW_USER_PERMISSION"],
}

print(f"Adding user {user['username']}")

auth_client = AuthServiceClient(os.environ["MLFLOW_TRACKING_URI"])
admin_mlflow_client = MlflowClient(os.environ["MLFLOW_TRACKING_URI"])

auth_client.create_user(user["username"], user["password"])
exp_id: str = admin_mlflow_client.create_experiment(user["experiment"])
ep: ExperimentPermission = auth_client.create_experiment_permission(
    exp_id, user["username"], user["permission"]
)

print(
    f"User '{user['username']}' added with '{user['permission']}' permission on experiment '{user['experiment']}'"
)
