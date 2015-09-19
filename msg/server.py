from fabric import api, operations
from fabric.contrib import files

import os

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

    @staticmethod
    def put(*args, **kwargs):
        return operations.put(*args, **kwargs)

    @staticmethod
    def template(template, dest, data, sudo=False):
        return files.upload_template(
            template, dest, context=data, use_jinja=True,
            template_dir=os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)
                ), 'templates'),
            use_sudo=True
        )
