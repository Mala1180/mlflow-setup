#!/bin/bash
# Configure MinIO Client

source .env

echo ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}

mc alias set minioserver http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}

# Create the MLFlow bucket
mc mb --ignore-existing "minioserver/${MINIO_MLFLOW_BUCKET}"

# Loop through all USER_* variables that are NOT *_PASSWORD
for var in $(compgen -A variable); do

    case "$var" in
        USER_*) ;;                         # matches variables beginning with USER_
        *) continue ;;                     # skip others
    esac

    case "$var" in
        *_PASSWORD) continue ;;            # skip password variables
    esac

    identifier="${var#USER_}"
    username="${!var}"

    pass_var="USER_${identifier}_PASSWORD"
    password="${!pass_var}"

    if [ -z "$username" ] || [ -z "$password" ]; then
        echo "Skipping $var — missing username or password"
        continue
    fi

    mc admin user add minioserver "$username" "$password"
    mc admin policy attach minioserver readwrite --user="$username"

done