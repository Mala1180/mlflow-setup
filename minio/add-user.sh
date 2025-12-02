#!/bin/bash

source .env
source .new-user.env

echo "New user to add: ${NEW_USER} ${NEW_USER_PASSWORD}"

mc alias set minioserver http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}

mc admin user add minioserver "$NEW_USER" "$NEW_USER_PASSWORD"
mc admin policy attach minioserver readwrite --user="$NEW_USER"
