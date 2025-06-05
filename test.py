import requests
from bs4 import BeautifulSoup
url = 'https://sentir.projection-learn.website/wp-json/responses/v1/endpoint'
data ={
    'name':'Slash',
    'text':'some text',
    'nda':True,
    'file':'name.txt',
    'email':'name@gmail.com'
}
with requests.Session() as session:
    response = session.post(url,data )
    soup = BeautifulSoup(response.text,'lxml')
    print(soup)

