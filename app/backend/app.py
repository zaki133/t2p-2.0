from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test')
def test():
    #Use GET method from postman or curl when contacting to test
    try:
        # Something happens here, will be added at a later date
        return jsonify("successful"), 200
    except Exception as e:
        return f"Error in processing: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

