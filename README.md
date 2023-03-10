# Viva Challenge
The ACM-ICPC (International Collegiate Programming Contest) is an algorithmic programming contest for college students. Teams of three, representing their university, work to solve the world's most real-world problems, fostering collaboration, creativity, innovation, and the ability to perform under pressure.

The Rest API manages information related to participants of ACM-ICPC and their results. The API can:
Create/Update/Delete participants
Create/Update/Remove competing teams and add/remove team members.
Record the results of each competition for each of the teams in different instances.
Get the results of a year in general (sorted by instances and within each instance by score).
Get the results of a year in a given instance (sorted by score)

## Requirements
- Docker

## Running the application
Run the command
```bash
    docker-compose up -d --build
```
[Access the django admin panel here](http://localhost:8000/admin)
## Creating Django Admin
1. Find out the django container id "viva_web"
```bash
    docker ps -a
```
2. Enter the cointainer
```bash
    docker exec -ti "containerid" /bin/sh
```
3. Do the admin creation process
```bash
    python manage.py createsuperuser
```
4. Exit the container
```bash
    exit
```

## Running the tests
Some unit tests and integration tests were created to test Team and Participant functionalities. The tests are in the path src/challenge/test
1. Find out the django container id "viva_web"
```bash
    docker ps -a
```
2. Enter the cointainer
```bash
    docker exec -ti "containerid" /bin/sh
```
3. Do the admin creation process
```bash
    python manage.py test
```
4. Exit the container
```bash
    exit
```

## Interacting with the application
The application gonna runs on http://localhost:8000. To be able to fulfill the tasks previously mentioned some routes were defined. Below is the list of these routes their endpoints and their uses:

- http://localhost:8000/admin

    Every Django application has an admin endpoint with a pre-defined interface that the application admin can use to manage. 

- http://localhost:8000/participants
    - GET: Lists the participants in the database. No parameters required
    - POST: Creates a new participant. The request body must be a JSON with the keys: first_name, last_name, id_no, date_birth, gender, and country.

- http://localhost:8000/participants/<int: id>
    - GET: Show information about a participant with id received as a parameter.
    - PUT: Edit a participant with id received as a parameter. The request body must be a JSON with the keys: first_name, last_name, id_no, date_birth, gender, and country.
    - DELETE: delete a participant with id received as a parameter

- http://localhost:8000/teams
    - GET: Lists the teams in the database. No parameters required
    - POST: Creates a new team. The request body must be a JSON with the keys: name, representative_name, and country.

- http://localhost:8000/teams/<int: id>
    - GET: Show information about a team with id received as a parameter.
    - PUT: Edit a team with id received as a parameter. The request body must be a JSON with the keys: name, representative_name, and country.
    - DELETE: delete a team with id received as a parameter

- http://localhost:8000/teams/<int: team_id>/members/<int: participant_id>
    - PUT: Add a member with id received as a parameter into a team with id received as a parameter. No request body is required.
    - DELETE: removes a member from a team with id received as a parameter from a team with id received as a parameter

- http://localhost:8000/competitions
    - GET: Lists the competitions in the database. No parameters required
    - POST: Creates a new competition. The request body must be a JSON with the keys: instance_name, and year.

- http://localhost:8000/competitions/<int: id>
    - GET: Show information about competition with id received as a parameter.
    - DELETE: delete a competition with id received as a parameter

- http://localhost:8000/competitions/<int: id_competition>/results/<int: id_team>
    - POST: Create a log recording the result of a team in one competition. The request body must be a JSON with the key: scores

- http://localhost:8000/results/<int: year>
    - GET: Show results of a year received as a parameter sorted by instances and within each instance by score.

- http://localhost:8000/results/<int: year>/<str:instance>
    - GET: Show results of a year in a given instance received as a parameter sorted by score.

- http://localhost:8000/swagger

    You can use swagger to see the API Documentation
    ** The API that create a log recording the result of a team in one competition and the API that create a competition does not have the correct data in the swagger.

## Stopping and Removing Container Images
Run the command
```bash
    docker-compose down
```
