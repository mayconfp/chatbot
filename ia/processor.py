from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import os

async def generate_response(message: str, context_path: str, openai_key: str):
     # Carrega FAISS a partir do diretório da empresa
     vector_store = FAISS.load_local(context_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
     retriever = vector_store.as_retriever()
     
     template = "Você é um atendente de IA, contexto: {context}, pergunta: {question}"
     prompt = ChatPromptTemplate.from_template(template)
     
     chain = (
         {'context': retriever, 'question': RunnablePassthrough()}
            | prompt
            | ChatOpenAI(openai_api_key=openai_key)
     )
     
     return await chain.invoke(message)