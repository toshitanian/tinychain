import requests
import random

ports = [5000, 5001]

while True:
    p = random.choice(ports)
    r = requests.get(f'http://localhost:{p}/mine')
    print('mine', r.json())

    p = random.choice(ports)
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        'from': 'aaa',
        'to': 'bbb',
        'amount': random.randint(0, 1000)
    }
    r = requests.post(f'http://localhost:{p}/txion', headers=headers, json=body)
    print('txion', r.json())
