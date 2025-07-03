import mysql.connector
import dotenv
import os
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler 

from Mailing.task_logic import global_news

dotenv.load_dotenv()

# DB Connection
def get_connection_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),  
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# Get user table and send global news
async def get_user_table():
    connection = get_connection_db()
    cursor = connection.cursor()
    cursor.execute("SELECT email, phone, notification_time FROM Global_News INNER JOIN Users on Global_News.user_id = Users.user_id WHERE Global_News.notification_time <= '14:30:00';")
    result = cursor.fetchall()
    
    if result:
        await global_news(user_list=result)  # Use 'await' for async function
        print('Result sent for mailing updated')

    cursor.close()
    connection.close()

# Ensure we have a running event loop
async def main():
    # Create and start the scheduler
    scheduler = AsyncIOScheduler()  # Use AsyncIOScheduler
    scheduler.add_job(get_user_table, 'interval', seconds=10)  # Schedule the async job every 10 seconds
    scheduler.start()

    # Run the event loop
    try:
        while True:
            
            await asyncio.sleep(1)  # This keeps the event loop running
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Shutdown scheduler gracefully
        print("Scheduler shut down.")

# Run the main function to start everything
if __name__ == "__main__":
    asyncio.run(main())  # Ensure that the event loop is running when the script starts
