
import os
import re

result = re.match(r'\w+', os.getenv('USER'))

config = {
    'client_id': '19f8a2736e8547c08d3a2a7276699a29',
    'client_secret': '2c770bd5ca7747118c505145603448b0',
    'app_name': 'vulture',
    'auth_url': 'https://accounts.spotify.com/api/token',
    'user': result.group() if result else 'demo'
}


def main() -> dict:
    for key, value in config.items():
        print(f"{key}: {value}")


if __name__ == '__main__':
    main()
