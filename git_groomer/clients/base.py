from typing import List, Union

from git_groomer.models import Branch


class BaseGitClient:
    __client_name__ = 'BASE'

    def get_branches(self) -> List[Branch]:
        pass

    def delete_branches(self, branches: List[Union[Branch, str]]) -> List[bool]:
        return [self.delete_single_branch(branch) for branch in branches]

    def delete_single_branch(self, branch: Union[Branch, str]) -> bool:
        branch_name = branch.name if isinstance(branch, Branch) else branch
        return self._delete_branch(branch_name)

    def _delete_branch(self, branch_name: str) -> bool:
        pass
