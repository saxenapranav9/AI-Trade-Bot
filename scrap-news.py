import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

uber_url = 'https://finviz.com/quote.ashx?t=UBER'
accenture_url = 'https://finviz.com/quote.ashx?t=ACN'
amazon_url = 'https://finviz.com/quote.ashx?t=AMZN'
dell_url = 'https://finviz.com/quote.ashx?t=DELL'
apple_url = 'https://finviz.com/quote.ashx?t=AAPL'
verizon_url = 'https://finviz.com/quote.ashx?t=VZ'
cisco_url = 'https://finviz.com/quote.ashx?t=CSCO'
fb_url = 'https://finviz.com/quote.ashx?t=FB'

url_list = [accenture_url,amazon_url,dell_url,apple_url,verizon_url,cisco_url,fb_url,uber_url]

def scrap_news():
    
    parsed_news = []
    from datetime import date, datetime,timedelta
    today = date.today()
    #When you misses to collect the previous day news
    # today = date.today() - timedelta(days=1 )

    # NLTK VADER for sentiment analysis
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    # New words and values
    new_words = {
        'crushes': 10,
        'beats': 5,
        'misses': -5,
        'trouble': -10,
        'falls': -100,
    }
    # Instantiate the sentiment intensity analyzer with the existing lexicon
    vader = SentimentIntensityAnalyzer()
    # Update the lexicon
    vader.lexicon.update(new_words)

    # Use these column names
    columns = ['ticker', 'date', 'time', 'headline']

    for url in url_list:

        r = requests.get(url,headers = headers)
        soup = BeautifulSoup(r.text,'html.parser')
 
        news = soup.find('table',{'id': 'news-table'})
        tr = news.findAll('tr')
                  
        for x in tr:

            text = x.get_text()

            date_scrape = x.td.text.split()
            headline = x.a.text

            if len(date_scrape) == 1:
                time = date_scrape[0]
            else:
                date = date_scrape[0]
                time = date_scrape[1]

            # Extract the ticker from the file name, get the string up to the 1st '_'  
            ticker = url.split('=')[1]
            # Append ticker, date, time and headline as a list to the 'parsed_news' list
            parsed_news.append([ticker, date, time, headline])

        # print(parsed_news[:10])    

        # Convert the list of lists into a DataFrame
        scored_news = pd.DataFrame(parsed_news, columns=columns)

        # Iterate through the headlines and get the polarity scores
        scores = scored_news['headline'].apply(vader.polarity_scores)

        # Convert the list of dicts into a DataFrame
        scores_df = pd.DataFrame.from_records(scores)

        # Join the DataFrames
        scored_news = scored_news.join(scores_df)

        # Convert the date column from string to datetime
        scored_news['date'] = pd.to_datetime(scored_news.date).dt.date
        # print(scored_news.tail())
    # DF TO EXCEL
    todays_news = scored_news[scored_news['date'] == today]
    directory='/Users/pranavsaxena/Desktop/Python/news-data/' + str(today) + '.xlsx'
    writer = ExcelWriter(directory)
    todays_news.to_excel(writer,'sentiment')
    writer.save()

scrap_news()  









































