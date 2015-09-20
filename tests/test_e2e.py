from msg import exceptions
from mocks import MockFabricTestCase


class TestHandShakeInstallerConfig(MockFabricTestCase):
    config_data = '''
host:
  prod: 'prod-host'
  stage: 'stage-host'

servos:
  - handshake
  - install:
      packages:
        - python
        - python-pip
'''
    expected = [{
        'command': 'echo "Hellooooooo nurse"',
        'sudo': False
    }, {
        'command': 'apt-get install -y python python-pip',
        'sudo': True
    }]

    def test(self):
        self.prod()
        self.compare()


class TestHandShakeInstallerConfigOverrides(MockFabricTestCase):
    config_data = '''
host:
  prod: 'test-server'
  stage: 'stage-server'

servos:
  - handshake:
      hello: 'I am overriding the default message'
  - install:
      command: pacman -S
      packages:
        - python
        - python-pip
        - mysql
'''
    expected = [{
        'command': 'echo "I am overriding the default message"',
        'sudo': False
    }, {
        'command': 'pacman -S python python-pip mysql',
        'sudo': True
    }]

    def test(self):
        self.prod()
        self.compare()


class TestInstallerMissingReqs(MockFabricTestCase):
    config_data = '''
host:
  prod: 'prod-host'
  stage: 'stage-host'

servos:
  - handshake
  - install
'''

    def test_it(self):
        try:
            self.prod()
        except exceptions.MSGException as e:
            self.assertEqual(len(e.errors), 1)
            self.assertEqual(e.errors[0].fields, ['packages'])


class TestHost(MockFabricTestCase):
    config_data = '''
host:
  prod: 'prod-host'
  stage: 'stage-host'

servos:
  - host: alexrecker.com
'''
    expected = [{
        'file': '/etc/hosts',
        'append': '127.0.0.1     alexrecker.com',
        'sudo': True
    }]

    def test(self):
        self.prod()
        self.compare()


class TestPut(MockFabricTestCase):
    config_data = '''
host:
  prod: prod-host
  stage: stage-host

servos:
  - put:
      source: '/local/file'
      destination: '/remote/location'
'''

    expected = [{
        'put': '/local/file',
        'destination': '/remote/location',
        'sudo': False
    }]

    def test(self):
        self.prod()
        self.compare()


class TestInstallAndClone(MockFabricTestCase):
    config_data = '''
host:
  prod: 'test-host'
  stage: 'test-host'

servos:
  - install: git
  - clone:
      url: https://github.com/arecker/msg.git
      target: ~/git/msg
'''

    expected = [{
        'command': 'apt-get install -y git',
        'sudo': True
    }, {
        'command': ' '.join([
            'git', 'clone',
            'https://github.com/arecker/msg.git',
            '~/git/msg'
        ]),
        'sudo': False
    }]

    def test(self):
        self.prod()
        self.compare()


class TestSite(MockFabricTestCase):
    config_data = '''
host:
  prod: 'test-lorelai'

servos:
  - install: nginx
  - site:
      server: nginx
      hostname: itsworking.local
      payload: /home/alex/Desktop/its.working.tar.gz
      root: /var/www/itsworking
'''

    expected = [{
        'command': 'apt-get install -y nginx',
        'sudo': True
    }, {
        'put': '/home/alex/Desktop/its.working.tar.gz',
        'destination': '/tmp',
        'sudo': False
    }, {
        'command': 'tar xvf /tmp/its.working.tar.gz -C /var/www/itsworking',
        'sudo': False
    }, {
        'command': 'rm /tmp/its.working.tar.gz',
        'sudo': False
    }, {
        'template': 'nginx.txt',
        'destination': '/etc/nginx/sites-available/itsworking.local',
        'data': {
            'port': 80,
            'hostname': 'itsworking.local',
            'root': '/var/www/itsworking',
            'index_files': [
                'index.html',
                'index.htm'
            ],
        }, 'sudo': True
    }, {
        'command': 'ln -s /etc/nginx/sites-available/itsworking.local ' +
        '/etc/nginx/sites-enabled/itsworking.local',
        'sudo': True
    }, {
        'file': '/etc/hosts',
        'append': '127.0.0.1     itsworking.local',
        'sudo': True
    }, {
        'command': 'systemctl reload nginx',
        'sudo': True
    }]

    def test(self):
        self.prod()
        self.compare()
