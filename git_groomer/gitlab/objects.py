from git_groomer.gitlab.client import GitlabClient
from git_groomer.base.objects import Repository


class GitlabRepository(Repository):

    def __init__(self, repository_name: str, repository_id: int):
        super().__init__(repository_name, GitlabClient(repository_id))
