from transformers import pipeline

# load local text generation model
generator = pipeline(
    "text-generation",
    model="google/flan-t5-base",
    max_length=100
)

def generate_answer(query, context):

    context_text = " ".join(context) if context else "No info available"

    prompt = f"""
You are a friendly HR assistant.

Context:
{context_text}

Employee question: {query}


"""

    result = generator(prompt, max_new_tokens=120)[0]["generated_text"]
    return result.strip()

