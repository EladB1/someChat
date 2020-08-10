# SomeChat
* A small chat app for learning purposes

### Setup
* Have the following installed:
  * docker
  * docker-compose
  * python3
  * pwgen
    * Or you can create your own passwords and place them in the correct locations
* Run: 
  * `./secret_init.bash` _(non-root user)_
  * `docker-compose up -d` to run the full app _(root user)_
  * `docker exec -it db_flaskapp /docker-entrypoint-initdb.d/init_db.bash` _(root user)_
