from flask import Flask, render_template, request, redirect, url_for, session
import requests
import openai
import base64
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# --- Formatter: bold words between backticks ---
def format_explanation_with_dynamic_headers(text):
    # Bold `code` terms
    text = re.sub(r'`([^`]+)`', r'<b>\1</b>', text)

    # Match lines like: FunctionName: (case-insensitive, line-start)
    text = re.sub(r'^([A-Za-z_][A-Za-z0-9_]*):\s*$', r'<h5 class="mt-3">\1</h5>', text, flags=re.MULTILINE)

    # Format bullet points nicely (turn "- " into • with line breaks)
    text = re.sub(r'^\s*-\s+', r'<br>• ', text, flags=re.MULTILINE)

    return text


# --- GitHub Search ---
def search_github_code(query):
    url = "https://api.github.com/search/code"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}"
    }
    params = {
        "q": f"{query} in:file language:python",
        "per_page": 1
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json().get("items", [])

# --- Get file content from GitHub API ---
def fetch_code_content(api_url):
    response = requests.get(api_url)
    content = response.json().get("content", "")
    try:
        return base64.b64decode(content).decode("utf-8")
    except Exception:
        return "Could not decode content."

# --- Generate GPT explanation ---
def generate_doc(code_snippet):
    system_msg = {
        "role": "system",
        "content": (
            "You are a helpful Python assistant that explains code to beginners. "
            "Your goal is to make the code understandable with bullet points."
        )
    }
    user_msg = {
        "role": "user",
        "content": (
            "Explain the following Python code by grouping explanations under each function name as a header.\n"
            "Use this format:\n"
            "FunctionName:\n"
            "- explanation 1\n"
            "- explanation 2\n"
            "Wrap each function/variable name in backticks.\n\n"
            f"{code_snippet}"
        )
    }

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[system_msg, user_msg],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    explanation = None
    query = None

    if request.method == "POST":
        query = request.form["query"]
        results = search_github_code(query)
        if results:
            code = fetch_code_content(results[0]["url"])
            explanation = generate_doc(code[:1000])
            explanation = format_explanation_with_dynamic_headers(explanation)
            result = code

        # Store results in session to persist across redirect
        session["result"] = result
        session["explanation"] = explanation
        session["query"] = query

        # Redirect to the GET route
        return redirect(url_for("index"))

    # On GET, retrieve from session and then clear
    result = session.pop("result", None)
    explanation = session.pop("explanation", None)
    query = session.pop("query", "")

    return render_template("index.html", result=result, explanation=explanation, query=query)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
