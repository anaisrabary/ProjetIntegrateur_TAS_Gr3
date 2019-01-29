# Projet Intégrateur TAS
INSA Toulouse

## Summary
* Prerequisites
* Getting Started
* Pipeline / architecture
* Scenario
* [Deployment](Deployment)
* [Bibliographic](biblio)


## Prerequisites
1. Make sure you have **conda** package
```sh
conda --version
```
If not please install [Anaconda](https://www.anaconda.com/download/#linux) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

1. Make sure you have [**docker**](https://docs.docker.com/install/linux/docker-ce/ubuntu/) and [**docker-compose**](https://docs.docker.com/compose/install/) installed.

## Getting Started
The project consists of 3 environment:
* The Python environment
* Docker for Minio and Elastic Search deployment.
* The Spark in system environment

### Python environment

1. Recreate the conda environment from `conda_env.yml`, :
```sh
conda env create -f conda_env.yml
```

1. Activate `cert-big-data` just created (Linux miniconda):
```sh
conda activate cert-big-data
```
The syntax depending on your environment and the tool your are using, please refer to the links above.

1. Check if your python version
```sh
python --version
### Should be 3.6.x
```

### Infrastructure deploy by Docker:
1. Copy **INSA_data_images** into **Deployment** and execute
```sh
cd Deployment
docker-compose pull
sudo sysctl -w vm.max_map_count=262144
docker-compose up --build
```

1. Start the docker services
```sh
docker-compose start
```

1. Wait for a while and check minio instance in your browser at `localhost:9001` and ElasticSearch at `localhost:9200`

### Spark Hadoop configuration:
1. Download Spark `spark-2.3.0-bin-without-hadoop` from [here](https://www.apache.org/dyn/closer.lua/spark/spark-2.3.0/spark-2.3.0-bin-without-hadoop.tgz) and extract the tar into the Spark directory (supposing `~/spark-2.3.0-bin-without-hadoop`).

1. Download Hadoop `hadoop-2.8.2` from [here](https://archive.apache.org/dist/hadoop/core/hadoop-2.8.2/hadoop-2.8.2.tar.gz) and extract into the neighbor (supposing `~/hadoop-2.8.2`)

1. Open the `~/.bashrc` file and add at the end:
```sh
# config hadoop
export HADOOP_HOME=~/hadoop-2.8.2
export PATH=$HADOOP_HOME/bin:$PATH
export SPARK_DIST_CLASSPATH=$(hadoop classpath)

# config spark
export SPARK_HOME=~/spark-2.3.0-bin-without-hadoop
export PATH=$SPARK_HOME/bin:$PATH
```

1. Reload the terminal `source ~/.bashrc`.

1. Download all dependencies:
    - [`Hadoop 2.8.2`](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws/2.8.2)
    - [`HttpClient 4.5.3`](https://mvnrepository.com/artifact/org.apache.httpcomponents/httpclient/4.5.3)
    - [`Joda Time 2.9.9`](https://mvnrepository.com/artifact/joda-time/joda-time/2.9.9)
    - [`AWS SDK For Java Core 1.11.234`](https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-core/1.11.234)
    - [`AWS SDK For Java 1.11.234`](https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk/1.11.234)
    - [`AWS Java SDK For AWS KMS 1.11.234`](http://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-kms/1.11.234)
    - [`AWS Java SDK For Amazon S3 1.11.234`](https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-s3/1.11.234)

1. Extract all the jar file into `$SPARK_HOME/bin`

1. Configure **HADOOP** to communicate with **Minio** (which is currently listening in `localhost:9001`) by editing the file `$HADOOP_HOME/etc/hadoop/core-site.xml` as the following:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>fs.s3a.endpoint</name>
    <description>
      DECA Minio endpoint
    </description>
    <value>http://127.0.0.1:9001</value>
  </property>

  <property>
    <name>fs.s3a.access.key</name>
    <description>AWS access key ID.</description>
    <value>minio</value>
  </property>

  <property>
    <name>fs.s3a.secret.key</name>
    <description>AWS secret key.</description>
    <value>minio123</value>
  </property>

  <property>
    <name>fs.s3a.path.style.access</name>
    <value>true</value>
    <description>Enable S3 path style access ie disabling the default virtual hosting behaviour.
      Useful for S3A-compliant storage providers as it removes the need to set up DNS for virtual hosting.
    </description>
  </property>

  <property>
    <name>fs.s3a.impl</name>
    <value>org.apache.hadoop.fs.s3a.S3AFileSystem</value>
    <description>The implementation class of the S3A Filesystem</description>
  </property>
</configuration>
```

1. Test spark shell from `$SPARK_HOME`
```sh
cd $SPARK_HOME
spark-shell --master local[4] --jars "../bin/hadoop-aws-2.8.2.jar,../bin/httpclient-4.5.3.jar,../bin/aws-java-sdk-core-1.11.234.jar,../bin/aws-java-sdk-kms-1.11.234.jar,../bin/aws-java-sdk-1.11.234.jar,../bin/aws-java-sdk-s3-1.11.234.jar,../bin/joda-time-2.9.9.jar"
```

You should See
```sh
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.3.0
      /_/

Using Scala version 2.11.8 (OpenJDK 64-Bit Server VM, Java 1.8.0_162)
Type in expressions to have them evaluated.
Type :help for more information.

scala>
```

1. You can test in spark shell whether you can retrieve data from minio
```python
val b1 = sc.textFile("s3a://train/0.npy")
b1.collect()
```

## Pipeline / architecture
Explained in project report

## Scenario
