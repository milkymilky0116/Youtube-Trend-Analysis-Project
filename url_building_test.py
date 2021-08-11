from flask import Flask, url_for
app = Flask(__name__)


@app.route('/')
def index():
    pass


@app.route('/video')
def video():
    pass


@app.route('/video/<videoid>')
def detail(videoid):
    pass


with app.test_request_context():
    print(url_for('index'))
    print(url_for('video'))
    print(url_for('video', next='/'))
    print(url_for('detail', videoid='11111'))

    if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True, port=9999)
