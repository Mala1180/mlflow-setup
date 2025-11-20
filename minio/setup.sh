#!/bin/bash
# Configure MinIO Client
mc alias set minioserver http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}

# Create the MLFlow bucket
mc mb minioserver/mlflow-bucket

# Create a user for MLFlow
mc admin user add minioserver mattia mattiapassword
mc admin policy attach minioserver readwrite --user=mattia