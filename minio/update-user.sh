#!/bin/bash

source config/.user.env

echo "Updating user: ${NEW_USER}"

mc alias set minioserver http://minio:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"

# Update existing user's credentials
mc admin user disable minioserver "$NEW_USER"
mc admin user add minioserver "$NEW_USER" "$NEW_USER_PASSWORD"
mc admin user enable minioserver "$NEW_USER"

echo "User '${NEW_USER}' password updated successfully."