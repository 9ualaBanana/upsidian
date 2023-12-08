import platform
import os
from subprocess import run
from requests import Request
import requests
from pathlib import Path, PurePath
from bs4 import BeautifulSoup

class Installer:

    def __init__(self, location: PurePath = None):
        if (platform.system() == 'Windows'):
            self._platform = 'win'
        else:
            raise EnvironmentError(platform.system())
        self._session = requests.session()
        self._session.verify = False
        self._download_page_request = self._session.prepare_request(
            Request('GET', 'https://obsidian.md/download', params={'os': self._platform, 'arch': platform.architecture()[0].rstrip("bit")}))
        self._location = location if location != None else os.path.join(Path.home(), 'Downloads')

    def download(self):
        try:
            download_hub = self._session.send(self._download_page_request)
            download_hub.raise_for_status()

            download_url = BeautifulSoup(download_hub.content).find('a', {'aria-label': 'Download Obsidian'}).get('href')
            if download_url == None:
                raise Exception("Download hub page didn't contain the necessary URL for download.", download_hub.content)
            installer = requests.get(download_url)
            installer.raise_for_status()

            self._path = Path(os.path.join(self._location, installer.headers['Content-Disposition'].split('filename=')[1]))
            Path.write_bytes(self._path, installer.content)
            return self
        except Exception as ex:
            raise Exception('Download failed.') from ex
        
    def run(self):
        run('', executable=self._path)