#final 
import requests
from bs4 import BeautifulSoup
from IPython.display import display, HTML

from urllib.parse import urljoin
from flask import Flask, render_template, request
from googletrans import Translator
import os
from flask import Flask, render_template

app = Flask(__name__)

url = 'https://junoon.me/trainings'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all 'img' elements with class 'd-width-100'
images = soup.find_all('img', class_='d-width-100')

# Find all 'a' elements with class 'd-display-inline-block' and 'd-width-100'
anchors = soup.find_all('a', class_='d-display-inline-block d-width-100')

# Display one image and one anchor (if available) in sequence
for img, anchor in zip(images, anchors):
    src = img.get('src')
    display(HTML(f'<img src="{src}" width="200">'))

    href = anchor.get('href')
    text = anchor.text.strip()
    display(HTML(f'<a href="{href}" target="_blank">{text}</a>'))
    
    print()  # Add a blank line for separation
