import requests
url = 'http://localhost:8000/api/tifinar/store-comment/'
data = {
    'page_title': 'test',
    'author_name': 'test',
    'author_email': 'test@test.com',
    'cmt_subject': 'test'
}
response = requests.post(url, data=data)
print(response.status_code, response.text)