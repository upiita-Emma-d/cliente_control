import requests
def envio_post(el_json):
    URL = 'http://34.136.99.177:8080/api/?format=json'
    headers = {'Content-Type':'application/json',}
    r = requests.post(URL,headers=headers, data = el_json)
    return r.text  