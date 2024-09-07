"""
Requests Library Cheat Sheet
=============================
This script demonstrates the basic usage of the Requests library in Python, 
which is used to make HTTP requests to interact with web services.
"""

import requests  # Importing the Requests library

# -------------------------
# Sending HTTP GET Requests
# -------------------------

# Simple GET request
response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
print(response.status_code)  # Prints the status code of the response (e.g., 200 for OK)
print(response.text)  # Prints the content of the response as a string

# Handling JSON response
data = response.json()  # Parses the response content as JSON
print(data)  # Prints the parsed JSON data as a Python dictionary

# -------------------------
# Sending HTTP POST Requests
# -------------------------

# Data to be sent in the POST request
payload = {'title': 'foo', 'body': 'bar', 'userId': 1}

# Sending POST request
post_response = requests.post('https://jsonplaceholder.typicode.com/posts', json=payload)
print(post_response.status_code)  # Prints the status code of the response
print(post_response.json())  # Prints the response content parsed as JSON

# -------------------------
# Handling Request Headers
# -------------------------

# Custom headers for a request
headers = {'User-Agent': 'my-app/0.0.1'}

# Sending GET request with headers
header_response = requests.get('https://httpbin.org/headers', headers=headers)
print(header_response.json())  # Prints the response content parsed as JSON

# -------------------------
# Handling Query Parameters
# -------------------------

# Query parameters to be sent in the GET request
params = {'q': 'requests', 'page': 2}

# Sending GET request with query parameters
params_response = requests.get('https://jsonplaceholder.typicode.com/comments', params=params)
print(params_response.url)  # Prints the full URL with parameters
print(params_response.json())  # Prints the response content parsed as JSON
