import base64
import github
import asyncio
import gitconfig
import time


class GitHub:
    def __init__(self, username=None, token=None):
        if token is None:
            token = gitconfig.SongSearch.token
        if username is None:
            username = gitconfig.SongSearch.user
        self.token, self.username = token, username
        self.repo, self.client = None, None

    async def login(self):
        self.client = await github.GHClient(username=self.username, token=self.token)
        return self.client

    async def set_repo(self, repo, owner=None):
        if owner is None:
            owner = self.username
        self.repo = await self.client.get_repo(owner=owner, repo=repo)
        return self.repo

    async def commit(self, file, rename=None, msg="No message"):
        """:param file the path to the file to upload
        :param rename what to rename the file
        :param msg commit message"""
        if rename is None:
            rename = file
        with open(file, "r") as f:
            cont = f.read()
        return await self.repo.add_file(filename=rename, message=msg, content=cont)


async def main():
    g = GitHub()
    await g.login()
    await g.set_repo("songsearch.github.io")
    print(await g.commit("gitpush.py"))


asyncio.run(main())
