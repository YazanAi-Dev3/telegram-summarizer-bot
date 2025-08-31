# Telegram Conversation Summarizer Bot

A sophisticated, dual-engine Telegram bot designed to summarize conversations within groups. This bot is built with a modular and scalable architecture, featuring a database for message archiving and a configurable summarization engine.

The primary use case is to help users who have been away from a busy group to quickly catch up on the discussions they missed.

---

## Features

* **Dual Summarization Engines**: Switch between a high-quality, Transformer-based abstractive summarizer and a lightweight, traditional extractive summarizer via a simple configuration change.
* **Database Archiving**: Automatically archives all messages from a group into a local SQLite database for later retrieval.
* **Conversation Range Summarization**: Users can specify the exact portion of a conversation to summarize by replying to a starting message.
* **Hybrid Summarization Logic**: Intelligently handles very long conversations by splitting them into chunks, summarizing each part, and then summarizing the results for a comprehensive final output.
* **Dockerized**: Comes with a `Dockerfile` for easy, consistent deployment on any cloud platform.
* **Professional Architecture**: Built with a clean, modular design (Separation of Concerns) for high maintainability and scalability.

---

## Tech Stack

* **Backend**: Python, FastAPI
* **Telegram API**: `python-telegram-bot`
* **Database**: SQLite with SQLModel (ORM)
* **AI Engine (Pro)**: `transformers` (Hugging Face)
* **AI Engine (Lightweight)**: `sumy` & `nltk`
* **Deployment**: Docker

---

## Local Setup and Installation

Follow these steps to run the project on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    The project includes two requirements files. For the full version (including Transformers), use `requirements.txt`. For the lightweight, free-to-deploy version, use `requirements-free.txt`.
    ```bash
    pip install -r requirements-free.txt
    ```

4.  **Set up environment variables:**
    Copy the example file to a new `.env` file and fill in your details.
    ```bash
    copy .env.example .env
    ```
    Now, edit the `.env` file with your Telegram Bot Token.

5.  **Run the application:**
    ```bash
    python main.py
    ```
    The server will start on `http://localhost:8000`. Use a tool like `ngrok` to expose it for testing with Telegram.

---

## How to Use

1.  Add the bot to your Telegram group and grant it administrator permissions (specifically, the permission to read messages).
2.  To get a summary, find the first message you want to include in the conversation.
3.  Reply to that message with the command `/summarize`.
4.  The bot will fetch all messages from the starting point to your command from its archive and provide a summary.

---

## Deployment

This application is ready for deployment using Docker. The included `Dockerfile` is optimized for a lightweight build when using the traditional summarization engine. It can be deployed on any platform that supports Docker containers, such as Render or Heroku. Remember to set the environment variables in your deployment service's dashboard.