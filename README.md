# RUG-NLP-QA
Open-book Question Answering for NLP


# Requirements
## Python
```
pip install -r requirements.txt
```

## Download required models
```
python ./scripts/download_artifacts.py
```

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

Run API in /api/main.py
```
uvicorn api.main:app --reload --port 8000
```


### OpenAI GPT-3
Run the following command to get the API key
```
export OPENAI_API_KEY=<your key>
```