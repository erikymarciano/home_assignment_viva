if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

## Running migrations
python manage.py migrate

python manage.py loaddata instances
python manage.py loaddata initial_competitions
python manage.py loaddata initial_participants
python manage.py loaddata initial_teams

exec "$@"