from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
import os

from git import Repo, RemoteReference
import git

from plugins.git.includes.git_helpers import GitHelper as helper


class BaseGitOps(ABC):
    @abstractmethod
    def fetch():
        pass

    @abstractmethod
    def init():
        pass

    @abstractmethod
    def files_add():
        pass

    @abstractmethod
    def create_index():
        pass

    @abstractmethod
    def remote_add():
        pass

    @abstractmethod
    def set_remote_reference():
        pass

    @abstractmethod
    def commit():
        pass

    @abstractmethod
    def push():
        pass

    @abstractmethod
    def pull():
        pass


@dataclass
class GitArgs:

    origin: Repo = None
    index: Repo = None
    git_url: str = str(None)
    git_proto: str = str(None)  # http, https or ssh (git@xyz)
    git_port: str = "443"
    git_path: str = "/tmp/git/backups"
    git_server: str = "gitea.example-org.co.uk"
    git_project: str = "example-proj"
    git_repo_name: str = "testrepo"
    git_branch: str = "master"
    git_remote: str = "origin"
    git_commit_message: str = "This is a jimi commit."
    git_server_type: str = (
        "gitea"  # http, https or gitea (gitea is http but runs on explicit port 3000)
    )


class GitOps(BaseGitOps):

    GIT_PROTO_GITEA: str = "http"
    GIT_PROTO_HTTPS: str = "https"

    def __init__(self, args: GitArgs = None) -> None:
        super().__init__()

        self.args = args

    pass

    def init(self) -> None:
        try:
            # init local
            try:
                git.Repo.init(self.args.git_path)
            except Exception as e:
                print(f"can't init new repo: {e}")
                pass
            # get repo object
            self.repo = Repo(self.args.git_path)
        except Exception as e:
            print(f"unable to init exception: {e}")

    def remote_add(self) -> None:
        # git remote add
        try:
            # if no remote then create one
            if len(self.repo.remotes) < 1:
                self.repo.create_remote(self.args.git_remote, self.git_url)
            elif len(self.repo.remotes) > 0:
                # check incoming arg remote matches current remote
                # if match do nothing, if no match delete all
                # delete existing remote
                if self.args.git_remote == self.repo.remotes[0].name:
                    for r in self.repo.remotes:
                        r.remove(repo=self.repo, name=r.name)
                # now create new one
                self.repo.create_remote(self.args.git_remote, self.git_url)
        except Exception as e:
            print(f"Error {e}")
            pass

    def create_index(self) -> None:
        self.index = self.repo.index

    def files_add(self) -> None:
        # add all files
        self.index.add("*")
        pass

    def commit(self) -> None:
        self.index.commit(self.args.git_commit_message)
        pass

    def fetch(self) -> None:
        # fetch --all
        # todo
        pass

    def set_remote_reference(self) -> None:
        # Setup remote tracking
        remote_ref = RemoteReference(
            self.repo,
            f"refs/remotes/{self.args.git_remote}/{self.args.git_branch}",
        )
        # set tracking branch
        self.repo.head.reference.set_tracking_branch(remote_ref)

    def push(self) -> None:

        try:
            # prepare push
            o = self.repo.remote(name=self.args.git_remote)
            # push to remote
            o.repo.remotes[0].push(force=True)

        except Exception as e:
            print(Exception(f"Cannot push to repo due to error: {e}"))
            pass

    def pull(self) -> None:
        try:
            o = self.repo.remote(name=self.args.git_remote)
            # pull from remote
            o.pull(self.args.git_remote, self.args.git_branch)
        except Exception as e:
            print(Exception(f"Cannot pull from repo due to error: {e}"))
            pass

    def _check_repo_exists(self, path: str) -> bool:
        # does repo exist
        return self.repo.repo.exists(path)

    def _get_url_https(self) -> str:
        proto = self.GIT_PROTO_HTTPS
        server = self.args.git_server
        port = self.args.git_port
        project = self.args.git_project
        repo = self.args.git_repo_name

        return str(f"{proto}://{server}:{port}/{project}/{repo}.git")

    def _get_url_gitea(self) -> str:
        proto = self.GIT_PROTO_GITEA
        server = self.args.git_server
        port = "3000"
        project = self.args.git_project
        repo = self.args.git_repo_name

        return str(f"{proto}://{server}:{port}/{project}/{repo}.git")

    def _get_url_ssh(self) -> str:
        prefix = "git"
        server = self.args.git_server
        project = self.args.git_project
        repo = self.args.git_repo_name

        return str(f"{prefix}@{server}:{project}/{repo}.git")

    def generate_url(self) -> None:
        # generate url
        if self.args.git_server_type == "https":
            self.args.git_proto = "https"
            self.git_url = self._get_url_https()
        elif self.args.git_server_type == "gitea":
            self.args.git_proto = "https"
            self.git_url = self._get_url_gitea()
        elif self.args.git_server_type == "ssh":
            self.args.git_proto = "ssh"
            self.git_url = self._get_url_ssh()

    def setup_fs_paths(self, git_path: Optional[str] = None) -> None:
        if git_path is not None:
            self.args.git_path = git_path
        # does path exist?  if not then create it
        if not helper._check_local_path(path=self.args.git_path):
            # create path
            helper._create_local_path(path=self.args.git_path)
        return
