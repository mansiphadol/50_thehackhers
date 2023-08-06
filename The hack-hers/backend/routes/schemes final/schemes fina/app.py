from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        language_choice = request.form.get('language_choice')
        keyword = request.form.get('keyword')
        url = f"https://labour.gov.in/search/node/{keyword}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            about_right_container = soup.find("div", class_="aboutRightContainer")
            if about_right_container:
                search_results = about_right_container.find_all("li", class_="search-result")
                results = []
                for result in search_results:
                    h3_title = result.find("h3", class_="title")
                    if h3_title:
                        link = h3_title.a["href"]
                        title_text = h3_title.a.get_text(strip=True)
                        title_text_translated = translator.translate(title_text, dest=language_choice).text
                        results.append((title_text_translated, link))

            return render_template('index.html', results=results)
        else:
            error_message = f"Failed to fetch URL. Status code: {response.status_code}"
            return render_template('index.html', error_message=error_message)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

