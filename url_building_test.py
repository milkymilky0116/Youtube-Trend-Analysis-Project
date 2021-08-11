from flask import Flask, url_for
from flask.templating import render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/video')
def video():
    return render_template("video-dump.html")


@app.route('/video/<videoid>')
def detail(videoid):
    return render_template("video-detail.html", value=videoid)


with app.test_request_context():
    print(url_for('index'))
    print(url_for('video'))
    print(url_for('video', next='/'))
    print(url_for('detail', videoid='11111'))

    if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True, port=9999)
