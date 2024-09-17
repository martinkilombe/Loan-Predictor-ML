# Loan Prediction App

This Django-based web application uses machine learning to predict loan approval based on user-provided information.

## Features

- User-friendly web interface for inputting loan application details
- Machine learning model for predicting loan approval
- Dockerized for easy deployment and scaling

## Prerequisites

- Python 3.10+
- Docker and Docker Compose (for containerized deployment)
- Git

## Local Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/loan-prediction-app.git
   cd loan-prediction-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

6. Open your browser and navigate to `http://localhost:8000` to use the app.

## Docker Deployment

1. Make sure you have Docker and Docker Compose installed on your system.

2. Create a `.env` file in the project root with the necessary environment variables:
   ```
   DEBUG=0
   SECRET_KEY=your_secret_key_here
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=loanprediction
   SQL_USER=loanuser
   SQL_PASSWORD=loanpassword
   SQL_HOST=db
   SQL_PORT=5432
   DATABASE=postgres
   ```

3. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

4. The app should now be running. Access it by navigating to `http://localhost:8000` in your web browser.

## Usage

1. Fill out the loan application form with the required information.
2. Submit the form to get a prediction on whether the loan is likely to be approved or denied.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.