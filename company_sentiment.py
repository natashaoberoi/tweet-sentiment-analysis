import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of 6 Big Tech Company Data")
st.sidebar.title("Sentiment Analysis of Big Tech Company Data")
st.markdown(" This application is a Streamlit dashboard used to visualize data about the sentiment of Tweets 🐦")

# input the correct data url
data_url = "/Users/natashaoberoi/Documents/Python projects/Tweets_sentiment/Bigtech.csv"


def polarity_to_sentiment(pol):
    # sorts polarity values into 5 sentiment bins
    pol = float(pol)
    if -1 <= pol < -0.6:
        return 'negative'
    elif -0.6 <= pol < -0.2:
        return 'slightly negative'
    elif -0.2 <= pol < 0.2:
        return 'neutral'
    elif 0.2 <= pol < 0.6:
        return 'slightly positive'
    else:
        return 'positive'


@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(data_url)
    # data cleaning
    data['created_at'] = pd.to_datetime(data['created_at'])
    sentiments = data['polarity'].apply(polarity_to_sentiment).to_frame()
    sentiments.rename(columns={'polarity': 'sentiment'}, inplace=True)
    data = pd.concat([data, sentiments], axis=1)
    return data


data = load_data()

if st.sidebar.checkbox("Show raw data", False):
    st.write(data)

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive','slightly positive','neutral','slightly negative','negative'),key='0')
st.sidebar.markdown('Tweet:')
st.sidebar.markdown(data.query('sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.subheader("Number of Tweets by Sentiment")
select1 = st.sidebar.selectbox('Visualization Type', ['Histogram','Pie chart'], key='1')
sentiment_count = data['sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.subheader("Number of tweets by sentiment")
    st.markdown("The sentiment, ranked as a polarity from -1 to 1, are sorted into the 5 categories seen in the plot:")
    if select1 == 'Histogram':
        fig_count = px.bar(sentiment_count,x='Sentiment',y='Tweets',color='Tweets',height=500)
        st.plotly_chart(fig_count)
    else:
        fig_count = px.pie(sentiment_count,values='Tweets',names='Sentiment')
        st.plotly_chart(fig_count)

st.sidebar.subheader("Breakdown Big Tech Company Tweets by Sentiment")
choice = st.sidebar.multiselect('Pick companies', ('Twitch','Youtube','Apple','Netflix','Amazon','Tesla', 'Nvidia'), key='2')
select2 = st.sidebar.selectbox('Visualization Type', ['Bar plot','Box plot'], key='5')



if len(choice) > 0:
    choice_data = data[data.file_name.isin(choice)]
    if select2 == 'Bar plot':
        # histfunc performs computation, facet creates more plots as more are added and split histograms by sentiment
        fig_choice = px.histogram(choice_data, x='file_name', y='sentiment', histfunc='count', color='sentiment',
                                  facet_col='sentiment', labels={'file_name':'Companies','sentiment':'Tweets'},
                                  height=600, width=800)
        st.plotly_chart(fig_choice)
    else:
        st.markdown("Sentiment is measured as polarity on a scale of -1 (negative) to +1 (positive)")
        fig_choice = px.box(choice_data, x="file_name", y="polarity", labels={'file_name':'Companies','sentiment':'Tweets'},
                            height=800, color='file_name')
        st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio("Display wordcloud for which sentiment?", ('positive','slightly positive','neutral',
                                                                            'slightly negative','negative'), key='3')

if not st.sidebar.checkbox("Hide", True, key='4'):
    st.subheader("Word cloud for %s sentiment" % (word_sentiment))
    df = data[data['sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    # STOPWORDS is just removing common words like articles and puncutation
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud)
    ax.axis("off")
    st.pyplot(fig)