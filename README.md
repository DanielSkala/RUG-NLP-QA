# RUG-NLP-QA
Open-book Question Answering for NLP


# Requirements
## Elastic Search
Installation using docker is the easiest
```
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.6.2
docker network create elastic
docker run -d \
        --name es42 \
       -p 9200:9200 \
       -p 9300:9300 \
       -e "discovery.type=single-node" \
       -e "xpack.security.enabled=false" \
       docker.elastic.co/elasticsearch/elasticsearch:8.6.2
```

Check with 
```
curl -XGET 'localhost:9200/_cluster/health?pretty'
```
Find indexes
```
curl http://localhost:9200/_aliases
```

## Python
```
pip install -r requirements.txt
```