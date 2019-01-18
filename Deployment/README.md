# Deployment

## Deployment
make sure you have docker and docker-compose installed  
https://docs.docker.com/install/linux/docker-ce/ubuntu/  
https://docs.docker.com/compose/install/

copy INSA_data_images/ into Deployment/  
from inside Deployment/ use the following commands:  
```bash
docker-compose pull
docker-compose up
```

## Useful docker-compose commands
stop services/containers
```bash
docker-compose stop
```

start existing services/containers
```bash
docker-compose start
```
or
```bash
docker-compose up
```

rebuild images while starting services/containers
```bash
docker-compose up --build
```

(stop services/containers and) remove services/containers
```bash
docker-compose down
```
