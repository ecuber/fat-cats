import requests
import json
import re

def authenticate(data):
    auth = requests.post('https://api.petfinder.com/v2/oauth2/token', data=data)
    return auth.json()

def get_zip():
    locale = input("Enter a ZIP Code: ")
    pattern = re.compile("^[0-9]{5}(?:-[0-9]{4})?$")
    while not re.match(pattern, locale):
        print("\nInvalid ZIP Code! Please try again.")
        locale = input("Enter a ZIP Code: ")
    return locale

data = {
  'grant_type': 'client_credentials',
  'client_id': 'qYj4EZ9pot9rRr545Dh8W7psT5Uu7MbmyXwyNRDX69RMtHZ4hD',
  'client_secret': 'jqllRqFJwhhi38VjbV5Mammh8J1mitHhvrn9NxXd'
}

credentials = authenticate(data)
print("Connected to API!")
locale = get_zip()
print(f"Searching for THICC cats within 25 mile radius of {locale}...")

headers = {
    "Authorization": f"Bearer {credentials['access_token']}"
}

params = (
    ("location", locale),
    ("type", "cats"),
    ("size", "large,xlarge"),
    ("distance", "25"),
    ("limit", "10"),
    ("sort", "random")
)

response = requests.get('https://api.petfinder.com/v2/animals', headers=headers, params=params)

# Reauthenticates if the access token expired
if response.status_code == 401:
    credentials = authenticate(data)
    responses = [requests.get('https://api.petfinder.com/v2/animals', headers=headers, params=params)]

cats = response.json()['animals']
print("\n")
for i, cat in enumerate(cats):
    print(f"{i + 1}: {cat['name']} {cat['url']}")