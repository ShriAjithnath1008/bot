import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = '7827622692:AAGTBPcthhZCiJmmS5OnBgIfewVunNEatnQ'
GEMINI_API_KEY = 'AIzaSyCnhwgJQCgVgSGKXslYU6dsPZIRcrD7YuU'
GEMINI_FLASH_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! I'm powered by Gemini 1.5 Flash. Ask me anything.")

async def send_long_message(update: Update, text: str):
    for i in range(0, len(text), 4096):
        await update.message.reply_text(text[i:i + 4096])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": user_input}]}
        ]
    }

    try:
        response = requests.post(GEMINI_FLASH_URL, headers=headers, json=payload)
        result = response.json()

        if "candidates" in result:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in result:
            error_message = result["error"].get("message", "Unknown error")
            reply = f"Gemini API Error: {error_message}\n\nFull response:\n{result}"
        else:
            reply = f"Empty or unrecognized response from Gemini.\n\nFull response:\n{result}"

    except Exception as e:
        reply = f"Exception occurred while contacting Gemini API: {str(e)}"

    await send_long_message(update, reply)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running with Gemini 1.5 Flash...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
