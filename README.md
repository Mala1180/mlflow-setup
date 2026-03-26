# MLflow Tracking Server Setup

This repository provides a containerized setup for MLflow, an open-source platform enabling MLOps and LLMOps workflows.

Mlflow uses two types of storage backends:

1. _Backend Store_: A database to store experiment and run metadata.

    - MySQL, MSSQL, SQLite and PostgreSQL.

2. _Artifact Store_: A location to store artifacts like models, plots, and data files.
    - Local filesystem, Amazon S3 and S3-compatible storage, Azure Blob Storage, Google Cloud Storage, FTP and SFTP
      Server, NFS and HDFS.

In this setup, we use **PostgreSQL** as the backend store and **MinIO** (an S3-compatible object storage) as the
artifact store.

## Prerequisites

- For MLflow Server
    - Docker
    - Docker Compose

- For MLflow Client
    - Python 3.9+
    - MLflow Python package

## Starting the MLflow Server

- Create a `.env` file in the root directory based on the provided `.server.env` file and customize the environment
  variables as needed.
    ```bash
    cp .env.server .env
    ```
- Start the services using Docker Compose:
    ```bash
    docker compose up -d
    ```

- Access the MLflow UI at [http://localhost:4000](http://localhost:4000) or MinIO UI
  at [http://localhost:9000](http://localhost:9000)

## Client Usage

1. Set the following environment variables in your client environment:

    ```bash
    # to use mlflow api
    MLFLOW_TRACKING_URI=http://127.0.0.1:4000
    MLFLOW_TRACKING_USERNAME=admin
    MLFLOW_TRACKING_PASSWORD=adminpassword

    # to save artifacts to minio storage
    MLFLOW_S3_ENDPOINT_URL=http://127.0.0.1:9000
    AWS_ACCESS_KEY_ID=john
    AWS_SECRET_ACCESS_KEY=johnpassword123
    ```
2. Use the following sample code check that everything is working correctly:

    ```python
    import mlflow
    from sklearn import datasets
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    # Experiment name of the experiment you have access to
    mlflow.set_experiment("experiment-1")

    X, y = datasets.load_iris(return_X_y=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    params = {
        "solver": "lbfgs",
        "max_iter": 1000,
        "random_state": 8888,
    }

    # Enable autologging for scikit-learn
    mlflow.sklearn.autolog()

    # Just train the model normally
    lr = LogisticRegression(**params)
    lr.fit(X_train, y_train)
    ```

## Server Configuration

### Managing Users

Create a `.user.env` file inside a `config` folder, based on the provided `config/.user.example.env` template:

```bash
cp config/.user.example.env config/.user.env
```

> For both adding and updating users, the scripts will read from this `.user.env` file.

- For adding new users
    ```bash
    ./config/add-user.sh
    ```

- For updating existing users
    ```bash
    ./config/update-user.sh
    ```

## License

This project is licensed under the MIT License.

## References

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MinIO Documentation](https://docs.min.io/)
