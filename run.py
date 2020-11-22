from trading_bot import Bot
from api_config import API_KEY, ALLOWED_CALLS_PER_MINUTE

bot = Bot(API_KEY, ALLOWED_CALLS_PER_MINUTE)
bot.start()
