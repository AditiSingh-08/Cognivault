
from app.services.llm_service import load_llm

print("Loading Gemini through LangChain...", flush=True)

try:
    llm = load_llm()

    print("Model loaded successfully!", flush=True)

    response = llm.invoke("Say hello in one sentence.")

    print("\nGemini response:")

    if isinstance(response.content, list):
        for item in response.content:
            if item.get("type") == "text":
                print(item["text"])
    else:
        print(response.content)

except Exception as e:
    print("\nError:", type(e).__name__)
    print(str(e))
