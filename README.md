# 🔗 URL Shortener API

A simple REST API built with Python and FastAPI. It turns long links into short ones and helps users manage their links.

## ✨ Features

- 👤 Create an account and log in
- 🔐 Keep accounts safe with hashed passwords and JWT tokens
- 🔗 Create short links
- 🌍 Open a short link to visit the original website
- 📋 See your own links
- 🗑️ Delete your own links
- 📊 See how many times a link was opened

## 🛠️ Built With

- **Python** – programming language
- **FastAPI** – API framework
- **Pydantic** – data validation
- **SQLite + SQLAlchemy** – database
- **PyJWT + bcrypt** – login and password security
- **Swagger UI** – API testing
- **Docker** – containerization

## 🚀 Run the Project

1. Clone the repository:

   `git clone https://github.com/BaznatMihai/URL-Shortener-API.git`

2. Open the project folder:

   `cd URL-Shortener-API`

3. Install the packages:

   `python -m pip install -r requirements.txt`

4. Copy `.env.example` to a new file called `.env`. Replace `REPLACE_WITH_YOUR_OWN_SECRET_KEY` with your own secret key.

5. Start the API:

   `python -m uvicorn app.main:app --reload`

6. Open **http://127.0.0.1:8000/docs** to try the API.

The SQLite database is created automatically when the app starts.

## 🐳 Run with Docker
Make sure Docker is installed and running.
### 1. Build the image
```bash
docker build -t url-shortener-api .
```
### 2. Run the container
Create a `.env` file using `.env.example` and set your own secret key.
```bash
docker run --name url-shortener-container --env-file .env -e PYTHONPATH=/app -v url-shortener-data:/data -w /data -p 8000:8000 url-shortener-api
```
### 3. Open Swagger UI
http://127.0.0.1:8000/docs
### 4. Stop and restart the container
Stop:
```bash
docker stop url-shortener-container
```
Restart:
```bash
docker start -ai url-shortener-container
```
The SQLite database is stored in a Docker volume, so your data is saved even after the container stops.

## 📌 API Routes

| Method | Route | What it does |
|---|---|---|
| `POST` | `/register` | Create an account |
| `POST` | `/login` | Log in and get a JWT token |
| `GET` | `/me` | See your account details |
| `POST` | `/shorten` | Create a short link |
| `GET` | `/my-urls` | See your links |
| `GET` | `/{short_code}` | Open the original link |
| `GET` | `/shorten/{short_code}/stats` | See link statistics |
| `DELETE` | `/urls/{url_id}` | Delete your link |

🔒 Some routes need a JWT token. You can log in and use **Authorize** in Swagger UI.

## 📝 Notes
- The base URL can be changed in the `.env` file.
- Secret keys and database files are excluded from Git.
- The API was manually tested using Swagger UI.
- The application runs locally and with Docker.
- This project was built to practice backend development.
