import gitlab
import configparser
import asyncio


class Gitlab:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./etc/config.ini')
        self.gl = gitlab.Gitlab(config['gitlab']['url'], config['gitlab']['token'])
        self.gitProject = None

    async def listProject(self):
        def fun():
            data = []
            projects = self.gl.projects.list(iterator=True)
            for i in projects:
                git = self.gl.projects.get(i.path_with_namespace).ssh_url_to_repo
                data.append({'projectName': i.path_with_namespace, 'git': git})
            return data
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, fun)

    async def listTag(self, gitProject):
        self.gitProject = gitProject

        def fun():
            data = []
            lists = self.gl.projects.get(self.gitProject).tags.list(iterator=True)
            git = self.gl.projects.get(self.gitProject).ssh_url_to_repo
            for l in lists:
                data.append({'name': l.name, 'message': l.message, 'git': git})
            return data

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, fun)

    async def listBranch(self, gitProject):
        self.gitProject = gitProject

        def fun():
            data = []
            lists = self.gl.projects.get(self.gitProject).branches.list(iterator=True)
            git = self.gl.projects.get(self.gitProject).ssh_url_to_repo
            for l in lists:
                data.append({'name': l.name, 'message': l.commit['message'], 'git': git})
            return data

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, fun)
