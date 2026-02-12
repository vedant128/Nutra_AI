# Nutra_AI: Your Personal Health & Wellness Companion

Nutra_AI is an intelligent virtual health assistant designed to revolutionize how you manage your physical and mental well-being. By integrating personalized advice on diet, exercise, sleep, and stress management, Nutra_AI helps you achieve your health goals through a user-friendly conversational interface.

![Nutra_AI Banner](outputs/image1.png)

## 🌟 Key Features

-   **Personalized Health Advice**: Tailored recommendations based on your unique profile, dietary preferences, and health goals.
-   **AI-Powered Chatbot**: Interact with our advanced AI (powered by Google Gemini) to get instant answers to your health queries.
-   **Daily Routine Tracking**: Monitor your sleep, exercise, water intake, and study habits to stay on top of your daily routine.
-   **Dashboard Management**: Easily update your health stats and preferences through a dedicated user dashboard.
-   **Secure Authentication**: robust user signup and login system to keep your data private.

## 🛠️ Technology Stack

-   **Backend Framework**: Flask (Python)
-   **Database**: SQLite (with SQLAlchemy ORM)
-   **AI Model**: Google Gemini 2.5 Flash
-   **Frontend**: HTML, CSS, JavaScript (Bootstrap 4)
-   **Deployment**: Ready for Heroku/Render (Gunicorn support)

## 🚀 Getting Started

Follow these instructions to set up the project locally on your machine.

### Prerequisites

-   Python 3.8 or higher
-   Pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Nutra_AI.git
    cd Nutra_AI
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    -   Create a `.env` file in the root directory.
    -   Copy the contents from `.env.example` and fill in your API keys:
        ```bash
        GOOGLE_API_KEY=your_google_ai_api_key
        FLASK_SECRET_KEY=your_secure_secret_key
        ```

### Running the Application

1.  **Start the Flask server:**
    ```bash
    python main.py
    ```

2.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000`.

## 📦 Deployment

This project is configured for easy deployment on platforms like **Heroku** or **Render**.

### Heroku / Render Setup

1.  **Procfile:** The repository includes a `Procfile` required for these platforms:
    ```
    web: gunicorn main:app
    ```

2.  **Environment Variables:**
    Ensure you add the following Environment Variables in your deployment dashboard (Settings > Config Vars):
    -   `GOOGLE_API_KEY`: Your Google Gemini API Key.
    -   `FLASK_SECRET_KEY`: A random secret string for session security.

## 📊 Project Statistics

-   **62%** of people prefer virtual healthcare solutions (Accenture).
-   **57%** of people want remote monitoring for chronic conditions (Accenture).

---
*Empowering your health journey with AI.*
