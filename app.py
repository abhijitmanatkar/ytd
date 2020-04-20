from flask import Flask, request, render_template, url_for
import requests
import pafy

app = Flask(__name__)

def format_duration(duration):
    if duration < 60:
        return str(duration)
    if duration < 3600:
        return str(duration//60) + ":" + str(duration%60)
    else:
        return str(duration//3600) + ":" + format_duration(duration%3600)

def format_size(size):
    if size < 1024:
        return str(size) + " B"
    if size < 1024*1024:
        tmp = int((size/1024)*100)
        return str(tmp // 100) + "." + str(tmp % 100) + " KB"
    if size < 1024*1024*1024:
        tmp = int((size/(1024*1024))*100)
        return str(tmp // 100) + "." + str(tmp % 100) + " MB"
    else:
        tmp = int((size/(1024*1024*1024))*100)
        return str(tmp // 100) + "." + str(tmp % 100) + " GB"


@app.route("/", methods=['POST', 'GET'])
def main_page():
    if request.form:
        yt_link = str(request.form['link'])
        try:
            if requests.get(yt_link).status_code < 400:
                print("Video Exists")
                vid = pafy.new(yt_link)
                return render_template("main.html", vid=vid, fd=format_duration, fs=format_size)
        except Exception as e:
            print("An exception occurred")
            print(e)
            return render_template("main.html", vid=None)

    return render_template("main.html", vid=None)

if __name__ == '__main__':
    app.run(port=5001,debug=True)
