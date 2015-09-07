from fabric import api
from fabric.contrib import files


class Accessor(object):
    '''
    a static class wrapper for fabric functions
    and environment variables
    '''
    api.env['use_ssh_config'] = True

    @staticmethod
    def host(name):
        api.env['host_string'] = name
        return Accessor

    @staticmethod
    def password(password):
        api.env['password'] = password
        return Accessor

    @staticmethod
    def run(*args, **kwargs):
        return api.run(*args, **kwargs)

    @staticmethod
    def sudo(*args, **kwargs):
        return api.sudo(*args, **kwargs)

    @staticmethod
    def append(*args, **kwargs):
        return files.append(*args, **kwargs)
