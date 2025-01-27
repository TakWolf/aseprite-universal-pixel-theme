from pathlib import Path

import httpx
from tqdm import tqdm


def download_file(url: str, file_path: Path):
    with httpx.stream('GET', url, follow_redirects=True) as response:
        assert response.is_success, url
        tmp_file_path = file_path.with_suffix(f'{file_path.suffix}.download')
        with tmp_file_path.open('wb') as file:
            if 'Content-Length' in response.headers:
                with tqdm(total=int(response.headers['Content-Length'])) as progress:
                    for chunk in response.iter_bytes():
                        file.write(chunk)
                        progress.update(len(chunk))
            else:
                for chunk in response.iter_bytes():
                    file.write(chunk)
        tmp_file_path.rename(file_path)
