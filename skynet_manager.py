import siaskynet as skynet


class SkyManager:

    def __init__(self):
        self.client = skynet.SkynetClient()

    def submit_file(self, file):
        return self.client.upload_file(path=file)

    def submit_folder(self, folder):
        return self.client.upload_directory(path=folder)
