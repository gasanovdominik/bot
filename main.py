import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from hands import (
    start, button_start, random_movie, search_actor, handle_actor_search,
    search_genre, handle_genre_search, search_year, handle_year_search,
    popular_queries, change_language, set_language,  
    SEARCH_ACTOR, SEARCH_GENRE, SEARCH_YEAR
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main():
    application = ApplicationBuilder().token("7903480173:AAHGN_WGifcJDawEFKMafGyyfieHybLIxoo").build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(button_start, pattern='^start$'),
            MessageHandler(filters.Regex("^(🎲 Случайный фильм|🎲 Random Movie|🎲 Zufälliger Film)$"), random_movie),
            MessageHandler(filters.Regex("^(🔎 Поиск по актеру|🔎 Search by Actor|🔎 Suche nach Schauspieler)$"),
                           search_actor),
            MessageHandler(filters.Regex("^(🎭 Поиск по жанру|🎭 Search by Genre|🎭 Suche nach Genre)$"), search_genre),
            MessageHandler(filters.Regex("^(📅 Поиск по году|📅 Search by Year|📅 Suche nach Jahr)$"), search_year),
            MessageHandler(filters.Regex("^(📊 Популярные запросы|📊 Popular Queries|📊 Beliebte Anfragen)$"),
                           popular_queries),
            MessageHandler(filters.Regex("^(🌐 Изменить язык|🌐 Change Language|🌐 Sprache ändern)$"), change_language)
        ],
        states={
            SEARCH_ACTOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_actor_search)],
            SEARCH_GENRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_genre_search)],
            SEARCH_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_year_search)],
            "WAITING_FOR_LANGUAGE": [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()

