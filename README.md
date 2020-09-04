# pybug

JIRA-style bug tracker in Django

### Set up:
Clone the repo
```console
$ git clone https://github.com/lseab/pybug
$ cd pybug
```
Create a new virtual environment
```console
$ virtualenv --python=python3.7 pybug
```
Activate it
```console
$ source pybug/bin/activate
```
Set up environment variables
```
# app_[dev/prod].env

DEBUG=<DEBUG>
DB_HOST=<DB_HOST>
DB_NAME=<DB_NAME>
DB_USER=<DB_USER>
DB_PASSWORD=<DB_PASSWORD>


# db_[dev/prod]
POSTGRES_DB=<POSTGRES_DB>
POSTGRES_USER=<POSTGRES_USER>
POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
```
Build and run the docker images.
```console
$ docker-compose up # Dev 
$ docker-compose -f docker-compose-deploy.yml up # Prod
```
Prepare database.
```console
$ docker-compose run app /scripts/prepare_db.sh # Dev 
$ docker-compose -f docker-compose-deploy.yml run app /scripts/prepare_db.sh # Prod
```
