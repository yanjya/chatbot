from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os 
from pypdf import PdfReader
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


#load api key
load_dotenv()

#load file and turn pdf into retriever
def get_prepared_data() :

    text = ''
    for pdf in os.listdir('pdf_file'):
        pdf_reader = PdfReader(f"pdf_file/{pdf}")
        for page in pdf_reader.pages:
            text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs_chunks = text_splitter.split_text(text)
    pdf_vectorstore = Chroma.from_texts(docs_chunks, OpenAIEmbeddings())
    return pdf_vectorstore.as_retriever()

#
def get_answer(user_query):
    """
    create stuff chain :是把輸出格式promt template  還有query 裝在一起的chain
    create_history_aware_retriever : 把chat_history還新的query 跟retriever 裝一起
    最後再使用create retriever chain 把有chat history 的retriever 還有 stuff docs 組合
    """
    #get random tarot card

    #load retriever
    retriever = get_prepared_data()  

    #create output prompt template for create_stuff_documents_chain
    output_prompt = ChatPromptTemplate.from_messages([
      ("system", "假設你是一位專業的中醫師還有心理諮商師，你會透過心理諮商的技巧還有關心鼓勵user 然後會用中醫的知識推薦一款飲料給user :\n\n{context}"),
      
      ("user", "{input}"),
      ("system","1. 先表示理解用戶心情"),
      ("system","2. 仔細思考應該要如何回答"),
      ("system","3. 重複user's 的問題，然後必須花100字給予溫暖還有鼓勵"),
      ("system","4. 鼓勵完必須加入兩次enter做出分段 \n\n"),
      ("system","5. 然後再用中醫的專業針對他的問題推薦他飲料然後解釋"),
      ("system","6. 跟他說這是不含咖啡因一整天都適合的好物"),
    ])





    document_chain = create_stuff_documents_chain(ChatOpenAI(), output_prompt )


    # history_chat_retriever_chain = create_history_aware_retriever(ChatOpenAI(), retriever, prompt)
    final_retriever_chain = create_retrieval_chain(retriever, document_chain)
    response = final_retriever_chain.invoke({
                
                "input": user_query,
                })
    activity_link = 'https://forms.gle/cMUNAZSumLSLUtXS6'
    a =  response['answer'] + f'\n\n "拿此對話到實體商店可享單品9折" \n\n最近有好玩的喝茶體驗活動，很多有趣的人都會參加，名額有限，趕快報名！\n\n{activity_link}'

    return a

