import os
import sys
import subprocess as sp

from functools import wraps
from typing import (
    Any,
    List,
)
from enum import (
    Enum,
    auto,
)

from pequod.logging import log


class ErrorCode(Enum):
    PRECONDITION_FAILED = auto()
    CALLED_PROCESS_ERROR = auto()


def run_as_root() -> bool:
    return os.geteuid() == 0


def panic(reason: str, code: ErrorCode) -> None:
    log.critical(reason)
    exit(code)


def ensure_not_running_as_root(fn) -> Any:

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if run_as_root():
            panic(
                reason=
                "This script must be run as non-root user inside docker group",
                code=ErrorCode.PRECONDITION_FAILED)

        return fn(*args, **kwargs)

    return wrapper


def user_id() -> int:
    return os.geteuid()


def group_id() -> int:
    return os.getegid()


def user() -> str:
    return os.environ["USER"]


def run(cmd: List[str], panic_on_error: bool = True) -> None:
    shell_cmd = " ".join(cmd)
    log.debug(f"Running `{shell_cmd}`")

    completed = sp.run(cmd, stdout=sys.stdout, stderr=sys.stderr)

    if completed.returncode != 0:
        msg = f"Called process `{shell_cmd}` exited with code {completed.returncode}"
        if panic_on_error:
            panic(reason=msg, code=ErrorCode.CALLED_PROCESS_ERROR)

        log.warning(msg)
