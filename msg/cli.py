import click

from config import Kicker
from exceptions import MSGException


@click.group()
def main():
    '''
    the tasty server tool
    '''
    pass


@main.command()
@click.argument('config', type=click.Path(exists=True))
def prod(config):
    '''
    execute a config on a production host
    '''
    go(config, 'prod')


@main.command()
@click.argument('config', type=click.Path(exists=True))
def stage(config):
    '''
    execute a config on a staging host
    '''
    go(config, 'stage')


def go(path, host):
    try:
        Kicker(path=path).validate(host).go()
    except MSGException as e:
        e.report()
        exit(1)
