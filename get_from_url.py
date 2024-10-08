from bs4 import BeautifulSoup
import requests


def get_from_hitoriconquest(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    grid = soup.find('div', {'id': 'puzzleTable'}).text
    return grid
