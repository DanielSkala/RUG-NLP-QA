# RUG-NLP-QA

Open-book Question Answering for NLP

## 1. Create a virtual environment
(make sure you are in the base environemnt)
```
# create a clean virtual environment
conda deactivate
conda env remove -n temp-env-py3.9
conda create -n temp-env-py3.9 python=3.9 -y
conda activate temp-env-py3.9
```

## 2. Install requirements

```
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Download required models
If this fails, you have to manually download artifacts from TODO (google drive) and put them in 
the root folder
Beware that the models are quite large (around 1GB)
```
python ./scripts/download_artifacts.py
```

## 4. Set up Elastic Search

Installation using docker is the easiest
Make sure docker is installed and running

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

## 5. Index PDF documents
It will ask you for a path to a pdf which can be found in ./samples and a name 
```
python ./pdf_indexer.py
```
## 6. After running the script, verify that the embeddings and text entries have been stored
You should see a ton of text
```
http://localhost:9200/example_document_index_3/_search
http://localhost:9200/example_embedding_index_3/_search
```

### [Optional] OpenAI GPT-3

Run the following command to get the API key

```
export OPENAI_API_KEY=<your key>
```

## Run API in /api/main.py

```
python -m uvicorn api.main:app --reload --port 8000
```

## Sample API calls
It is better to use a tool such as Insomnia or Postman to make API calls but you can also just 
copy&paste the following commands into your browser.

Example queries: 
1. What is the equation of multihead attention?
2. When was Stalin born?
3. Who are the authors of this paper?

Example API calls:
```
http://localhost:8000/doc/<doc_id>/_index?q=<query>
http://localhost:8000/doc/stalingay/_index?
q=What%20is%20the%20equation%20of%20multihead%20attention?
```

## [Optional] Clean up & delete a virtual environment

```
conda deactivate
conda env remove -n temp-env-py3.9
```