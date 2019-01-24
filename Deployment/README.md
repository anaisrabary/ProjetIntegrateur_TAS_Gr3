# Minio-Elasticsearch deployment with example images

## Getting started
Following these instructions you should be able to:
- deploy our infrastructure as docker services/containers
- stop & start existing services/containers without data loss
- re-deploy our infrastructure [useful for collaborators]

### Prerequisites
make sure you have docker and docker-compose installed  
https://docs.docker.com/install/linux/docker-ce/ubuntu/  
https://docs.docker.com/compose/install/

### Deploy infrastructure for the first time
Copy INSA_data_images/ into Deployment/  
From inside Deployment/ use the following commands:  
```bash
docker-compose pull
docker-compose up --build
```

### Stop & start
Stop services/containers while inside terminal on startup : Ctrl-C  
Stop services/containers from host, still inside Deployment/ :
```bash
docker-compose stop
```

Start existing & stopped services/containers
```bash
docker-compose start
```

### Re-deploy infrastructure (overwrite)
From inside Deployment/ use the following commands:  
```bash
docker-compose down --volumes
docker-compose up --build
```
The first command stops and deletes associated containers, deletes associated volumes  
The second command deploys services/containers and forces build even if the image already exists


## Minio

### About
Minio is an object-based storage server, best suited for storing unstructured data. It's light enough to be packaged in the application stack. It can be distributed.

### Using Python client
```bash
pip install minio
```
```python
#import
from minio import Minio  

#replace <> with appropriate values
minioClient = Minio('<minioHost>:<minioPort>', access_key=<accessKey>, secret_key=<secretKey>, secure=False)
minioClient.fput_object(<bucketName>, <objectName>, <file>)
```
The option secure=False tells Minio not to use a secure access (HTTPS protocol/SSL certificates) to the server. I'ts used for testing purpose given our project's context and it should not be used in a production environment.

## Elasticsearch 

### About
Elasticsearch is a scalable search and analytics engine. It can be distributed.

### Using Python client
```bash
pip install elasticsearch
```
```python
#import 
from elasticsearch import Elasticsearch  

#replace <> with appropriate values
es = Elasticsearch([{'host':<esHost>,'port':<esPort>}])
doc = {'image':'<minioHost>:<minioPort>/minio/'+<bucketName>+'/'+<objectName>, 'labels': <labelsArray>.tolist(), 'label':<labelString>}
es.index(index=<indexName>, doc_type=<type>, id=<id>, body=doc)
```

### Search examples
- get all links with label 'forest'  
navigator: http://localhost:9200/images/_search?q=label:forest&filter_path=hits.hits._source.image&size=50  
curl: 
```bash
curl -X GET "localhost:9200/images/_search?q=label:forest&filter_path=hits.hits._source.image&size=50"
```

