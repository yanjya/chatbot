from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
import os 
from pypdf import PdfReader
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

#load api key
load_dotenv()

def get_prepared_data() :
    '''
    load file and turn pdf into retriever
    '''
    text = ''
    for pdf in os.listdir('pdf_file'):
        pdf_reader = PdfReader(f"pdf_file/{pdf}")
        for page in pdf_reader.pages:
            text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs_chunks = text_splitter.split_text(text)
    pdf_vectorstore = Chroma.from_texts(docs_chunks, OpenAIEmbeddings())
    return pdf_vectorstore.as_retriever()

def test_get_answer(chat_history,user_query):
    """
    create stuff chain :是把輸出格式promt template  還有query 裝在一起的chain
    create_history_aware_retriever : 把chat_history還新的query 跟retriever 裝一起
    最後再使用create retriever chain 把有chat history 的retriever 還有 stuff docs 組合
    """
    #load retriever
    retriever = get_prepared_data()  

    #create output prompt template for create_stuff_documents_chain
    output_prompt = ChatPromptTemplate.from_messages([
      ("system", "Answer the user's questions based on the below context:\n\n{context}"),
      MessagesPlaceholder(variable_name="chat_history"),
      ("user", "{input}"),
    ])

    
    document_chain = create_stuff_documents_chain(ChatOpenAI(), output_prompt)

    # create prompt template for create_history_aware_retriever
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    
    history_chat_retriever_chain = create_history_aware_retriever(ChatOpenAI(), retriever, prompt)
    final_retriever_chain = create_retrieval_chain(history_chat_retriever_chain, document_chain)
    response = final_retriever_chain.invoke({
                "chat_history": chat_history,
                "input": user_query,
                })
    
    return response['answer']
