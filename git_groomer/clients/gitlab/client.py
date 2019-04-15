import os
from typing import List, Optional

import requests
import maya

from git_groomer.clients.base import BaseGitClient
from git_groomer.models import Commit, Branch


class GitlabClient(BaseGitClient):
    __client_name__ = 'GitLab'

    def __init__(self, project_id: int, api_token: Optional[str] = None):
        self.__api_token = api_token or os.getenv("GITLAB_API_TOKEN")
        self.project_id = project_id
        self._base_api_url = f'https://gitlab.com/api/v4/projects/{self.project_id}'

    def _make_headers(self) -> dict:
        return {'PRIVATE-TOKEN': self.__api_token}

    def get_branches(self) -> List[Branch]:
        response = requests.get(f'{self._base_api_url}/repository/branches',
                                headers=self._make_headers())
        result = []
        if response.status_code == 200:
            for branch in response.json():
                last_branch_commit = branch['commit']
                last_branch_commit = Commit(short_id=last_branch_commit['short_id'], long_id=last_branch_commit['id'],
                                            author=last_branch_commit['author_email'],
                                            title=last_branch_commit['title'], message=last_branch_commit['message'],
                                            created_on=maya.parse(last_branch_commit['authored_date']).datetime(),
                                            parent_ids=last_branch_commit['parent_ids'])
                branch = Branch(name=branch['name'], merged=branch['merged'], last_commit=last_branch_commit)
                result.append(branch)
            return result
        else:
            raise Exception()

    def _delete_branch(self, branch_name: str) -> bool:
        response = requests.delete(f'{self._base_api_url}/repository/branches/{branch_name}',
                                   headers=self._make_headers())
        return response.status_code == 204
