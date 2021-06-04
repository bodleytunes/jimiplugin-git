from dataclasses import dataclass
import os
from typing import Union


from git import Repo
import git

from plugins.git.includes.git_ops import GitOps
from plugins.git.includes.git_helpers import GitHelper as helper


@dataclass
class CloneArgs:

    repo: Repo = None
    git_url: str = None
    git_clone_local_path: str = None
    git_clone_subpath: str = None


class CloneGit:
    def __init__(self, git_repo: git.Repo, args: CloneArgs = None) -> None:
        self.args = args  # pass in args as CloneArgs object
        self.git_repo = git_repo

        pass

    def clone(self) -> Union[git.Repo, bool]:
        # get new repo object
        # g = git.Repo()
        # build full local path to clone to
        clone_path = self._build_clone_path(
            self.args.git_clone_local_path, self.args.git_clone_subpath
        )
        # pre flights and clone
        if helper._check_local_path(path=self.args.git_clone_local_path):
            try:
                # clone
                self.repo = self.git_repo.clone_from(
                    url=self.args.git_url, to_path=clone_path
                )
                return self.repo
            except Exception as e:
                print(f"can't clone repo: {e}")
                return False
        else:
            try:
                # create new path
                helper._create_local_path(self.args.git_clone_local_path)
                # clone
                self.repo = self.git_repo.clone_from(
                    url=self.args.git_url, to_path=clone_path
                )
                return self.repo
            except Exception as e:
                print(f"can't clone repo: {e}")
                # todo: now have an option to git pull instead?
                return False

    def _build_clone_path(
        self, git_clone_local_path: str, git_clone_subpath: str
    ) -> str:

        return os.path.join(git_clone_local_path, git_clone_subpath)
