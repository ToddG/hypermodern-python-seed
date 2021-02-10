"""{{cookiecutter.project_name}} console."""

import click
import typing
import multiprocessing
from loguru import logger
from {{cookiecutter.project_name}}.custom_logger import init_click_logger
import platform,socket,re,uuid

from . import __version__

logger = logger.bind(version=__version__)

LOG_LEVEL="log_level"


def get_system_info() -> typing.Dict[str,str]:
    """Compiled from internet.

    See: https://stackoverflow.com/questions/3103178/\
            how-to-get-the-system-info-with-python#3103224

    Returns:
        dict[str,str]: Dictionary of system statistics.
    """
    info={}
    try:
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['cpus']=str(multiprocessing.cpu_count())
    except Exception as e:
        logger.error("failed to get system info", exception=str(e))
    return info


@click.command()
@click.option(
    "-ll",
    "--log-level",
    type=click.Choice(["debug", "info", "warning", "error"], case_sensitive=False),
    default="error",
)
@click.version_option(version=__version__)
@click.pass_context
def main(ctx: dict, log_level: str) -> None:
    """The {{cookiecutter.project_name}} console entry point."""
    ctx.ensure_object(dict)  # type: ignore
    log_level = log_level.upper()
    ctx.obj[LOG_LEVEL] = log_level  # type: ignore
    init_click_logger(log_level)
    click.echo("console for {{cookiecutter.project_name}} started...")
    logger.debug("system information", **get_system_info()) 


