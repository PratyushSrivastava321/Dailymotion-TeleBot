import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

API_TOKEN = "YOUR_API_TOKEN"

def get_dailymotion_download_link(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,  # Suppress output
        'skip_download': True  # Do not download the video, only get the info
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_url = info_dict.get('url', None)
        return video_url

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a Dailymotion video URL, and I will provide you with a download link.')

# Message handler for URLs
def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text

    try:
        update.message.reply_text('Fetching download link...')
        download_link = get_dailymotion_download_link(url)
        if download_link:
            update.message.reply_text(f'Download link: {download_link}')
        else:
            update.message.reply_text('Failed to retrieve download link.')

    except Exception as e:
        update.message.reply_text(f'An error occurred: {e}')

# Main function to run the bot
def main():
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
    updater = Updater(API_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

