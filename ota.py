import git

import config

TRACK_BRANCH = config.git_branch

class OTA():
    class NotGitRepo(Exception):
        pass

    class NoSuchBranchError(Exception):
        pass

    class NoSuchCommitError(Exception):
        pass

    class CheckoutError(Exception):
        pass

    def __init__(self):
        try:
            self.repo = git.Repo(search_parent_directories=False)
            self.error = None
        except git.InvalidGitRepositoryError:
            self.error = "Does not appear to be in a git repo"

    def current_version(self):
        if self.error:
            return "Unknown"

        sha = self.repo.head.object.hexsha
        dirty = self.repo.is_dirty()
        return sha + ' (dirty)' if dirty else ''

    # Returns True if updated, False if nothing to update to,
    # Throws exceptions if problems with git
    def run(self, force=False):
        if self.error:
            raise self.NotGitRepo()

        if self.repo.is_dirty() and not force:
            return False # Probably should get some feedback

        try:
            self.repo.remotes.origin.fetch('origin', TRACK_BRANCH)
        except IndexError as e:
            raise self.NoSuchBranchError(TRACK_BRANCH) from e

        remote_head = self.repo.remotes.origin.refs.master
        remote_head_id = self.repo.remotes.origin.refs.master.object.hex_sha
        current_commit_id = self.repo.head.object.hexsha

        if remote_head_id == current_commit_id:
            return False

        try:
            remote_head.checkout(force=force)
            return True
        except git.GitCommandError as e:
            raise self.CheckoutError(e)
