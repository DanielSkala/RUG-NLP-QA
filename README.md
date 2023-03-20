# RUG-NLP-QA
Open-book Question Answering for NLP


# Requirements
## Elastic Search
Installation using docker is the easiest
```
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.6.2
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.6.2
```
## Python
```
pip install -r requirements.txt
```