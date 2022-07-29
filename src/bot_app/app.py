from .my_local_settings import API_KEY
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .sqlighter import SQLighter, Applications


bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())
db = SQLighter('db.db')
db_applications = Applications('db.db')