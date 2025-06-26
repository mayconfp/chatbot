from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

async def generate_response(message: str, context_path: str, openai_key: str):
    print(f"📥 Mensagem recebida: {message}")
    print(f"📁 Caminho do contexto: {context_path}")
    print("🔍 Carregando FAISS...")

    vector_store = FAISS.load_local(
        context_path,
        OpenAIEmbeddings(openai_api_key=openai_key),
        allow_dangerous_deserialization=True
    )

    print("✅ FAISS carregado com sucesso!")
    retriever = vector_store.as_retriever()
    print("🔗 Retriever criado.")

    # Recupera documentos como contexto
    docs = await retriever.aget_relevant_documents(message)
    context = "\n\n".join([doc.page_content for doc in docs])
    print("📄 Contexto recuperado:", context)

    template = """
     Você é um atendente de IA. Use o contexto abaixo para responder de forma direta, cordial e precisa.

     Se a resposta não estiver no contexto, diga: "Desculpe, essa informação não está disponível no momento."

     Contexto:
     {context}

     Pergunta do cliente:
     {question}
     """

    prompt = ChatPromptTemplate.from_template(template)
    print("🧠 Prompt construído.")

    chain = (
        {"context": lambda _: context, "question": RunnablePassthrough()}
        | prompt
        | ChatOpenAI(model="gpt-3.5-turbo", api_key=SecretStr(openai_key))
    )

    print("🚀 Executando a chain...")
    return await chain.ainvoke({"question": message})

