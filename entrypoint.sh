if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

## Running migrations
python manage.py makemigrations
python manage.py migrate

## Running fixtures
python manage.py loaddata instances.json
python manage.py loaddata initial_competitions.json
python manage.py loaddata initial_participants.json
python manage.py loaddata initial_teams.json

## Running the application server
python manage.py runserver 0.0.0.0:8000