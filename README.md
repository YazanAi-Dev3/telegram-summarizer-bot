# Telegram Conversation Summarizer Bot

A professionally engineered, dual-engine Telegram bot service designed to summarize conversations within groups. This project has evolved from a simple script into a fully automated, testable, and deployable service with a persistent database and a complete CI/CD pipeline.

The primary use case is to help users who have been away from a busy group to quickly catch up on the discussions they missed by providing accurate summaries of conversation segments.

---

## Core Features

* **Dual Summarization Engines**: Easily switch between a high-quality, Transformer-based abstractive summarizer and a lightweight, traditional extractive summarizer via a simple configuration change.
* **Persistent Database Archiving**: Automatically archives all messages from a group into a persistent PostgreSQL database, ensuring data is never lost.
* **Conversation Range Summarization**: Users can specify the exact portion of a conversation to summarize by replying to a starting message, or summarize the most recent messages.
* **Hybrid Summarization Logic**: Intelligently handles very long conversations by splitting them into chunks, summarizing each part, and then summarizing the results for a comprehensive final output.
* **Automated Testing Suite**: Includes a full suite of unit and integration tests using `pytest` to ensure code quality and reliability.
* **Continuous Integration & Delivery (CI/CD)**: Features a complete GitHub Actions pipeline that automatically runs tests, builds a new Docker image, and triggers deployment on every push to the main branch.
* **Rich Command Set**: Includes user-friendly commands like `/help` for guidance and `/stats` for displaying chat analytics queried directly from the database.
* **Dockerized for Portability**: Comes with a `Dockerfile` for easy, consistent deployment on any cloud platform that supports containers.

---

## Tech Stack

* **Backend**: Python, FastAPI
* **Telegram Integration**: `python-telegram-bot`
* **Database**: PostgreSQL
* **ORM**: SQLModel
* **AI Engine (Pro)**: `transformers` (Hugging Face)
* **AI Engine (Lightweight)**: `sumy` & `nltk`
* **Testing**: `pytest`, `pytest-asyncio`, `httpx`
* **CI/CD**: GitHub Actions, Docker
* **Deployment**: Render

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
    Use `requirements.txt` for the full version (including Transformers) or `requirements-free.txt` for the lightweight version.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Copy the example file to a new `.env` file and fill in your details.
    ```bash
    copy .env.example .env
    ```
    Edit the `.env` file with your Telegram Bot Token and your external PostgreSQL database URL.

5.  **Run the application:**
    ```bash
    python main.py
    ```
    The server will start on `http://localhost:8000`.

---

## How to Use

1.  Add the bot to your Telegram group and grant it administrator permissions.
2.  Use the following commands:
    * `/start`: Displays the welcome message.
    * `/help`: Shows a detailed list of all commands.
    * `/summarize`: **Reply** to the first message of a conversation to summarize everything from that point to your command.
    * `/summarize_last [N]`: Summarizes the last N messages (e.g., `/summarize_last 20`). Defaults to 50.
    * `/stats`: Displays statistics about the archived messages in the chat.