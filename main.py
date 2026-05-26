import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Web Server for Render Health Checks ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Saba Pool Bot is running smoothly!")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"Health check server running on port {port}")
    server.serve_forever()

# --- Bot Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the welcoming landing page with direct portal buttons."""
    
    # Define the links exactly as requested
    channel_url = "https://t.me/SabaPoolGB"
    website_url = "https://fifa2026sport.com/"
    
    # Create high-visibility interactive buttons
    keyboard = [
        [
            InlineKeyboardButton("🚀 Join Saba Pool Telegram Channel", url=channel_url)
        ],
        [
            InlineKeyboardButton("🌐 Visit Official Website", url=website_url)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Welcome message layout
    welcome_text = (
        "🏆 **Welcome to Saba Pool!** 🏆\n\n"
        "Get instant access to live fixtures, expert match pools, and updates right at your fingertips.\n\n"
        "👇 **Click the buttons below to join our community and access our main portal:**"
    )
    
    await update.message.reply_text(
        text=welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown",
        disable_web_page_preview=False
    )

async def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("Missing TELEGRAM_TOKEN environment target variable.")

    # Run the mandatory background port web server for Render
    threading.Thread(target=run_health_server, daemon=True).start()

    # Initialize the app container
    app = Application.builder().token(TOKEN).build()
    
    # Add the core entry router command handler
    app.add_handler(CommandHandler("start", start))
    
    print("Saba Pool core polling engine running...")
    
    async with app:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
