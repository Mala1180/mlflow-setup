#!/bin/sh

./mlflow/server/auth/replace-env-vars.sh

echo "✔ Generated auth config file"

# Execute the command passed as arguments (or default)
exec "$@"