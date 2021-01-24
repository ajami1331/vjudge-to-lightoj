from requests import session
from zipfile import ZipFile
import http.cookiejar
import shutil
import pickle
import time
import os

path = os.path.dirname(__file__)

class Vjudge:
    judgeSlug = "Vjudge"
    rootUrl = "https://vjudge.net/"
    loginUrl = "/user/login/"
    allSubmissionsUrl = "/user/exportSource?minRunId=0&maxRunId=99999999&ac=false"
    acSubmissionsUrl = "/user/exportSource?minRunId=0&maxRunId=99999999&ac=true"
    username = str()
    password = str()
    zipUrl = str()
    s = session()
    loggedIn = False

    def clearSolutions(self):
        solutionsDir = path + os.sep + "solutions"
        try:
            shutil.rmtree(solutionsDir)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
            pass
        time.sleep(2)
        os.mkdir(solutionsDir)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.login()

    def login(self):
        payLoad = {
            'username': self.username,
            'password': self.password
        }

        self.s = session()
        login_url = f"{self.rootUrl}{self.loginUrl}"
        r = self.s.post(login_url, data=payLoad)
        if(r.text == "success"):
            self.loggedIn = True
        else:
            print(r.text)

    def downloadSubmissions(self):
        if not self.loggedIn:
            print("Sorry, can't download data. You are not logged into Vjudge.")
            return None
        if not os.path.exists('zip-files'):
            os.mkdir('zip-files')
        self.zipUrl = path + os.sep + "zip-files" + os.sep + self.username + '.zip'
        if os.path.exists(self.zipUrl):
            os.remove(self.zipUrl)

        self.clearSolutions()
        source_dowload_url = f"{self.rootUrl}{self.acSubmissionsUrl}"
        self.downloadUrl(source_dowload_url, self.s, self.zipUrl)
        self.extractZip()
        print("Solutions downloaded and extracted.")
    
    def downloadUrl(self, url, sess, save_path, chunk_size=128):
        r = sess.get(url, stream=True)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)

    def extractZip(self, sourcePath = ""):
        sourcePath = self.zipUrl if not sourcePath else sourcePath
        destinationPath = path + os.sep + "solutions"
        with ZipFile(sourcePath, 'r') as zipFile:
            zipFile.extractall(destinationPath)