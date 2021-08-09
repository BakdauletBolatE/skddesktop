import requests

url = 'http://10.245.12.67:9012/bip-sync/?wsdl'
headers = {'content-type': 'application/soap+xml; charset=utf-8'}


try:
    response = requests.get(url,headers=headers)
    print(response.status_code)

except requests.exceptions.ConnectionError:
    print("пР")
