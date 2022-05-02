install docker-ce and docker compose
clone repo
docker stack init
add secrets:
printf "<pass_here>" | docker secret create pg_password -
printf "<tg_token_here>" | docker secret create telegram_token -
run:
docker stack deploy henlo --compose-file docker-compose.yml
build henlo web:
docker build . -t henlo_web:latest
create venv & collect static
migrate, create superuser if needed