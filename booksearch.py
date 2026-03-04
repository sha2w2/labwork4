from flask import Flask, request, jsonify, send_from_directory
import urllib.request
import urllib.parse
import json
import os

app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/script.js")
def serve_js():
    return send_from_directory(".", "script.js")


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "No query provided"}), 400

    encoded_query = urllib.parse.quote(query)
    url = f"https://www.googleapis.com/books/v1/volumes?q={encoded_query}&maxResults=20"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    books = []
    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        books.append({
            "title": info.get("title", "Unknown Title"),
            "authors": info.get("authors", ["Unknown Author"]),
            "infoLink": info.get("infoLink", "#"),
        })

    return jsonify({"books": books})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Book Finder running at http://localhost:{port}")
    app.run(debug=True, port=port)
