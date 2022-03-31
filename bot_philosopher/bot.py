from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, Emoji
from importlib import reload
from pony import orm
import logging, math, sys

reload(sys)


# ORM
db = orm.Database()


class Db_Sheet1(db.Entity):
    Quote_ID = orm.PrimaryKey(int, auto=True)
    Name = orm.Required(str)
    Quote_Category = orm.Required(str)
    Quote = orm.Required(str)


# Подключение к базе
db.bind(
    provider="sqlite",
    filename="/Users/fomindmitry/Documents/GitHub/bot_philosopher/DB.sqlite",
    create_db=True,
)
db.generate_mapping()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Функция, которая возвращает создает кнопки категорий на экране
def category_names():
    # Выбираем все категории, которые у нас есть
    with orm.db_session:
        category_names = Db_Sheet1.select_by_sql(
            "SELECT Quote_Category, Quote_ID FROM db_Sheet1;"
        )
        custom_keyboard = list(
            set(
                [
                    category_names[:][i].Quote_Category
                    for i in range(len(category_names[:]))
                ]
            )
        )
    # Создаем переменную с уникальными категориями
    custom_keyboard = [
        custom_keyboard[2 * i : 2 * (i + 1)]
        for i in range(int(math.ceil(len(category_names[:]) / 2)))
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    return reply_markup


# Функция, которая создает кнопки авторов на экране
def author_names():
    with orm.db_session:
        author_names = Db_Sheet1.select_by_sql("SELECT Name, Quote_ID FROM db_Sheet1;")
        custom_keyboard = list(
            set([author_names[:][i].Name for i in range(len(author_names[:]))])
        )
    # Создаем переменную с уникальными именами
    custom_keyboard = [
        custom_keyboard[2 * i : 2 * (i + 1)]
        for i in range(int(math.ceil(len(author_names[:]) / 2)))
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    return reply_markup


# Возвращаем реплику исходя из того, что нажали на экране
def get_quote_by_category(index, args):
    with orm.db_session:
        category_list = Db_Sheet1.select_by_sql(
            "SELECT Quote_Category,Quote_ID FROM db_Sheet1;"
        )
        category = list(
            set(
                [
                    category_list[:][i].Quote_Category
                    for i in range(len(category_list[:]))
                ]
            )
        )
        if args in category:
            quote = Db_Sheet1.select_by_sql(
                f"""SELECT Quote,
                           Quote_Category, Name,
                           Quote_ID FROM db_Sheet1 WHERE Quote_Category = "{args}" ORDER BY RANDOM() LIMIT 1;"""
            )[0]
        else:
            quote = Db_Sheet1.select_by_sql(
                f"""SELECT Quote,
                         Quote_Category,
                         Name,Quote_ID FROM db_Sheet1 WHERE Name = "{args}" ORDER BY RANDOM() LIMIT 1;"""
            )[0]
        return f"{quote.Quote} ~ {quote.Name} \n {Emoji.THOUGHT_BALLOON}"


# Берем из базы случайную реплику и возвращаем ее пользователю
def get_random_quote():
    with orm.db_session:
        quote = Db_Sheet1.select_by_sql(
            "SELECT Quote, Name, Quote_ID FROM db_Sheet1 ORDER BY RANDOM() LIMIT 1;"
        )[0]
    return f"{quote.Quote} ~ {quote.Name} \n {Emoji.THOUGHT_BALLOON}"


# Что пишем при старте
def start(bot, update):
    text = """Я бесполезный бот философ,такой же бесполезный как все философы.

Если тебе хочется услышать какую-нибудь цитату по категории,то введи /category.
Либо /author, если нужна цитата по автору.
Если тебе хочется услышать случайную цитату с улиц, то введи /random

Если нужна помощь - /help"""
    bot.sendMessage(update.message.chat_id, text=text)


# Вызвать категории
def category(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Хмм..какая именно категория тебя интересует?",
        reply_markup=category_names(),
    )


# Вызвать авторов
def author(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Хмм..и кто же именно тебе нужен?",
        reply_markup=author_names(),
    )


# Рандомная цитата
def random(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=get_random_quote())


# Информация о боте
def about(bot, update):
    bot.sendMessage(
        update.message.chat_id, text="Цель моей жизни - сдать экзамен Хозяину"
    )


# Вызвать помощь
def help(bot, update):
    bot.sendMessage(
        update.message.chat_id,
        text=f"""Знания - это сила {Emoji.THOUGHT_BALLOON}
/category - Выбрать цитату по категории
/author - Выбрать цитату по автору
/random - Выбрать случайную цитату
/about - Расскажет о смысле существования бота""",
    )


# Вернуть ответ при нажатии на клавишу
def user_reply(bot, update):
    bot.sendMessage(
        update.message.chat_id, text=get_quote_by_category(0, update.message.text)
    )


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


# The EventHandler
updater = Updater("5107716470:AAHDiqCGYzMFsN423isheUE2px8pTGiK7ZU")

# Get the dispatcher to register handlers
dp = updater.dispatcher

# on command
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("about", about))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("category", category))
dp.add_handler(CommandHandler("author", author))
dp.add_handler(CommandHandler("random", random))

# On nocommand
dp.add_handler(MessageHandler([Filters.text], user_reply))

# Log all errors
dp.add_error_handler(error)

# Start the Bot
updater.start_polling()

updater.idle()

