# 🔍 GitDecode

GitDecode is a lightweight SaaS tool that fetches Python code from GitHub using the GitHub Search API and explains it using OpenAI's GPT-3.5. It’s designed to help developers and learners understand unfamiliar code with structured natural language explanations.

---

## 🚀 Features

- 🔎 GitHub code search integration
- 🧠 GPT-3.5 explanations with prompt engineering
- 💡 Readable output with dynamic formatting
- 🌙 Dark mode toggle
- 📋 Copy-to-clipboard support
- 🐳 Dockerized for easy deployment

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/sivadboon/gitdecode.git
cd gitdecode
```

### 2. Create and configure your .env file
#### Create a .env file in the root directory and add the following:

```bash
OPENAI_API_KEY=your_openai_api_key
GITHUB_TOKEN=your_github_token
SECRET_KEY=your_flask_secret_key
```

#### ⚠️ Your OpenAI key must be from a valid account using GPT-3.5 API. Your GitHub token should have public_repo read access.

### 3. Run using Docker

#### Build the Container:

```bash
docker build -t gitdecode .
```

#### Run the container:

```bash
docker run --env-file .env -p 5000:5000 gitdecode
```

## 🛠 Project Structure

```bash
├── app/
│   ├── app.py                 # Main Flask app
│   ├── templates/index.html   # UI template
│   └── static/style.css       # Custom styling
├── Dockerfile
├── requirements.txt
├── .env                       # API keys (not committed)
└── README.md
```
