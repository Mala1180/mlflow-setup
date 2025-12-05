docker exec -it mlflow-server sh -c "poetry run python mlflow/adduser.py"
docker exec -it minio bash /minio/add-user.sh