from git_groomer.clients.gitlab.client import GitlabClient
from git_groomer.models import Repository


class GitlabRepository(Repository):

    def __init__(self, repository_name: str, repository_id: int):
        super().__init__(repository_name, GitlabClient(repository_id))
