import os

from typing import List

from pequod.helpers import (
    ensure_not_running_as_root,
    group_id,
    log,
    run,
    user_id,
)
from pequod.config import (
    REPO_NAME,
    CONTAINER_NAME,
    HOST_WORKSPACE_DIR,
    HOST_DOCKER_COMPOSE_PATH,
    CONTAINER_WORKSPACE_DIR,
    CONTAINER_BASHRC_PATH,
)


class Client:

    def __init__(self) -> None:
        self._setup_env()

    def _setup_env(self) -> None:
        os.environ["REPO_NAME"] = str(REPO_NAME)
        os.environ["CONTAINER_NAME"] = str(CONTAINER_NAME)
        os.environ["HOST_WORKSPACE_DIR"] = str(HOST_WORKSPACE_DIR)
        os.environ["CONTAINER_WORKSPACE_DIR"] = str(CONTAINER_WORKSPACE_DIR)
        os.environ["COMPOSE_PROJECT_NAME"] = str(REPO_NAME)

    # --------------------------------------------------------------------------

    @ensure_not_running_as_root
    def login(self) -> None:
        self._bash(user=f"{user_id()}:{group_id()}")

    @ensure_not_running_as_root
    def create(self) -> None:
        log.info(f"Mounting '{HOST_WORKSPACE_DIR}' -> '{CONTAINER_WORKSPACE_DIR}'")
        self._compose_build()
        self._add_group()
        self._add_user()
        self._change_owner()

    def remove(self) -> None:
        self._stop()
        self._rm()

    @ensure_not_running_as_root
    def restart(self) -> None:
        self._compose_restart()

    @ensure_not_running_as_root
    def root(self) -> None:
        self._bash(user="root")

    # --------------------------------------------------------------------------

    def _bash(self, user: str) -> None:
        cmd = [
            "--user", f"{user}", "--env", "REPO_NAME", f"{CONTAINER_NAME}",
            "/bin/bash", "--rcfile", f"{CONTAINER_BASHRC_PATH}"
        ]
        self._exec(cmd)

    # --------------------------------------------------------------------------

    def _compose_build(self) -> None:
        cmd = [
            "docker-compose", "-f", f"{HOST_DOCKER_COMPOSE_PATH}", "up", "-d",
            "--build", "--force-recreate"
        ]
        run(cmd)

    def _add_group(self) -> None:
        cmd = [f"{CONTAINER_NAME}", "groupadd", "-g", f"{group_id()}", "grp"]
        self._exec(cmd, panic_on_error=False)

    def _add_user(self) -> None:
        user = os.environ["USER"]
        cmd = [
            f"{CONTAINER_NAME}", "useradd", "-u", f"{user_id()}", "-g",
            f"{group_id()}", "-m", f"{user}"
        ]
        self._exec(cmd)

    def _change_owner(self) -> None:
        user = os.environ["USER"]
        cmd = [
            f"{CONTAINER_NAME}", "chown", "-R", f"{user}",
            f"{CONTAINER_WORKSPACE_DIR}"
        ]
        self._exec(cmd)

    # --------------------------------------------------------------------------

    def _stop(self) -> None:
        cmd = ["docker", "container", "stop", f"{CONTAINER_NAME}"]
        run(cmd)

    def _rm(self) -> None:
        cmd = ["docker", "container", "rm", f"{CONTAINER_NAME}"]
        run(cmd)

    # --------------------------------------------------------------------------

    def _compose_restart(self) -> None:
        cmd = [
            "docker-compose", "-f", f"{HOST_DOCKER_COMPOSE_PATH}", "up", "-d"
        ]
        run(cmd)

    # --------------------------------------------------------------------------

    def _exec(self, cmd: List[str], interactive: bool = True, **kwargs) -> None:
        cmd = ["docker", "exec"] + (["-it"] if interactive else []) + cmd
        run(cmd, **kwargs)

    def _compose_config(self) -> None:
        cmd = ["docker-compose", "config"]
        run(cmd)
