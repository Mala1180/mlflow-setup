import os

import pytest
from mlflow import MlflowClient
from mlflow.entities import Run, Experiment
from mlflow.server.auth.client import AuthServiceClient
from python_on_whales import DockerClient
from mlflow.server.auth.entities import ExperimentPermission
from tests.env import load_env_vars

load_env_vars()

users = [
    {"username": "user1", "password": "user1password"},
    {"username": "user2", "password": "user2password"},
]


@pytest.fixture(scope="session", autouse=True)
def deploy_stack():
    docker_client = DockerClient(compose_project_directory=os.getcwd())
    docker_client.compose.up(detach=True, build=True)
    yield
    docker_client.compose.down(volumes=True)


@pytest.fixture(scope="session")
def auth_client():
    return AuthServiceClient(os.environ["MLFLOW_TRACKING_URI"])


@pytest.fixture(scope="session")
def admin_mlflow_client():
    return MlflowClient(os.environ["MLFLOW_TRACKING_URI"])


@pytest.fixture(scope="session", autouse=True)
def mlflow_users(auth_client):
    auth_client.create_user(users[0]["username"], users[0]["password"])
    auth_client.create_user(users[1]["username"], users[1]["password"])


@pytest.fixture(scope="session")
def experiments(auth_client, admin_mlflow_client):
    exp1_id: str = admin_mlflow_client.create_experiment("experiment-user-1")
    exp2_id: str = admin_mlflow_client.create_experiment("experiment-user-2")
    ep1: ExperimentPermission = auth_client.create_experiment_permission(
        exp1_id, users[0]["username"], "READ"
    )
    ep2: ExperimentPermission = auth_client.create_experiment_permission(
        exp2_id, users[1]["username"], "EDIT"
    )
    return [ep1, ep2]


@pytest.fixture(scope="session")
def user_clients():
    client1 = MlflowClient(
        f"http://{users[0]['username']}:{users[0]['password']}@localhost:4000"
    )
    client2 = MlflowClient(
        f"http://{users[1]['username']}:{users[1]['password']}@localhost:4000"
    )
    return [client1, client2]


def test_user1_can_read_experiment(experiments, user_clients):
    client1, _ = user_clients
    ep1, _ = experiments
    exp1: Experiment = client1.get_experiment(ep1.experiment_id)
    assert exp1.experiment_id == ep1.experiment_id


def test_user1_cannot_create_run(experiments, user_clients):
    client1, _ = user_clients
    ep1, _ = experiments
    with pytest.raises(Exception):
        client1.create_run(ep1.experiment_id)


def test_user1_cannot_create_run_in_others_experiments(experiments, user_clients):
    client1, _ = user_clients
    _, ep2 = experiments
    with pytest.raises(Exception):
        client1.create_run(ep2.experiment_id)


def test_user2_can_create_runs(mlflow_users, experiments, user_clients):
    _, ep2 = experiments
    _, client2 = user_clients
    run: Run = client2.create_run(ep2.experiment_id)
    assert run.info.experiment_id == ep2.experiment_id


def test_user2_cannot_create_run_in_others_experiments(
    mlflow_users, experiments, user_clients
):
    _, client2 = user_clients
    ep1, _ = experiments
    with pytest.raises(Exception):
        client2.create_run(ep1.experiment_id)
