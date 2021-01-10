cp henlo.service /etc/systemd/system/henlo.service
docker-compose build
systemctl enable henlo.service
systemctl start henlo.service
