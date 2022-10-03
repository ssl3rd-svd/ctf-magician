import os
import shutil

import bs4
import pyjson5
import requests

class CTFdParserException(Exception):
    pass

class CTFdRequestException(CTFdParserException):
    pass

class CTFdNonceNotFound(CTFdParserException):
    pass

class CTFdNotLoggedIn(CTFdParserException):
    pass

class CTFdParser:
    
    def __init__(self, baseurl, useragent='ctf-magician'):
        
        self.loggedin = False
        self.baseurl = baseurl

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': useragent
        })

    def parse_nonce_from_html(html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        scripts = soup.select('head > script')
        for script in scripts:
            script = script.text.strip()
            if script.startswith('window.init = '):
                initobj = script[len('window.init = '):]
                initobj = pyjson5.loads(initobj)
                if 'csrfNonce' in initobj:
                    return initobj['csrfNonce']
        return ''

    def ctfd_get(self, url, *args, status_ok=200, **kwargs):
        try:
            response = self.session.get(self.baseurl + url, *args, **kwargs)
        except requests.RequestException as e:
            raise CTFdRequestException
        if response.status_code != status_ok and status_ok != None:
            raise CTFdRequestException
        return response

    def ctfd_api_get(self, *args, check_logged_in=True, check_api_success=True, **kwargs):

        if check_logged_in and not self.loggedin:
            raise CTFdNotLoggedIn

        response = self.ctfd_get(*args, **kwargs)
        data = response.json()
        if check_api_success and data['success'] != True:
            raise CTFdRequestException

        return data['data']

    def login(self, username, password):

        response = self.ctfd_get('/login')
        nonce = CTFdParser.parse_nonce_from_html(response.text)
        if not nonce:
            raise CTFdNonceNotFound

        try:
            response = self.session.post(
                self.baseurl + '/login',
                data = {
                    'name': username,
                    'password': password,
                    '_submit': 'Submit',
                    'nonce': nonce
                },
                allow_redirects=False
            )
        except requests.RequestException as e:
            raise CTFdRequestException

        if response.status_code != 302:
            return False
        else:
            self.loggedin = True
            return True

    def get_chall_list(self):
        return self.ctfd_api_get('/api/v1/challenges')

    def get_chall_desc(self, chall_id):
        chall = self.ctfd_api_get(f'/api/v1/challenges/{chall_id}')
        return chall['description']

    def get_chall_files_list(self, chall_id):
        chall = self.ctfd_api_get(f'/api/v1/challenges/{chall_id}')
        return chall['files']

    def download_chall_files(self, chall_id, download_dir):

        os.makedirs(download_dir, exist_ok=True)

        downloaded = []

        for chall_file in self.get_chall_files_list(chall_id):
            
            filename = chall_file
            idx = chall_file.find("?token=")
            if idx != -1:
                filename = chall_file[:idx]
            
            filename = os.path.basename(filename)
            filepath = os.path.join(download_dir, filename)

            response = self.ctfd_get(chall_file, status_ok=None, stream=True)
            if response.status_code != 200:
                raise CTFdRequestException

            with open(filepath, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
                del response

            downloaded.append(filepath)

        return downloaded
