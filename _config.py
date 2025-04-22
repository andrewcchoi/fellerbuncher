import os

from dotenv import load_dotenv
load_dotenv()

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT").split(",")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_TO = os.environ.get("EMAIL_TO", "")
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PWD = os.environ.get("EMAIL_PWD")
