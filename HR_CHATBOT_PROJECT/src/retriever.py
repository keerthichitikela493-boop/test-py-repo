import json
import faiss
import numpy as np
from embedder import embed_text

with open("hr_faq.json") as f:
    data = json.load(f)

questions = [item["question"] for item in data]
answers = [item["answer"] for item in data]

embeddings = embed_text(questions)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

def search(query, k=2):
    query_vector = embed_text([query])
    distances, indices = index.search(np.array(query_vector), k)

    results = []
    for i in indices[0]:
        results.append(answers[i])

    return results
