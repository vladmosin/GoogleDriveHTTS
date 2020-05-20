import argparse
import requests
from secrets import token_urlsafe
import json


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', required=True)
    parser.add_argument('--secret', required=True)
    return parser.parse_args()


def step2(client_id):
    code_verifier = token_urlsafe(128)
    code_challenge = code_verifier

    url = 'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'client_id': client_id,
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/drive.readonly',
        'code_challenge': code_challenge,
        'code_challenge_method': 'plain',
        'state': 'step2'
    }

    r = requests.post(url, params=params)

    print('Go to:')
    print(r.url)

    print('Enter code:')
    code = input()

    return code_verifier, code


def step5(client_id, client_secret, code_verifier, code):
    url = 'https://oauth2.googleapis.com/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'code': code,
        'grant_type': 'authorization_code',
        'code_verifier': code_verifier
    }
    r = requests.post(url, params=params)
    print(r.status_code)

    print(r.text)
    data = json.loads(r.text)

    access_token = data['access_token']
    print(f'Access token = {access_token}')

    get_url = 'https://www.googleapis.com/drive/v2/files'
    get_params = {
        'access_token': access_token
    }
    get_r = requests.get(get_url, params=get_params)

    print('Status code')
    print(get_r.status_code)
    print('Content')
    print(get_r.content)
    print('Text')
    print(get_r.text)


if __name__ == '__main__':
    args = parse_arguments()

    client_id = args.id
    client_secret = args.secret

    code_verifier, code = step2(client_id)
    step5(client_id, client_secret, code_verifier, code)
