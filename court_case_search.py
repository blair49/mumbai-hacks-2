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

# load the LLM model
from langchain.chat_models import ChatOpenAI
model_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=model_name)


# Using q&a chain to get the answer for our query
from langchain.chains.question_answering import load_qa_chain
chain = load_qa_chain(llm, chain_type="stuff",verbose=True)

def getResponse(query):
  matching_docs = db.similarity_search(query)
  answer =  chain.run(input_documents=matching_docs, question=query)
  return answer



