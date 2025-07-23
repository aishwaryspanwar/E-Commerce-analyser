from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

model = OllamaLLM(model="llama3")

prompt_text = (
    "You are tasked with extracting specific information from the following text content:\n\n"
    "{dom_content}\n\n"
    "Please follow these instructions carefully:\n"
    "1. Extract only the information that directly matches the description: compare the product name, cost, and review in a tabular form.\n"
    "2. Do not include any extra text, comments, or explanations.\n"
    "3. If nothing matches, return an empty string ('').\n"
    "4. Output only the requested data—no other text.\n"
    "5. Return the data in a structured format (a Markdown table).\n"
    "6. Ignore any irrelevant data at the very start of the DOM; begin from the first relevant product entry.\n"
)

prompt = ChatPromptTemplate.from_template(prompt_text)
chain = LLMChain(llm=model, prompt=prompt)

def parse_with_ollama(chunks):
    results = []
    for idx, chunk in enumerate(chunks, start=1):
        print(f"Processing chunk {idx}/{len(chunks)}…")
        response = chain.invoke({"dom_content": chunk})
        if isinstance(response, dict):
            text = response.get("text", "").strip()
        else:
            text = str(response).strip()
        if text:
            results.append(text)
    return "\n\n".join(results)
