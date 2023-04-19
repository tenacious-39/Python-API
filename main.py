from flask import Flask, jsonify

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Codechef route
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


# Codeforces route
@app.route('/codeforces/<string:cfUsername>')
def codeforces(cfUsername):
    urlcf = "https://codeforces.com/profile/" + cfUsername
    try:
        req = requests.get(urlcf)
        doc = BeautifulSoup(req.content, "html.parser")
        ratingInfo = doc.find(class_="info").find("ul").find("li").find("span")
        ratingInfo = ratingInfo.get_text()
        ratingCategory = doc.find(class_="user-rank").find("span").get_text()
        fullySolved = doc.find(class_="_UserActivityFrame_counterValue").get_text()
        totalContests = findTotalContests(cfUsername)
        print(totalContests)
        return jsonify(isValid=True, rating=ratingInfo, category=ratingCategory, problems=fullySolved, contest=totalContests)
    except:
        return jsonify(isValid=False)

def findTotalContests(cfUsername):
    urlcfContest = "https://codeforces.com/contests/with/"+cfUsername
    try:
        req = requests.get(urlcfContest)
        doc = BeautifulSoup(req.content, "html.parser")
        totalContests = doc.find(class_="user-contests-table").find("tbody").find("tr").find("td").get_text()
        return totalContests
    except:
        return "0"
    


# leetcode route
@app.route('/leetcode/<string:lcUsername>')
def leetcode(lcUsername):
    urllc = "https://leetcode.com/" + lcUsername
    try:
        req = requests.get(urllc)
        doc = BeautifulSoup(req.content, "html.parser")
        rating = doc.select_one("#__next > div > div.mx-auto.w-full.grow.p-4.md\:mt-0.md\:max-w-\[888px\].md\:p-6.lg\:max-w-screen-xl.mt-\[50px\] > div > div.w-full.lc-lg\:max-w-\[calc\(100\%_-_316px\)\] > div:nth-child(2) > div.bg-layer-1.dark\:bg-dark-layer-1.rounded-lg.mt-4.flex.h-\[200px\].w-full.min-w-\[200px\].p-4.lc-lg\:mt-0.lc-xl\:hidden > div > div.relative.min-h-\[53px\].text-xs > div > div:nth-child(1) > div.text-label-1.dark\:text-dark-label-1.flex.items-center.text-2xl")
        if rating is None:
            rating = "invalid"
        else:
            rating = rating.string

        fullySolved = doc.select_one("#__next > div > div.mx-auto.w-full.grow.p-4.md\:mt-0.md\:max-w-\[888px\].md\:p-6.lg\:max-w-screen-xl.mt-\[50px\] > div > div.w-full.lc-lg\:max-w-\[calc\(100\%_-_316px\)\] > div.flex.w-full.flex-col.space-x-0.space-y-4.lc-xl\:flex-row.lc-xl\:space-y-0.lc-xl\:space-x-4 > div.min-w-max.max-w-full.w-full.flex-1 > div > div.mx-3.flex.items-center.lc-xl\:mx-8 > div.mr-8.mt-6.flex.min-w-\[100px\].justify-center > div > div > div > div.text-\[24px\].font-medium.text-label-1.dark\:text-dark-label-1")
        hardSolved= doc.select_one("#__next > div > div.mx-auto.w-full.grow.p-4.md\:mt-0.md\:max-w-\[888px\].md\:p-6.lg\:max-w-screen-xl.mt-\[50px\] > div > div.w-full.lc-lg\:max-w-\[calc\(100\%_-_316px\)\] > div.flex.w-full.flex-col.space-x-0.space-y-4.lc-xl\:flex-row.lc-xl\:space-y-0.lc-xl\:space-x-4 > div.min-w-max.max-w-full.w-full.flex-1 > div > div.mx-3.flex.items-center.lc-xl\:mx-8 > div.flex.w-full.flex-col.space-y-4.lc-xl\:max-w-\[228px\] > div:nth-child(3) > div.flex.w-full.items-end.text-xs > div.flex.flex-1.items-center > span.mr-\[5px\].text-base.font-medium.leading-\[20px\].text-label-1.dark\:text-dark-label-1")
        mediumSolved= doc.select_one("#__next > div > div.mx-auto.w-full.grow.p-4.md\:mt-0.md\:max-w-\[888px\].md\:p-6.lg\:max-w-screen-xl.mt-\[50px\] > div > div.w-full.lc-lg\:max-w-\[calc\(100\%_-_316px\)\] > div.flex.w-full.flex-col.space-x-0.space-y-4.lc-xl\:flex-row.lc-xl\:space-y-0.lc-xl\:space-x-4 > div.min-w-max.max-w-full.w-full.flex-1 > div > div.mx-3.flex.items-center.lc-xl\:mx-8 > div.flex.w-full.flex-col.space-y-4.lc-xl\:max-w-\[228px\] > div:nth-child(2) > div.flex.w-full.items-end.text-xs > div.flex.flex-1.items-center > span.mr-\[5px\].text-base.font-medium.leading-\[20px\].text-label-1.dark\:text-dark-label-1")
        easySolved= doc.select_one("#__next > div > div.mx-auto.w-full.grow.p-4.md\:mt-0.md\:max-w-\[888px\].md\:p-6.lg\:max-w-screen-xl.mt-\[50px\] > div > div.w-full.lc-lg\:max-w-\[calc\(100\%_-_316px\)\] > div.flex.w-full.flex-col.space-x-0.space-y-4.lc-xl\:flex-row.lc-xl\:space-y-0.lc-xl\:space-x-4 > div.min-w-max.max-w-full.w-full.flex-1 > div > div.mx-3.flex.items-center.lc-xl\:mx-8 > div.flex.w-full.flex-col.space-y-4.lc-xl\:max-w-\[228px\] > div:nth-child(1) > div.flex.w-full.items-end.text-xs > div.flex.flex-1.items-center > span.mr-\[5px\].text-base.font-medium.leading-\[20px\].text-label-1.dark\:text-dark-label-1")
        return jsonify(isValid=True, rating=rating, total_problems=fullySolved.string,
                       hard_problems=hardSolved.string, medium_problems=mediumSolved.string, easy_problems=
                       easySolved.string)
    except:
        return jsonify(isValid=False)
    

@app.route('/gfg/<string:gfgUsername>')
def gfg(gfgUsername):
    urlgfg = "https://auth.geeksforgeeks.org/user/" + gfgUsername
    try:
        req = requests.get(urlgfg)
        doc = BeautifulSoup(req.content, "html.parser")
        problems=doc.find_all(class_="score_card_value")
        problems = problems[1].get_text()
        problemLevels = doc.find(class_="solved_problem_section").find_all(class_="tab")

        easySolved=problemLevels[2].get_text()
        mediumSolved=problemLevels[3].get_text()
        hardSolved=problemLevels[4].get_text()
        return jsonify(isValid=True, total_problems=problems, easy_problems=easySolved, medium_problems=
                       mediumSolved, hard_problems=hardSolved)
    except:
        return jsonify(isValid=False)



if __name__=="__main__":
    app.run(debug=True)