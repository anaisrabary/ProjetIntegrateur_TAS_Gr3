# Deployment

## Deployment
make sure you have docker and docker-compose installed  
https://docs.docker.com/install/linux/docker-ce/ubuntu/  
https://docs.docker.com/compose/install/

copy INSA_data_images/ into Deployment/  
from inside Deployment/ use the following commands:  
```bash
docker-compose pull
docker-compose up --build
```

## Get unlabelled images
with curl
```bash
curl -X GET "localhost:9200/images/_search" -H 'Content-Type: application/json' -d'
{
  "query": { 
    "bool": { 
      "must_not": [
        {"exists":{"field":"labels"}}
      ]
    }
  }
}
'
```
in a python script
```python
from elasticsearch import Elasticsearch  
es = Elasticsearch([{'host':<host>,'port':<port>}])
es.search(index='images',body='{"query": {"bool": {"must_not": [{ "exists": { "field": "labels" }}]}}}')
```

## Useful docker commands
display images
```bash
docker images
```

remove an image
```bash
docker rmi <image-id>
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

rebuild images while starting services/containers
```bash
docker-compose up --build
```

(stop services/containers and) remove services/containers and attached volumes
```bash
docker-compose down --volumes
```

## Minio client for python
```bash
pip install minio
```
```python
#Imports  
from minio import Minio  

#in general
minioClient = Minio('<host>:<port>', access_key=<accesskey>, secret_key=<secretkey>, secure=<boolean>)
minioClient.fput_object(<bucketname>, <objectname>, <file>)
```

## Elasticsearch client for python
```bash
pip install elasticsearch
```
```python
#Imports  
from elasticsearch import Elasticsearch  

#in general
es = Elasticsearch([{'host':<host>,'port':<port>}])
doc = {'image':'<hostname>:<portname>/minio/'+<bucketName>+'/'+<objectname>, 'labels': <npyarray>[<i>].tolist()}
es.index(index=<indexName>, doc_type=<type>, id=<i>, body=doc)
minioClient.fput_object(<bucketname>, <objectname>, <file>)
```



