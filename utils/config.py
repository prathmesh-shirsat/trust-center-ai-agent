import json
import os
from dotenv import load_dotenv

load_dotenv()

def load_tasks(filename="config/tasks.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)  # Returns a list of task JSON objects
