import requests

API_URL = "http://127.0.0.1:5000"


def get_data(operation, initial_date, end_date, platform):
  url = API_URL + "/getData"

  params = {'operation': operation, 'initial_date': initial_date, 'end_date': end_date, 'platform': platform}
  response = requests.get(url, params)
  response.raise_for_status()

  response = response.json()
  return response["response"]

def get_utm():
  url = API_URL + "/get_utm"
  response = requests.get(url)
  response.raise_for_status()

  response = response.json()
  return response["response"]

def get_offset():
  url = API_URL + "/get_offset"
  response = requests.get(url)
  response.raise_for_status()

  response = response.json()
  return response["response"]
