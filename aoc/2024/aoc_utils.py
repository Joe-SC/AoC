import os
from dotenv import load_dotenv
load_dotenv()
import requests

SESSION_COOKIE = os.getenv("SESSION_COOKIE")

def fetch_input_data(year, day):
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, cookies={"session": SESSION_COOKIE})
    response.raise_for_status()
    return response.text
