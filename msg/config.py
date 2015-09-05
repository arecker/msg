import yaml


def parse(path=None, data=None):
    '''
    parses a yaml formatted config
    either from a file path or
    passed data
    '''
    if data:
        return yaml.load(data)
    if path:
        with open(path) as file:
            return yaml.load(file)
    return {}
