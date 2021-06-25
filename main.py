import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCKS_API_KEY = "API_KEY"
NEWS_API_KEY = "API_KEY"
TWILIO_SID = "TWILIO_SID"
TWILIO_TOKEN = "TWILIO_TOKEN"
PHONE_NUMBER = "TWILIO_PH_NO"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCKS_API_KEY
}

url = f'https://www.alphavantage.co/query'
r = requests.get(url, params=parameters)
data = r.json()

date_wise_stockList = [values for (i, values) in data["Time Series (Daily)"].items()]

first_price = float(date_wise_stockList[0]["4. close"])
second_price = float(date_wise_stockList[2]["4. close"])

change_percentage = round((first_price - second_price) / first_price * 100, 2)

stock_change = ""

if change_percentage >= 5:
    stock_change += f"🔺{change_percentage}%"
else:
    stock_change += f"🔻{change_percentage}%"

news_url = "https://newsapi.org/v2/top-headlines"

news_parameters = {
    "apiKey": NEWS_API_KEY,
    # "q": COMPANY_NAME,
    "country": "us",
    "category": "business",
}

news_response = requests.get(news_url, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()
first_three_news = news_data["articles"][0:3]
print(len(first_three_news))

account_sid = TWILIO_SID
auth_token = TWILIO_TOKEN
client = Client(account_sid, auth_token)

message_list = [f"{STOCK}: {stock_change}" for i in first_three_news]

for message_data in message_list:
    # body_text = f"{STOCK}: {stock_change}\nHeadline: {i['title']}\nBrief: {i['description']}"
    # print(body_text)

    message = client.messages.create(
        body=message_data,
        from_=PHONE_NUMBER,
        to="NUMBER_TO_SEND")
