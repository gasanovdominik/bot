import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler
from database import connect_to_db, search_movies_by_actor, get_random_movie, search_movies_by_genre, search_movies_by_year, log_query, get_popular_queries
from lang import translations

SEARCH_ACTOR, SEARCH_GENRE, SEARCH_YEAR = range(3)

user_language = 'ru'

logger = logging.getLogger(__name__)

def main_keyboard(language):
    try:
        keyboard = [
            [KeyboardButton(translations[language]['random_movie_button'])],
            [KeyboardButton(translations[language]['search_actor_button'])],
            [KeyboardButton(translations[language]['search_genre_button'])],
            [KeyboardButton(translations[language]['search_year_button'])],
            [KeyboardButton(translations[language]['popular_queries_button'])],
            [KeyboardButton(translations[language]['change_language_button'])]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    except KeyError as e:
        logger.error(f"Missing translation key: {e}")
        return None

def start_keyboard():
    keyboard = [[InlineKeyboardButton("Начать", callback_data='start')]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_name = user.first_name if user.first_name else "Пользователь"
    await update.message.reply_text(translations[user_language]['greeting'].format(user_name=user_name), reply_markup=main_keyboard(user_language))
    return ConversationHandler.END

async def button_start(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    user_name = user.first_name if user.first_name else "Пользователь"
    await query.edit_message_text(text=translations[user_language]['greeting'].format(user_name=user_name), reply_markup=main_keyboard(user_language))
    return ConversationHandler.END

async def random_movie(update: Update, context: CallbackContext):
    connection = connect_to_db()
    if not connection:
        await update.message.reply_text(translations[user_language]['error'])
        return
    cursor = connection.cursor()
    movie = get_random_movie(cursor)

    if movie:
        await update.message.reply_text(translations[user_language]['random_movie'].format(movie=movie[0]), parse_mode="Markdown")
    else:
        with open("kotik.jpg", "rb") as image:
            await update.message.reply_photo(photo=image, caption=translations[user_language]['no_results'])

    cursor.close()
    connection.close()
    return ConversationHandler.END

async def search_actor(update: Update, context: CallbackContext):
    await update.message.reply_text(translations[user_language]['enter_actor_name'])
    return SEARCH_ACTOR

async def handle_actor_search(update: Update, context: CallbackContext):
    actor_name = update.message.text.strip()
    if not actor_name:
        await update.message.reply_text(translations[user_language]['enter_actor_name'])
        return SEARCH_ACTOR

    connection = connect_to_db()
    if not connection:
        await update.message.reply_text(translations[user_language]['error'])
        return ConversationHandler.END
    cursor = connection.cursor()
    movies = search_movies_by_actor(cursor, actor_name)

    log_query(cursor, "actor", actor_name)
    connection.commit()

    if movies:
        response = translations[user_language]['actor_search'].format(actor_name=actor_name, movies="\n".join([f"🎞 `{movie[0]}`" for movie in movies]))
        await update.message.reply_text(response, parse_mode="Markdown")
    else:
        with open("kotik.jpg", "rb") as image:
            await update.message.reply_photo(photo=image, caption=translations[user_language]['no_results'])

    cursor.close()
    connection.close()
    return ConversationHandler.END

async def search_genre(update: Update, context: CallbackContext):
    await update.message.reply_text(translations[user_language]['enter_genre_name'])
    return SEARCH_GENRE

async def handle_genre_search(update: Update, context: CallbackContext):
    genre_name = update.message.text.strip()
    if not genre_name:
        await update.message.reply_text(translations[user_language]['enter_genre_name'])
        return SEARCH_GENRE

    connection = connect_to_db()
    if not connection:
        await update.message.reply_text(translations[user_language]['error'])
        return ConversationHandler.END
    cursor = connection.cursor()
    movies = search_movies_by_genre(cursor, genre_name)

    log_query(cursor, "genre", genre_name)
    connection.commit()

    if movies:
        response = translations[user_language]['genre_search'].format(genre_name=genre_name, movies="\n".join([f"🎞 `{movie[0]}`" for movie in movies]))
        await update.message.reply_text(response, parse_mode="Markdown")
    else:
        with open("kotik.jpg", "rb") as image:
            await update.message.reply_photo(photo=image, caption=translations[user_language]['no_results'])

    cursor.close()
    connection.close()
    return ConversationHandler.END

async def search_year(update: Update, context: CallbackContext):
    await update.message.reply_text(translations[user_language]['enter_year'])
    return SEARCH_YEAR

async def handle_year_search(update: Update, context: CallbackContext):
    year = update.message.text.strip()
    if not year.isdigit():
        await update.message.reply_text(translations[user_language]['enter_year'])
        return SEARCH_YEAR

    connection = connect_to_db()
    if not connection:
        await update.message.reply_text(translations[user_language]['error'])
        return ConversationHandler.END
    cursor = connection.cursor()
    movies = search_movies_by_year(cursor, year)

    log_query(cursor, "year", year)
    connection.commit()

    if movies:
        response = translations[user_language]['year_search'].format(year=year, movies="\n".join([f"🎞 `{movie[0]}`" for movie in movies]))
        await update.message.reply_text(response, parse_mode="Markdown")
    else:
        with open("kotik.jpg", "rb") as image:
            await update.message.reply_photo(photo=image, caption=translations[user_language]['no_results'])

    cursor.close()
    connection.close()
    return ConversationHandler.END

async def popular_queries(update: Update, context: CallbackContext):
    connection = connect_to_db()
    if not connection:
        await update.message.reply_text(translations[user_language]['error'])
        return
    cursor = connection.cursor()
    queries = get_popular_queries(cursor)

    if queries:
        response = translations[user_language]['popular_queries'].format(queries="\n".join([f"{query[0]}: `{query[1]}` ({query[2]} раз)" for query in queries]))
        await update.message.reply_text(response, parse_mode="Markdown")
    else:
        await update.message.reply_text(translations[user_language]['no_results'])

    cursor.close()
    connection.close()
    return ConversationHandler.END

async def change_language(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Выберите язык / Choose language / Wählen Sie die Sprache:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Русский")],
                [KeyboardButton("English")],
                [KeyboardButton("Deutsch")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    return "WAITING_FOR_LANGUAGE"

async def set_language(update: Update, context: CallbackContext):
    global user_language
    language_choice = update.message.text.strip().lower()

    if language_choice in ["русский", "russian"]:
        user_language = 'ru'
    elif language_choice in ["english", "английский"]:
        user_language = 'en'
    elif language_choice in ["deutsch", "немецкий"]:
        user_language = 'de'
    else:
        await update.message.reply_text("Некорректный выбор. Пожалуйста, выберите язык из предложенных.")
        return "WAITING_FOR_LANGUAGE"

    await update.message.reply_text(
        translations[user_language]['greeting'].format(user_name=update.effective_user.first_name),
        reply_markup=main_keyboard(user_language)
    )
    return ConversationHandler.END





