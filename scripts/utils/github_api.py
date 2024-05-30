import httpx

_BASE_URL = 'https://api.github.com'


def get_releases_latest_tag_name(repository_name: str) -> str:
    url = f'{_BASE_URL}/repos/{repository_name}/releases/latest'
    response = httpx.get(url, follow_redirects=True)
    assert response.is_success, url
    return response.json()['tag_name']
