from langchain_google_genai import ChatGoogleGenerativeAI
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python src/agents/summarize_agent.py /path/to/textfile.txt")
        return

    text_file = sys.argv[1]
    with open(text_file, "r") as f:
        text = f.read()

    if not text.strip():
        print("No text to summarize.")
        return

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    prompt = f"Summarize the following document:\n\n{text}"
    summary = model.invoke(prompt)
    print("Summary:")
    print(summary)

if __name__ == "__main__":
    main()
