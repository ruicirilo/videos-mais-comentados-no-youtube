from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    url = "https://kworb.net/youtube/topvideos_comments.html"
    response = requests.get(url)
    response.encoding = 'utf-8'  # Forçar a codificação para UTF-8
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontre a tabela
    table = soup.find('table')
    rows = table.find_all('tr')

    # Extraia os dados
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols_text = [ele.text.strip() for ele in cols]

        # Pegue o link correto do vídeo
        link_tag = row.find('a')
        if link_tag and 'href' in link_tag.attrs:
            video_href = link_tag['href']  # Exemplo: 'video/kJQP7kiw5Fk.html'
            # Extrair o ID do vídeo removendo 'video/' e '.html'
            video_id = video_href.replace('video/', '').replace('.html', '')
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            cols_text.append(f'<a href="{video_url}" target="_blank">Ver no YouTube</a>')

        if cols_text:
            data.append(cols_text)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)




