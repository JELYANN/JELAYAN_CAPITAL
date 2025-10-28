#!/usr/bin/env bash
set -e

# wait-for-db (simple)
host="$DB_HOST"
port="${DB_PORT:-3306}"

echo "=> waiting for database at $host:$port ..."
while ! nc -z "$host" "$port"; do
  sleep 0.5
done
echo "=> database is up"

# Apply migrations and collectstatic (non-interactive)
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

# create superuser if env provided (optional)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "from django.contrib.auth import get_user_model; User=get_user_model(); \
  import os; \
  username=os.getenv('DJANGO_SUPERUSER_USERNAME'); \
  email=os.getenv('DJANGO_SUPERUSER_EMAIL',''); \
  password=os.getenv('DJANGO_SUPERUSER_PASSWORD'); \
  User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password)" \
  | python manage.py shell || true
fi

exec "$@"
