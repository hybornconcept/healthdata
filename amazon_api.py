from flask import Flask, jsonify

# init app
app = Flask(__name__)

# route
books = [
    {
        "id": 1,
        "title": "python for beginners"
    },
    {
        "id": 2,
        "title": "Web API Mastery"
    },
    {
        "id": 3,
        "title": "Building Web API"
    },
]


@app.route('/')
def index():
    return "hello API Lovers"

# API ROUTE


@app.route("/api/v1/books", methods=["GET"])
def getbooks():
    return jsonify({"books": books})


if __name__ == '__main__':
    app.run(debug=True)
