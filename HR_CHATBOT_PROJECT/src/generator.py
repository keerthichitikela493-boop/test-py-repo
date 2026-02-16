from transformers import pipeline

# load local text generation model
generator = pipeline(
    "text-generation",
    model="google/flan-t5-base",
    max_length=100
)

def generate_answer(query, context):
    prompt = f"""
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    result = generator(prompt)[0]["generated_text"]
    return result.strip()
