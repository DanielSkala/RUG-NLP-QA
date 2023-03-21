from sentence_transformers import SentenceTransformer

model_names = [
    "distiluse-base-multilingual-cased-v1",
    "gpt2"
]

for model_name in model_names:
    model = SentenceTransformer(model_name)
    model.save(f"./artifacts/{model_name}")