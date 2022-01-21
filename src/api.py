import base64
from time import time
from urllib.parse import urlencode
import requests

from src import config
from src.database.credentials import Credentials


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
    service_name = 'spotify'

    def __init__(self) -> None:
        # from app import config

        self.base_uri = 'https://accounts.spotify.com/api/token'
        self.token_url = config.config()['auth_url']

        self.client_id = config.config()['client_id']
        self.client_secret = config.config()['client_secret']

        self.credentials = Credentials()

    """
    Authenticate the python session.
    To authenticate as a user use authorize redirect
    """

    def authenticate(self):
        if self.has_valid_session():
            return True

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

        self.login(auth_response_data['access_token'])
        print(auth_response_data)
        # save the access token
        # access_token = auth_response_data['access_token']

    """
    Builds the redirect string that spotify uses to authenticate the user
    client_id       Required    The Client ID generated after registering your application.
    response_type	Required    Set to code.
    redirect_uri	Required    The URI to redirect to after the user grants or denies permission. This URI needs to have
                                been entered in the Redirect URI allowlist that you specified when you registered your
                                application (See the app settings guide). The value of redirect_uri here must exactly
                                match one of the values you entered when you registered your application, including
                                upper or lowercase, terminating slashes, and such.
    state	        Optional    This provides protection against attacks such as cross-site request forgery. See RFC-6749.
    scope	        Optional    A space-separated list of scopes.If no scopes are specified, authorization will be
                                granted only to access publicly available information: that is, only information
                                normally visible in the Spotify desktop, web, and mobile players.
    show_dialog	    Optional    Whether or not to force the user to approve the app again if they've already done so.
                                If false (default), a user who has already approved the application may be
                                automatically redirected to the URI specified by redirect_uri. If true, the user will
                                not be automatically redirected and will have to approve the app again.
    """

    def authorize(self) -> str:
        query = urlencode({
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': config.config()['redirect'],
            # 'state': 'something-unique',
            # 'scope': 'user.read',
            # 'show_dialog': 'false',
        })

        return f'https://accounts.spotify.com/authorize?{query}'
    """
    grant_type	    Required    This field must contain the value "authorization_code".
    code	        Required    The authorization code returned from the previous request.
    redirect_uri	Required    This parameter is used for validation only (there is no actual redirection). The value of this parameter must exactly match the value of redirect_uri supplied when requesting the authorization code.
    """

    def login(self, code: str):

        base64credentials = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode('utf-8')
        ).decode('utf-8')

        headers = {
            'Authorization': f'Basic {base64credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(
            url=self.token_url,
            headers=headers,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': config.config()['redirect'],
            }
        )

        self.set_authorization(response['access_token'])
        self.credentials.insert(
            f'{self.service_name}_refresh', response['refresh_token'], 36000)
        self.credentials.insert(self.service_name, response['access_token'])

        return True

    def refresh(self):
        refresh = self.credentials.get(f'{self.service_name}_refresh')

        if refresh:
            return self.login(refresh)

        return False

    def set_authorization(self, code: str, expiry: int = 3600) -> None:
        self._auth_code = code
        self._auth_expiry = int(time()) + expiry

    def get_authorization(self) -> str:
        if self._auth_code and self._auth_expiry > time():
            return self._auth_code

        return False

    def has_valid_session(self) -> bool:
        return bool(self.get_authorization())


def main():
    # print(config.config())

    spotify = Spotify()
    spotify.authenticate()


if __name__ == '__main__':
    main()
