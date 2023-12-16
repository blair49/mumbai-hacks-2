# !pip install openai langchain sentence_transformers -q
# !pip install unstructured -q

# # install the environment dependencies
# !pip install pydantic==1.10.8
# !pip install typing-inspect==0.8.0 typing_extensions==4.5.
# !pip install chromadb==0.3.26

# !pip install "unstructured[pdf]"

# import langchain dir loader from document loaders
from langchain.document_loaders import DirectoryLoader

# directory path
directory = './documents'

# function to load the text docs
def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

documents = load_docs(directory)
len(documents)

# use text splitter to split text in chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

# split the docs into chunks using recursive character splitter
def split_docs(documents,chunk_size=1000,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

# store the splitte documnets in docs variable
docs = split_docs(documents)

# embeddings using langchain
from langchain.embeddings import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# using chromadb as a vectorstore and storing the docs in it
from langchain.vectorstores import Chroma
db = Chroma.from_documents(docs, embeddings)

# insert an openai key below parameter
import os
from google.colab import userdata
openai_api_key = userdata.get('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = openai_api_key

# load the LLM model
from langchain.chat_models import ChatOpenAI
model_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=model_name)


# Using q&a chain to get the answer for our query
from langchain.chains.question_answering import load_qa_chain
chain = load_qa_chain(llm, chain_type="stuff",verbose=True)

# Doing similarity search  using query
# query = "Tell me about the buffalo marriage case"
# matching_docs = db.similarity_search(query)

# print(matching_docs[0])

# answer =  chain.run(input_documents=matching_docs, question=query)
# print(answer)

# !pip install Flask

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api/generate_response', methods=['POST'])
def getResponse():
  data = request.get_json()
  user_input = data.get('user_input', '')
  matching_docs = db.similarity_search(user_input)
  answer =  chain.run(input_documents=matching_docs, question=user_input)
  return jsonify({'response': answer})

if __name__ == '__main__':
    app.run(debug=True)

