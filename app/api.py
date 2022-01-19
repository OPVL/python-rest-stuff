import base64
import requests
import config


class Api:
    def __init__(self, **kwargs) -> None:
        self.base_uri = kwargs['base_uri']

    def get(self, uri: str, params: dict = {}, options: dict = {}):
        return requests.get(url=self.buildUrl(uri), params=params)

    def post(self, uri: str, params: dict = {}, options: dict = {}):
        return requests.post(url=self.buildUrl(uri), params=params)

    def buildUrl(self, uri) -> str:
        return self.base_uri + uri


class Spotify(Api):
    def __init__(self) -> None:
        self.base_uri = 'https://accounts.spotify.com/api/token'
        self.token_url = config.config()['auth_url']

        self.client_id = config.config()['client_id']
        self.client_secret = config.config()['client_secret']

    def authenticate(self):
        base64credentials = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode('utf-8')
        ).decode('utf-8')

        headers = {
            'Authorization': f'Basic {base64credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        auth_response = requests.post(
            url=self.token_url,
            headers=headers,
            data={'grant_type': 'client_credentials'}
        )

        auth_response_data = auth_response.json()

        print(auth_response_data)
        # save the access token
        # access_token = auth_response_data['access_token']


def main():
    print(config.config())

    spotify = Spotify()
    spotify.authenticate()


if __name__ == '__main__':
    main()
