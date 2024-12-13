import os
from openai import OpenAI
from Constants import *
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI()
