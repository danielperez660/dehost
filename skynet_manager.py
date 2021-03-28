import siaskynet as skynet
import os


class SkyManager:

    def __init__(self):
        self.client = skynet.SkynetClient()

    def submit_file(self, file):
        name = file.filename
        url = self.client.upload_file(path="temp/" + name).replace("sia://", "")
        os.remove("temp/" + name)
        return url

    def submit_folder(self, folder):
        return self.client.upload_directory(path=folder)

    def fetch_file(self, url):
        files = self.client.download_file(path=url)
        return files
