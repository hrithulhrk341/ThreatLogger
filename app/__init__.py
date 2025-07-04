from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
import os

mail = Mail()

def create_app():
    # Load environment variables from .env
    load_dotenv()

    app = Flask(__name__)

    # App configuration
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "supersecretkey")
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

    # Initialize extensions
    mail.init_app(app)

    # Import and register routes
    from .routes import main
    app.register_blueprint(main)

    return app
