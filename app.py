from flask import Flask, request, jsonify
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import os
import json

# Setup OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"


# Load the knowledge base
def load_knowledge_base(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

knowledge_base_file = "building_data_segment_1.json"
knowledge_base = load_knowledge_base(knowledge_base_file)

# Format the knowledge base
def format_knowledge_base(data):
    formatted = []
    for key, value in data.items():
        formatted.append(f"{key.capitalize()}: {value}")
    return "\n\n".join(formatted)

formatted_knowledge = format_knowledge_base(knowledge_base)

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=["knowledge_base", "history", "input"],
    template="""
You are a helpful assistant with access to the following knowledge base:

{knowledge_base}

Conversation history:
{history}

User query:
{input}

Provide the most relevant and accurate response to the user query.
"""
)

# Initialize LangChain components
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

conversation = LLMChain(
    llm=llm,
    prompt=prompt_template
)

# Flask app
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("message", "")
    if not user_query:
        return jsonify({"response": "Please provide a valid query."})

    # Run the LangChain conversation
    response = conversation.run({
        "knowledge_base": formatted_knowledge,
        "input": user_query,
        "history": memory.chat_memory
    })

    return jsonify({"response": response})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
