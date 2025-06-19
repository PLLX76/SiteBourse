# Simplified Stock Market Website

This project is a simple website that displays stock market information using Flask for the backend and HTML for the frontend. It does not use a database and relies on web scraping to fetch real-time stock data.

## Features

- Display of current stock prices.
- Web scraping to retrieve data.

## Supported Websites

- JustETF
- Boursier.com
- Boursorama

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML
- **Web Scraping:** Cloudscraper (Python)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/PLLX76/SiteBourse.git
   cd SiteBourse
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment:**

   - On Windows:

     ```bash
     .\env\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source env/bin/activate
     ```

4. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   _(A `requirements.txt` file will be created containing the necessary dependencies such as `Flask` and scraping libraries)_

## Usage

1. **Run the Flask application:**

   ```bash
   python main.py
   ```

2. **Access the website:**
   Open your browser and go to `http://127.0.0.1:5000/` (or the address and port provided by Flask).
