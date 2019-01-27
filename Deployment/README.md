# Minio-Elasticsearch deployment with example images

## Getting started
Following these instructions you should be able to:
- deploy our infrastructure as docker services/containers
- use our infrastructure
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
docker-compose up
```
### Use infrastructure
#### Stop & start
Stop services/containers while inside terminal on startup : Ctrl-C  
Stop services/containers from host, still inside Deployment/ :
```bash
docker-compose stop
```

Start existing & stopped services/containers
```bash
docker-compose start
```
#### Down & up
Stop services/containers, remove containers and network :
```bash
docker-compose down
```

Create services/containers and attach their existing volumes:
```bash
docker-compose up
```

### Re-deploy infrastructure (overwrite)  [useful for collaborators]
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

### Minio instances
There are 4 Minio instances accessible from port 9001 to 9004 on localhost.

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
The option secure=False tells Minio not to use a secure access (HTTPS protocol/SSL certificates) to the server. It's used for testing purpose given our project's context and it should not be used in a production environment.

## Elasticsearch 

### About
Elasticsearch is a scalable search and analytics engine. It can be distributed.

### Elasticsearch nodes
There are 3 elasticsearch nodes. 2 data nodes and 3 master-eligible nodes. We chose this infrastructure to avoid the split-brain while maintaining high availability, the cluster can go on if it loses 1 node. (for more detail, refer to this article: https://qbox.io/blog/split-brain-problem-elasticsearch)  
The first node is accessible on port 9200 on localhost.
To access other nodes: 
- List docker networks
```bash
docker network ls
```
- Look for our infrastructure network, it should be something like deployment_default.  
Find services/containers IP addresses
```bash
docker network inspect <network>
```
- Look for IPv4Address field for elasticsearch2, elasticsearch3 services/containers

You can now access other nodes on port 9200 using the IP addresses you found

### Search examples
get all links with label 'forest'  
navigator: http://localhost:9200/train/_search?q=test_label:forest&filter_path=hits.hits._source.url&size=50  
curl: 
```bash
curl -X GET "http://localhost:9200/train/_search?q=test_label:forest&filter_path=hits.hits._source.url&size=50"
```
python:
```python
es.search(index='train', q='test_label:forest', filter_path='hits.hits._source.url',size=50)
````
