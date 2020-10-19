#!/usr/bin/env sh

echo "WAITING 5 SEC FOR DB TO RUN..."
sleep 5
python3 manage.py makemigrations api
echo "MIGRATION CREATED"
python3 manage.py migrate
echo "MIGRATION COMPLETED, LAUNCH SERVER."
python3 manage.py runserver 0:8000
