from flask import Flask,render_template,request
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

# 如果访问 /index 则返回和index()函数相同的模板，或者返回index()函数
@app.route("/index")
def home():
    # return render_template("index.html")
    return index()

@app.route("/movie")
def movie():
    datalist=[]
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    sql="select * from movies250"
    data=cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    return render_template("movie.html",movies=datalist)

@app.route("/score")
def score():
    score=[] #存放分数
    num=[]  #存放每个分数的数量
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    sql="select score,count(score) from movies250 group by score"
    data=cur.execute(sql)
    for item in data:
        score.append(item[0])
        num.append(item[1])
    cur.close()
    con.close()
    return render_template("score.html",score=score,num=num)

@app.route("/word")
def word():
    return render_template("word.html")

@app.route("/team")
def team():
    return render_template("team.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=3000)