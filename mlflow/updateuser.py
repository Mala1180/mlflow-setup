import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from mlflow import MlflowClient
from mlflow.entities import Experiment
from mlflow.server.auth.client import AuthServiceClient
from mlflow.server.auth.entities import ExperimentPermission

user_env_path = Path(os.getcwd()) / "config" / ".user.env"
env_path = Path(os.getcwd()) / ".env"

load_dotenv(env_path, override=False)
load_dotenv(user_env_path, override=True)

user = {
    "username": os.environ["NEW_USER"],
    "password": os.environ["NEW_USER_PASSWORD"],
    "experiment": os.environ["NEW_USER_EXPERIMENT"],
    "permission": os.environ["NEW_USER_PERMISSION"],
}

print(f"Updating user {user['username']}")

auth_client = AuthServiceClient(os.environ["MLFLOW_TRACKING_URI"])
admin_mlflow_client = MlflowClient(os.environ["MLFLOW_TRACKING_URI"])

auth_client.update_user_password(user["username"], user["password"])

exp: Optional[Experiment] = admin_mlflow_client.get_experiment_by_name(user["experiment"])
if exp is None:
    exp_id: str = admin_mlflow_client.create_experiment(user["experiment"])
    ep: ExperimentPermission = auth_client.create_experiment_permission(
        exp_id, user["username"], user["permission"]
    )
    print(
        f"User '{user['username']}' updated with new experiment '{user['experiment']}' and '{user['permission']}' permission"
    )
else:
    auth_client.update_experiment_permission(
        exp.experiment_id, user["username"], user["permission"]
    )
    print(
        f"User '{user['username']}' updated with '{user['permission']}' permission on experiment '{user['experiment']}'"
    )
