import requests
import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
alpha_api = "SXACC77MJRIDFDOJ"
news_api = "dd1fa253170a48048d8d7950c45bd90c"

# -------------------------Get data from stock price api-------------------------

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": alpha_api,
    "sortBy": "relevancy"

}

response = requests.get("https://www.alphavantage.co/query", params=stock_params)
response.raise_for_status()
data_index = list(response.json()["Time Series (Daily)"])

last_data = response.json()["Time Series (Daily)"][data_index[0]]
two_day_data = response.json()["Time Series (Daily)"][data_index[1]]

last_close = float(last_data["4. close"])
two_day_close = float(two_day_data["4. close"])

performance = (last_close / two_day_close - 1) * 100

# ---------------------------News response--------------------------#
news_params = {
        "apiKey": news_api,
        "q": COMPANY_NAME,
        "from": data_index[1],
        "to": data_index[0]
    }

news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
news_response.raise_for_status()
news_data = news_response.json()["articles"][:2]
# latest_news_title = news_data[0]["title"]
# latest_news_brief = news_data[0]["content"]



# -----------------------------Generate news------------------------------#
if performance > 0:
    message = client.messages.create(
        body=f"{STOCK} ⬆️ by {round(performance, 4)}%\n"
             f"{latest_news_title}\n"
             f"{latest_news_brief}",
        from_='+18163071223',
        to='+85269738381',
    )
    print(message.sid)

else:
    message = client.messages.create(
        body=f"{STOCK} ⬇️ by {round(performance, 4)}%\n\n"
             f"Title: {news_data[0]['title']}\n\n"
             f"Brief: {news_data[0]['content']}\n\n"
             f"Title: {news_data[1]['title']}'\n\n"
             f"Brief: {news_data[1]['content']}",
        from_='+18163071223',
        to='+85269738381',
    )

    print(message.sid)



# -------------------------Get data from news api-------------------------
# news_params = {
#     "apiKey": news_api,
#     "q": COMPANY_NAME,
#     "from": data_index[1],
#     "to": data_index[0]
# }
#
# news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
# news_response.raise_for_status()
# news_data = news_response.json()["articles"][:2]
#
# last_news = (news_data[0]["title"], news_data[0]["content"])
# previous_news = (news_data[1]["title"], news_data[1]["content"])



















## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

