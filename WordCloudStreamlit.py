#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import bs4
import requests

# st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Simple WordCloud App for BIA')

# Header of the streamlit application
st.sidebar.header("Select Link")

# URL of the streamlit app, user to input this
URL = st.sidebar.text_input('Enter the URL to get text', value='https://en.wikipedia.org/wiki/Chandrayaan-3')

# Get number of words as the input from user
st.sidebar.header("Select No. of words you want to display")
words = st.sidebar.slider("No. of words", 0, 1000, 100)


# Define functions
def get_text_from_web_url(target_url):
    """
        Function to get the text from the target URL.
        This will get all the text wrapped in <p> tag of the HTML
    """
    response = requests.get(target_url)

    if response is not None:
        html = bs4.BeautifulSoup(response.text, 'html.parser')
        
        text_list = html.select("p")
        
        full_text = '\n'.join([ raw_text.text for raw_text in text_list])
        
        return full_text
    else:
        return "No Text Found"
 

# Define word count function 
def get_word_count_from_text(text_data):
    """
        Function to get the word count dictionary from the text data
    """
    word_dict = {}

    for word in text_data.split(" "):
        word = str(word).lower().replace('"', "").replace("\n", "").replace("\t", "").replace("'", "")
        word_dict[word] = word_dict.get(word, 0) + 1
    
    return word_dict
    
# Function to get n frequent words from the word count dict
def get_top_n_words(word_dict, n=10):
    top_words_dict = {}
    for k, v in sorted(word_dict.items(), key=lambda x:x[1], reverse=True)[0:n]:
        top_words_dict[k] = v
    
    return top_words_dict

# Check if URL is not none then call the function to get the text data 
if URL is not None:
    text_data = get_text_from_web_url(URL)
    st.subheader("Word Cloud Plot")
    
    # Get dictionary of words from the text data
    word_dict = get_word_count_from_text(text_data)
    
    #using stopwords to remove extra words
    stopwords = set(STOPWORDS)
    for stopword in stopwords:
        if stopword in word_dict:
            del word_dict[stopword]
    
    # Get top 10 words
    top_words_dict = get_top_n_words(word_dict)
    
    # Generate word cloud
    wordcloud = WordCloud(background_color = "white", max_words = words, stopwords = stopwords).generate_from_frequencies(word_dict)
    # wordcloud = WordCloud(background_color = "white", max_words = words,stopwords = stopwords).generate(text_data)

# Show the plot on streamlit
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis("off")
plt.show()
st.pyplot(plt)

st.subheader("Top 10 words")
st.write(top_words_dict)
