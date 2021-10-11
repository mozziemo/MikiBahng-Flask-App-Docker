import os
import time

from flask import Flask, render_template, request, url_for
import requests

import pandas as pd
import numpy as np

import pygal
from pygal.style import Style
from pygal.style import DefaultStyle

from mymodules import text_analysis

app = Flask(__name__)

@app.route('/')
def welcome():
	return render_template('welcome.html')

@app.route('/google-news-app/select-search-term')
def select_google_news_search_term():
	return render_template('select_google_news_search_term.html')

@app.route('/google-news-app/sentiment-analysis', methods=['POST'])
def google_news_sentiment_analysis():
	try:
		if request.method == 'POST':
		    search_term = request.form['keyword']
		else:
		    search_term = 'Tesla'

		clean_headlines = text_analysis.google_news_query(str(search_term))

		data_df, positive_count, neutral_count, negative_count, sentiment_score_average, sentiment_overall = text_analysis.sentiment_analysis(clean_headlines)

		with pd.option_context('display.max_colwidth', -1):
			data_count = len(data_df)
			data_to_show = data_df[1:11].to_html(classes='bluetable') 

		total = positive_count + negative_count + neutral_count

		# positive_rate = f'{100.0*float(positive_count)/total:.2f}'
		# negative_rate = f'{100.0*float(negative_count)/total:.2f}'
		# neutral_rate = f'{100.0*float(neutral_count)/total:.2f}'

		positive_rate = round(100.0*float(positive_count)/total, 1)
		negative_rate = round(100.0*float(negative_count)/total, 1)
		neutral_rate = round(100.0*float(neutral_count)/total, 1)

		#custum style for pygal charts
		custom_style = Style(colors=('#0b7eea', '#47b752', '#ff1119'))
		# pygal bar chart
		bar_chart = pygal.HorizontalBar(style=custom_style, height=300, width=700, legend_at_bottom=True, legend_at_bottom_columns=3)
	#	bar_chart.title = 'Distribution of News Headlines for the search term: {}'.format(search_term)
		bar_chart.title = '(Distribution of News Headlines in Count)'
		bar_chart.add('Positive Headlines', positive_count)
		bar_chart.add('Neutral Headlines', neutral_count)
		bar_chart.add('Negative Headlines', negative_count)
		bar_chart = bar_chart.render_data_uri()

		# pygal pie chart
		pie_chart = pygal.Pie(style=custom_style, margin_left=250, margin_right=50, margin_top=25,margin_bottom=25, height=450, width=700,
								legend_box_size=24, legend_font_size=24, 
								legend_at_bottom=True, legend_at_bottom_columns=3,
								)

		pie_chart.title = '(Distribution of News Headlines in %)'
		pie_chart.add('Positive', positive_rate)
		pie_chart.add('Neutral', neutral_rate)
		pie_chart.add('Negative', negative_rate)
		pie_chart = pie_chart.render_data_uri()
		return render_template('google_news_sentiment_analysis.html', data_count=data_count, data_table=data_to_show, search_term=search_term, sentiment_score_average=round(sentiment_score_average, 5), sentiment_overall=sentiment_overall, positive_rate=positive_rate, negative_rate=negative_rate, neutral_rate=neutral_rate, bar_chart=bar_chart, pie_chart = pie_chart)

	except Exception as e:
		time.sleep(1)
		print(repr(e))
		return render_template("google_news_search_term_error.html", error=repr(e))


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True) # for development
	# app.run(host='0.0.0.0', port=80, debug=Flase) # for deployment

