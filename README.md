# tweet-sentiment-analysis
## Project Overview
This project uses Streamlit to create an interactive web application that visualizes sentiment analysis of tweets about six major tech companies. The dataset is sourced from Kaggle and includes sentiment data for tweets related to these companies. The application allows users to explore the sentiment distribution and trends for each company.

## Features
* Interactive Data Visualization: View sentiment analysis for tweets about six big tech companies.
* Company Selection: Select a specific company to view detailed sentiment analysis.
* Sentiment Distribution: Pie charts and bar charts displaying the distribution of sentiments (positive, neutral, negative).
* Word Cloud: Visualization of the most common words used in the tweets for each sentiment category.

## Requirements
* Python 3.8 or higher
* Streamlit
* Pandas
* Matplotlib
* Seaborn
* Wordcloud

## Setup
1. Clone the repository.
2. Download the dataset either from the repository or from the Kaggle dataset which can be found [here](https://www.kaggle.com/datasets/wjia26/big-tech-companies-tweet-sentiment). Keep it in the same folder as company_sentiment.py.
3. Run Streamlit from the command line
   ```
   streamlit run company_sentiment.py
   ```
4. Open your web browser and go to http://localhost:8501 to view the application.

## Acknowledgements
The dataset is provided by Kaggle and includes tweets about six major tech companies.
