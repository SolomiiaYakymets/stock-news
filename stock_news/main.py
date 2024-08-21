import requests
import datetime
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_URL = "https://www.alphavantage.co/query"
NEWS_URL = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "<API_KEY>"
NEWS_API_KEY = "<API_KEY>"

TWILIO_SID = "<SID>"
TWILIO_AUTH_TOKEN = "<AUTH_TOKEN>"

TODAY = datetime.date.today()

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

stock_response = requests.get(STOCK_URL, params=stock_params)
stock_response.raise_for_status()
data = stock_response.json()["Time Series (Daily)"]

yesterday = TODAY - datetime.timedelta(days=1)
day_before_yesterday = yesterday - datetime.timedelta(days=1)

yesterday_closing_price = float(data[str(yesterday)]["4. close"])
day_before_yesterday_closing_price = float(data[str(day_before_yesterday)]["4. close"])

difference = yesterday_closing_price - day_before_yesterday_closing_price
up_or_down = None
if difference > 0:
    up_or_down = "🔺"
else:
    up_or_down = "🔻"

percentage_change = round(abs((difference / day_before_yesterday_closing_price) * 100))
is_changed = False
if percentage_change > 5:
    is_changed = True

if is_changed:
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }
    news_response = requests.get(NEWS_URL, params=news_parameters)
    news_response.raise_for_status()
    print(news_response.json())
    news_data = news_response.json()["articles"]

    message_info = f"TSLA: {up_or_down} {percentage_change}%\n"
    for num in range(3):
        message_info += f"Headline: {news_data[num]["title"]}\nBrief: {news_data[num]["description"]}\n\n"

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message_info,
        from_="+12565789358",
        to="<PHONE_NUMBER>",
    )
