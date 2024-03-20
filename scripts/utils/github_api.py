import requests

_BASE_URL = 'https://api.github.com'


def get_releases_latest_tag_name(repository_name: str) -> str:
    url = f'{_BASE_URL}/repos/{repository_name}/releases/latest'
    response = requests.get(url)
    assert response.ok, url
    return response.json()['tag_name']
