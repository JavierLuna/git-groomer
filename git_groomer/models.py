import re
from datetime import datetime
from typing import List

import maya

from git_groomer.clients.base import BaseGitClient


class Commit:
    def __init__(self, short_id: str, long_id: str, author: str, title: str, message: str, created_on: datetime,
                 parent_ids: List[str]):
        self.short_id = short_id
        self.long_id = long_id
        self.author = author
        self.message = message
        self.created_on = created_on
        self.parent_ids = parent_ids
        self.title = title


class Branch:
    def __init__(self, name: str, merged: bool, last_commit: Commit):
        self.name = name
        self.merged = merged
        self.last_commit = last_commit

    def __repr__(self):
        return f"<Branch {self.name} >"

    def __str__(self):
        return self.name


class Repository:
    def __init__(self, name: str, gitclient: BaseGitClient):
        self.name = name
        self.gitclient = gitclient
        self._branches = None

    @staticmethod
    def _filter_branches(branches: List[Branch], author: str = None, older_than: int = None, newer_than: int = None,
                         name: str = None, merged: bool = None) -> List[Branch]:
        filters = []

        if author is not None:
            filters.append(lambda b: b.last_commit.author == author)

        if merged is not None:
            filters.append(lambda b: b.merged == merged)

        if older_than is not None:
            date_cutoff = maya.now() - maya.timedelta(days=older_than)
            date_cutoff = date_cutoff.datetime()
            filters.append(lambda b: b.last_commit.created_on < date_cutoff)

        if newer_than is not None:
            date_cutoff = maya.now() - maya.timedelta(days=older_than)
            date_cutoff = date_cutoff.datetime()
            filters.append(lambda b: b.last_commit.created_on >= date_cutoff)

        if name is not None:
            regex = re.compile(name)
            filters.append(lambda b: regex.match(b.name))

        return [branch for branch in branches if all(f(branch) for f in filters)]

    def filter_branches(self, author: str = None, older_than: int = None, newer_than: int = None, name: str = None,
                        merged: bool = None):
        return self._filter_branches(self.branches, author=author, older_than=older_than, newer_than=newer_than,
                                     name=name, merged=merged)

    @property
    def branches(self):
        if self._branches is None:
            self._branches = self.gitclient.get_branches()
        return self._branches

    @branches.setter
    def branches(self, branches: List[Branch]):
        self._branches = branches

    def update_branches(self):
        self._branches = self.gitclient.get_branches()
