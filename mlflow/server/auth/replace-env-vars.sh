#!/bin/sh

INPUT="mlflow/server/auth/basic_auth_template.ini"
OUTPUT="mlflow/server/auth/basic_auth.ini"

# Create or overwrite the output file
sed \
    -e "s|__POSTGRES_USER__|${POSTGRES_USER}|g" \
    -e "s|__POSTGRES_PASSWORD__|${POSTGRES_PASSWORD}|g" \
    -e "s|__POSTGRES_CONTAINER__|${POSTGRES_CONTAINER}|g" \
    -e "s|__POSTGRES_PORT__|${POSTGRES_PORT}|g" \
    -e "s|__POSTGRES_DB__|${POSTGRES_DB}|g" \
    -e "s|__MLFLOW_ADMIN_USER__|${MLFLOW_ADMIN_USER}|g" \
    -e "s|__MLFLOW_ADMIN_PASSWORD__|${MLFLOW_ADMIN_PASSWORD}|g" \
    "$INPUT" > "$OUTPUT"