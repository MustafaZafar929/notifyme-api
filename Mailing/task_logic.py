import os 
import requests as request 
import httpx


from typing import List, Tuple
from datetime import date
from mailing import send_mail
from redis_cache import get_catched_news , set_cache_news
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.environ.get("API_KEY")

current_date = date.today()
formatted_date = current_date.strftime("%A, %d %B %Y")

async def global_news(user_list: List[Tuple]):
   cache_key = f'global_news : {current_date}'
   cached_data = get_catched_news(cache_key)
   news_body = ""

   if cached_data:
    news_body = cached_data

   else:
    response =  await fetch_news()
    if response.status_code == 200:
        try:
            data = response.json()
            
            top_news_list = data.get("top_news", [])
            articles = top_news_list[0].get("news", [])[:5] if top_news_list else []

            if not articles:
                news_body = "📰 No news articles available today."
            else:
                news_body = f"🗞️ Top Global News for {formatted_date}\n\n"
                for i, article in enumerate(articles, 1):
                    title = article.get("title", "No Title")
                    link = article.get("url", "#")
                    description = article.get("summary", article.get("text", "")).strip()
                    news_body += (
                        f"{i}. {title}\n"
                        f"{description}\n"
                        f"🔗 Read more: {link}\n\n"
                    )
                set_cache_news(cache_key=cache_key , news_data=news_body)
        except Exception as e:
            news_body = f"❌ Failed to parse news: {e}"

    else:
        news_body = f"⚠️ Failed to fetch news. Status code: {response.status_code}"

    for row in user_list:
        email = row[0]
        subject = f"🌍 Global News - {formatted_date}"
        print(f"Sending email to {email}")
        send_mail.delay(receiver_address=email, subject=subject, body=news_body)
    
 

 
async def fetch_news():
     url = f"https://api.worldnewsapi.com/top-news?source-country=us&language=en&date"
     headers = {
        'x-api-key': API_KEY
    }
    
     async with httpx.AsyncClient() as client:
         response = await client.get(url , headers=headers)
         return response