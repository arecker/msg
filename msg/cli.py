import click


@click.group()
def main():
    '''
    the low budget deployment tool
    '''
    pass


@main.command()
def prod():
    '''
    execute a config on a production host
    '''
    pass


@main.command()
def stage():
    '''
    execute a config on a staging host
    '''
    pass
