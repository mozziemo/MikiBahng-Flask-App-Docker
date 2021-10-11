from textblob import TextBlob
from bs4 import BeautifulSoup
import requests

import pandas as pd     
import numpy as np
import re


def google_news_query(search_term='President Biden'):
    """
    # Google News Search    
        - Args: search_term
        - Returns: headlins_clean
    """
    # search_term = 'President Biden'
    search_term = search_term.replace(' ', '+')

    google_search_url = f'https://news.google.com/search?q={search_term}&hl=en-US&gl=US&ceid=US:en'

    PC_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
    headers = {"user-agent" : PC_USER_AGENT}

    response = requests.get(google_search_url, headers=headers)
    # print(f'response.status_code = {response.status_code}')
    print(f'type(response.text) = {type(response.text)}')

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        # print(soup.prettify())
        a_tags = soup.find_all('a', class_='DY5T1d')
        
        headlines = []
        for i in range(len(a_tags)):
            # print(a_tags[i].text)
            headlines.append(a_tags[i].text)
        print(headlines)
        print('********************')

        headlines_clean = []
        for headline in headlines:
            headlines_clean.append(" ".join(re.findall("[a-zA-Z]+", headline)))
        return headlines_clean  

    else:
        # print(f'response.status_code == {response.status_code}')
        pass


def sentiment_analysis(clean_text_list):
    """
    # Sentiment analysis for text input (eg, clean text from Google News Search results)    
        - Args: clean_text_list
        - Returns: data_table, positive_count, neutral_count, negative_count,
                   sentiment_score_average, sentiment_overall
    """
        
    score_list = []
    sentiment_list = []
    data = pd.DataFrame()

    for line in clean_text_list:
        tb = TextBlob(line)
        sentiment_score = tb.sentiment.polarity
        score_list.append(sentiment_score)
        # sentiment evaluation for each line of the text input
        if sentiment_score > 0:
            sentiment = 'positive'
        elif sentiment_score < 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        sentiment_list.append(sentiment)

    score_array = np.array(score_list).astype(np.float)
    sentiment_array = np.array(sentiment_list)

    sentiment_score_average = np.average(score_array)

    # Overall sentiment evaluation	
    if sentiment_score_average > 0:
        sentiment_overall = 'Positive'
    elif sentiment_score_average < 0:
        sentiment_overall = 'Negative'
    else:
        sentiment_overall = 'Neutral'
    
    data['clean_text'] = np.array(clean_text_list).astype(str)
    data['SA_score'] = score_array
    data['Sentiment'] = sentiment_array
    data_table = data[['clean_text','SA_score','Sentiment']].rename(columns = {
        'clean_text' : 'Text', 'SA_score' : 'Polarity', 'Sentiment' : 'Sentiment'})

    # print(data_table.head())

#     with pd.option_context('display.max_colwidth', -1): 
#         data_to_show = data_table[1:11].to_html(classes='bluetable')

    positive_count = len(data[data['SA_score']>0])
    negative_count = len(data[data['SA_score']<0])
    neutral_count = len(data[data['SA_score']==0])

    # total = positive_count + negative_count + neutral_count
    
    # positive_rate = float(positive_count)/total
    # negative_rate = float(negative_count)/total
    # neutral_rate = float(neutral_count)/total

    # print(f'positive_rate = {100.0*positive_rate:.1f} %')
    # print(f'negative_rate = {100.0*negative_rate:.1f} %')
    # print(f'neutral_rate = {100.0*neutral_rate:.1f} %')
    
    return data_table, positive_count, neutral_count, negative_count, sentiment_score_average, sentiment_overall


if __name__ == '__main__':

    ## Google News Search
    search_term = 'Amazon'
    # search_term = input("Type Search Term for google news query: ")
    clean_headlines = google_news_query(str(search_term))
    data_df, positive_count, neutral_count, negative_count, sentiment_score_average, sentiment_overall = sentiment_analysis(clean_headlines)

    total = positive_count + negative_count + neutral_count
    
    positive_rate = float(positive_count)/total
    negative_rate = float(negative_count)/total
    neutral_rate = float(neutral_count)/total

    print(f'positive_rate = {100.0*positive_rate:.1f} %')
    print(f'neutral_rate = {100.0*neutral_rate:.1f} %')    
    print(f'negative_rate = {100.0*negative_rate:.1f} %')

    print(f'sentiment_score_average = {sentiment_score_average:.2f}')
    print(f'sentiment_overall = {sentiment_overall}')

    print(data_df.head(10))