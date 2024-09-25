from .my_local_settings import API_KEY
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .sqlighter import SQLighter, Applications, Bank
import logging


bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())
db = SQLighter('db.db')
db_applications = Applications('db.db')
db_bank = Bank('db.db')

# logging.basicConfig(
#     level=logging.INFO,
#     filename="bot_log.log",
#     filemode="w",
#     format="%(asctime)s %(levelname)s %(message)s"
# )
