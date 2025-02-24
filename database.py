import logging
import mysql.connector

logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": "ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com",
    "user": "ich1",
    "password": "password",
    "database": "sakila"
}

def connect_to_db():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Ошибка подключения к базе данных: {err}")
        return None

def search_movies_by_actor(cursor, actor_name):
    cursor.execute("""
        SELECT f.title FROM film f
        JOIN film_actor fa ON f.film_id = fa.film_id
        JOIN actor a ON fa.actor_id = a.actor_id
        WHERE a.first_name LIKE %s OR a.last_name LIKE %s
    """, (f"%{actor_name}%", f"%{actor_name}%"))
    return cursor.fetchall()

def get_random_movie(cursor):
    cursor.execute("SELECT title FROM film ORDER BY RAND() LIMIT 1")
    return cursor.fetchone()

def search_movies_by_genre(cursor, genre):
    cursor.execute("""
        SELECT f.title FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE c.name LIKE %s
    """, (f"%{genre}%",))
    return cursor.fetchall()

def search_movies_by_year(cursor, year):
    cursor.execute("SELECT title FROM film WHERE release_year = %s", (year,))
    return cursor.fetchall()

def log_query(cursor, query_type, query_text):
    cursor.execute("""
        INSERT INTO popular_queries (query_type, query_text)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
        query_count = query_count + 1,
        last_queried = CURRENT_TIMESTAMP
    """, (query_type, query_text))

def get_popular_queries(cursor):
    cursor.execute("""
        SELECT query_type, query_text, query_count
        FROM popular_queries
        ORDER BY query_count DESC
        LIMIT 10
    """)
    return cursor.fetchall()
