# ---------------- IMPORTS ----------------
import os
import json
import faiss
import numpy as np
from embedder import embed_text


# ---------------- LOAD JSON FILE SAFELY ----------------
BASE_DIR = os.path.dirname(__file__)  # folder where this file exists
file_path = os.path.join(BASE_DIR, "hr_faq.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)


# ---------------- EXTRACT QUESTIONS & ANSWERS ----------------
questions = [item["question"] for item in data]
answers = [item["answer"] for item in data]


# ---------------- CREATE EMBEDDINGS ----------------
embeddings = embed_text(questions)


# ---------------- BUILD FAISS INDEX ----------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


# ---------------- SEARCH FUNCTION ----------------
def search(query, k=2):
    query_vector = embed_text([query])
    distances, indices = index.search(np.array(query_vector), k)

    results = []
    for i in indices[0]:
        results.append(answers[i])

    return results
