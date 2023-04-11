from fastapi import FastAPI
from algorithm.ir_system import IRSystem
from algorithm.document_operator import PDFDocumentOperator
from datasets import load_dataset
from algorithm.caching_strategy import PDFChunkingCachingStrategy
import settings
from sentence_transformers import SentenceTransformer, util
import time
from tqdm import tqdm

caching_strategy = PDFChunkingCachingStrategy(
    document_factory=settings.document_factory,
    embedding_factory=settings.embedding_factory,
    embedding_operator=settings.embedding_operator,
    # embedding_operator=OpenAIEmbeddingOperator("text-embedding-ada-002"),
    document_operator=PDFDocumentOperator()
)

ir_system = IRSystem(
    answer_strategy=settings.answer_strategy,
    caching_strategy=caching_strategy,
)

# app = FastAPI()

questions_dataset = load_dataset('GroNLP/ik-nlp-22_slp', 'questions')
question_list = questions_dataset['test']['question']
answer_list = questions_dataset['test']['answer']
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
similarity_list = []

start_time = time.time()

for q in tqdm(question_list):
    if question_list.index(q) == 25:
        continue
    result = ir_system.find('test', q)
    gen_answer = model.encode(result['answer'])
    correct_answer = model.encode(answer_list[question_list.index(q)])

    cosine_score = util.pytorch_cos_sim(gen_answer, correct_answer)
    print(f"Generated answer: {result['answer']}\n \n Correct answer: {answer_list[question_list.index(q)]}\n \n Cosine score: {cosine_score}")
    similarity_list.append(cosine_score)

# stop the timer
end_time = time.time()

# elapsed time
semantic_similarity_elapsed_time = end_time - start_time

print(f"Average cosine score: {sum(similarity_list)/len(similarity_list)}")
print(f"Information retrieval time: {round(semantic_similarity_elapsed_time, 2)} seconds")