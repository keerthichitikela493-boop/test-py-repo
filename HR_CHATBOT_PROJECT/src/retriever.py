# ---------------- IMPORTS ----------------
import os
import json
import faiss
import numpy as np
from embedder import embed_text


# ---------------- LOAD JSON FILE ----------------
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "hr_faq.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)


# ---------------- PREPARE DATA ----------------
questions = [item["question"] for item in data]
answers = [item["answer"] for item in data]


# ---------------- CREATE EMBEDDINGS ----------------
embeddings = embed_text(questions).astype("float32")


# ---------------- NORMALIZE VECTORS (IMPORTANT) ----------------
faiss.normalize_L2(embeddings)


# ---------------- BUILD INDEX ----------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # cosine similarity
index.add(embeddings)


# ---------------- SEARCH FUNCTION ----------------
def search(query, k=3, threshold=0.65):
    query_vector = embed_text([query]).astype("float32")
    faiss.normalize_L2(query_vector)

    scores, indices = index.search(query_vector, k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if score >= threshold:
            results.append({
                "answer": answers[idx],
                "score": float(score)
            })

    # ---------------- NO MATCH FOUND ----------------
    if not results:
        return ["I'm not sure about that yet. Please contact HR for accurate information."]

    # ---------------- RETURN BEST ANSWER ONLY ----------------
    best = max(results, key=lambda x: x["score"])
    return [best["answer"]]
