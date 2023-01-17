from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.g8d0ssb.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

# DB연결과 크롤링 패키지 임포트!

@app.route('/')
def home():
    return render_template('index.html')

# ----------------------------------------------------------

@app.route("/page", methods=["POST"])
def page_post():
    url_receive = request.form['url_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    page_list = list(db.pages.find({}, {'_id': False}))
    count = len(page_list) + 1

    doc = {
        'url': url_receive,
        'title': title,
        'image': image,
        'desc': desc,
        'num': count
    }

    db.pages.insert_one(doc)

    return jsonify({'msg': '저장 완료'})


@app.route("/page", methods=["GET"])
def page_get():
    page_list = list(db.pages.find({}, {'_id': False}))
    return jsonify({'pages': page_list})


@app.route("/delete/page", methods=["POST"])
def delete_page():
    num_receive = request.form['num_give']

    db.pages.delete_one({'num': int(num_receive)})

    return jsonify({'msg': '삭제 완료'})

# ----------------------------------------------------------


@app.route("/video", methods=["POST"])
def video_post():
    url_receive = request.form['url_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('head > title').text
    image = soup.select_one('meta[property="og:image"]')['content']

    video_list = list(db.videos.find({}, {'_id': False}))
    count = len(video_list) + 1

    doc = {
        'url': url_receive,
        'title': title,
        'image': image,
        'num': count
    }

    db.videos.insert_one(doc)

    return jsonify({'msg': '저장 완료'})



@app.route("/video", methods=["GET"])
def video_get():
    video_list = list(db.videos.find({}, {'_id': False}))
    return jsonify({'videos': video_list})


@app.route("/delete/video", methods=["POST"])
def delete_video():
    num_receive = request.form['num_give']

    db.videos.delete_one({'num': int(num_receive)})

    return jsonify({'msg': '삭제 완료'})


# ----------------------------------------------------------

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


# github에 업데이트된 파일 push하는 방법 연습하기 위해 작성하는 주석!