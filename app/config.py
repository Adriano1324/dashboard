from mongoengine import connect
from fastapi_mail import FastMail
from jinja2 import Environment, FileSystemLoader
import os


backend_url = 'http://127.0.0.1:8000'

connection = connect('dashboard')
email=''
password=''

mail = FastMail(email, password)

jinja_env = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]

