import os
import asyncio
import logging
from datetime import datetime

import dotenv
import mysql.connector
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Mailing.task_logic import global_news

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)

def get_connection_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
    )

async def get_user_table():
    connection = None
    cursor = None
    try:
        current_time = datetime.now().time().strftime('%H:%M:%S')
        current_date = datetime.now().date()
        connection = get_connection_db()
        cursor = connection.cursor()
        
        query = """
            SELECT users.email, news_preferences.notification_time
            FROM news_preferences
            INNER JOIN users ON news_preferences.user_id = users.id
            LEFT JOIN notification_history ON users.id = notification_history.user_id 
                AND DATE(notification_history.sent_at) = %s
            WHERE news_preferences.notification_time <= %s
            AND notification_history.id IS NULL;
        """
        cursor.execute(query, (current_date, current_time))
        result = cursor.fetchall()

        if result:
            await global_news(user_list=result)
            history_query = """
                INSERT INTO notification_history (user_id, sent_at)
                SELECT users.id, NOW()
                FROM users
                WHERE users.email IN %s
            """
            cursor.execute(history_query, (tuple(email for email, _ in result),))
            connection.commit()
            logging.info(f"Notifications sent for {len(result)} users at {current_time}")
        else:
            logging.info(f"No users to notify at {current_time}")

    except Exception as e:
        logging.exception(f"Error in get_user_table: {str(e)}")
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if connection:
            try:
                connection.close()
            except Exception:
                pass

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(get_user_table, 'interval', minutes=10)
    scheduler.start()
    logging.info("Scheduler started: running get_user_table every 10 minutes")

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Shutting down scheduler...")
        scheduler.shutdown()
        logging.info("Scheduler shut down.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        logging.exception("Fatal error running scheduler")




