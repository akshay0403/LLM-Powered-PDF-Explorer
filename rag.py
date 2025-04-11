# -*- coding: utf-8 -*-
"""RAG.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RS2vIWeiGySqJWwgmRd__U7dmytevPbA

# Installing the Required Libararies
"""

!pip install -r requirement.txt

!pip install --upgrade unstructured[local-interference]

"""# Importing the Required Libraries"""

import os
from langchain.document_loaders import UnstructuredFileIOLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

"""# Loding the API Key"""

os.environ['GROQ_API_KEY'] = "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"

"""# Loading the Raw Data ( pdf )"""

import requests
url = "https://www.local1070.org/system/files/12.28.21_crypto_seminar.pdf"

response = requests.get(url)

response

"""# Save the pdf to Loacal File"""

with open("crypto_blockchain.pdf", "wb") as f:
    f.write(response.content)

!pip install pi_heif

with open("crypto_blockchain.pdf", "rb") as f:
  loader = UnstructuredFileIOLoader(file = f)
  documents = loader.load()

documents

"""# Chunking the pdf"""

text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)

text_splitter

texts = text_splitter.split_documents(documents)

type(texts)

"""# Embeddings"""

embeddings = HuggingFaceEmbeddings()

"""# Creating Vector Database"""

persist_directory = "vector_db"

vectordb = Chroma.from_documents(texts, embeddings, persist_directory = persist_directory)

"""# Retreival"""

retriver = vectordb.as_retriever()

"""# Loading the LLM"""

llm = ChatGroq(model = "Llama-3.3-70b-versatile", temperature = 0)

"""# Combining All The Steps"""

qa_chain = RetrievalQA.from_chain_type(llm = llm, chain_type = "stuff", retriever = retriver, return_source_documents = True)

"""# Testing the RAG Model -> Test # 1"""

query = "What is the meaning of cryptocurrency from this pdf"
response = qa_chain.invoke({"query":query})

print(response)

print(response['result'])

"""# Testing the RAG Model -> Test # 2"""

query_2 = "Can you explain about blockchain from this pdf"
response_2 = qa_chain.invoke({"query":query_2})

print(response_2)

print(response_2['result'])

