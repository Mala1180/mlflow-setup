docker exec -it mlflow-server sh -c "poetry run python mlflow/updateuser.py"
docker exec -it minio bash /minio/update-user.sh