import argparse
import requests
from secrets import token_urlsafe


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
        'redirect_uri': 'http://localhost',
        'response_type': 'code',
        'scope': None,
        'code_challenge': code_challenge,
        'code_challenge_method': 'plain',
        'state': 'step2'
    }

    r = requests.post(url, data=params)

    print(r.status_code)
    print(r.content)
    print(r.text)


def step5(client_id, client_secret):
    url = 'https://oauth2.googleapis.com/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://localhost'
    }


if __name__ == '__main__':
    args = parse_arguments()

    client_id = args.id
    client_secret = args.secret

    step2(client_id)
