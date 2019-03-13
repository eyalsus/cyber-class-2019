from flask import Flask, request
app = Flask(__name__)

@app.route('/dropzone', methods=['POST'])
def hello():
    print (request.get_data())
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)