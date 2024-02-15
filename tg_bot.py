from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage, AIMessage
import ey_demo
load_dotenv()
TOKEN = os.getenv('TG_TOKEN')


chat_history = []

async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:  
    if chat_history == []:
        chat_history.append(AIMessage(content= 'good day mate'))
        
    await update.message.reply_html(rf"Answer {update.effective_user.mention_html()}'s Question")
    response = ey_demo.test_get_answer(chat_history= chat_history,user_query=update.message.text)
    await update.message.reply_text(response)
    chat_history.append(HumanMessage(content= update.message.text) )
    chat_history.append(AIMessage(content=response ))
    
    if len(chat_history) > 10:
        chat_history.pop(0)



app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, reply_message))
app.run_polling(allowed_updates=Update.ALL_TYPES)