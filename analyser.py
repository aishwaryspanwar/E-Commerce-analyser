from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
model = OllamaLLM(model="gemma3")
prompt_text = (
    "You are tasked with extracting specific information from the following text content:\n\n"
    "{dom_content}\n\n"
    "Please follow these instructions carefully:\n"
    "1. Extract only the information that directly matches the description: compare the product name, selling price, MRP, delivery date, review and any more relevant comparison features (like colour, storage, weight etc) depending on the type of product in a tabular form.\n"
    "2. Do not include any extra text, comments, or explanations.\n"
    "3. If nothing matches, return an empty string ('').\n"
    "4. Output only the requested data—no other text.\n"
    "5. Return the data in a structured format (a Markdown table), don't add a note or any heading beside it.\n"
    "6. Ensure the output is clean and formatted correctly for easy readability.\n"
    "7. Don't type 'Here are the extracted product details:'.\n")

prompt = ChatPromptTemplate.from_template(prompt_text)
chain = LLMChain(llm=model, prompt=prompt)

@lru_cache(maxsize=16)
def _parse_chunk(chunk: str) -> str:
    resp = chain.invoke({"dom_content": chunk})
    if isinstance(resp, dict):
        text = resp.get("text", "").strip()
    else:
        text = str(resp).strip()
    return text

def parse_with_ollama(chunks):
    """
    Try to send all data in one go if possible; otherwise parallelize.
    Returns the combined extracted tables.
    """
    if len(chunks) == 1:
        return _parse_chunk(chunks[0])

    total_length = sum(len(c) for c in chunks)
    if total_length < 20000:
        merged = "\n\n".join(chunks)
        return _parse_chunk(merged)

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = pool.map(_parse_chunk, chunks)

    tables = [r for r in results if r]
    return "\n\n".join(tables)
