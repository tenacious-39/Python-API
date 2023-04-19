from flask import Flask, jsonify

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/codechef/<string:ccUsername>')
def codechef(ccUsername):
    urlcc = "https://www.codechef.com/users/" + ccUsername
    try:
        req = requests.get(urlcc)
        doc = BeautifulSoup(req.content, "html.parser")
        problems = doc.find(class_="problems-solved")
        fullySolved = problems.find("h5").get_text()
        fullySolved = fullySolved.replace("Fully Solved (", "")
        fullySolved = fullySolved.replace(")", "")
        ratingNum = doc.find(class_="rating-number").get_text()
        starRating = doc.find(class_="rating").get_text()
        if ratingNum[0] == '0':
            ratingNum = "0"
        return jsonify(isValid=True, username=ccUsername, problems=fullySolved, rating=ratingNum, star=starRating)
    except:
        return jsonify(isValid=False)


@app.route('/codeforces/<string:cfUsername>')
def codeforces(cfUsername):
    urlcf = "https://codeforces.com/profile/" + cfUsername
    try:
        req = requests.request("GET", urlcf)
        doc = BeautifulSoup(req.content, "html.parser")
        ratingInfo = doc.find(class_="info")
        #ratingInfo = ratingInfo.get_text()
        print("printing")
        print(ratingInfo)
        return jsonify(isValid=True)
    except:
        return jsonify(isValid=False)

if __name__=="__main__":
    app.run(debug=True)