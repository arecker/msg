from unittest import TestCase

from msg.server import Accessor
from msg import servos
from msg.exceptions import ServoMissingFieldsException
from mocks import MockFabricTestCase


class TestBaseServo(TestCase):
    def test_init_accessor_passes(self):
        obj = servos.BaseServo()
        self.assertEqual(obj.run, Accessor.run)
        self.assertEqual(obj.sudo, Accessor.sudo)

    def test_init_data_dict(self):
        obj = servos.BaseServo()
        self.assertEqual(obj.config, {})
        expected = {
            'one': 1,
            'two': True,
            'three': 'hello'
        }
        obj = servos.BaseServo(expected)
        self.assertEqual(obj.config, expected)

    def test_defaults_loaded_in_config(self):
        class MockServo(servos.BaseServo):
            defaults = {
                'one': 1,
                'two': 2,
                'three': 3
            }

        mock = {
            'one': 'ONE',
            'three': 3,
            'extra': 'wooh!'
        }

        expected = {
            'one': 'ONE',
            'two': 2,
            'three': 3,
            'extra': 'wooh!'
        }

        obj = MockServo(mock)
        self.assertEqual(obj.config, expected)

    def test_not_implemented(self):
        class MockServo(servos.BaseServo):
            pass

        for method in ['go', 'nuke']:
            with self.assertRaises(NotImplementedError):
                getattr(MockServo(), method)()

    def test_validate_no_required(self):
        class MockServo(servos.BaseServo):
            pass

        try:
            MockServo().validate()
        except:
            self.fail('failed to validate with no required fields')

    def test_validate_pass(self):
        class MockServo(servos.BaseServo):
            required = ['something']

        try:
            MockServo({'something': 'hello'}).validate()
        except:
            self.fail('failed to validate with good config')

    def test_validate_fail(self):
        class MockServo(servos.BaseServo):
            required = ['something', 'here']
        mock = {'something': 'hello'}
        obj = MockServo(mock)
        with self.assertRaises(ServoMissingFieldsException):
            obj.validate()

        try:
            obj.validate()
        except ServoMissingFieldsException as e:
            self.assertEqual(e.fields, ['here', ])


class TestHandShake(MockFabricTestCase):
    def test_default_go(self):
        servos.HandShake().go()
        self.assertEqual(self.mock.last, {
            'command': 'echo "Hellooooooo nurse"',
            'sudo': False
        })

    def test_go(self):
        servos.HandShake({'hello': 'test message'}).go()
        self.assertEqual(self.mock.last, {
            'command': 'echo "test message"',
            'sudo': False
        })

    def test_default_nuke(self):
        servos.HandShake().nuke()
        self.assertEqual(self.mock.last, {
            'command': 'echo "You ever see a podrace?"',
            'sudo': False
        })

    def test_nuke(self):
        servos.HandShake({'goodbye': 'test message'}).nuke()
        self.assertEqual(self.mock.last, {
            'command': 'echo "test message"',
            'sudo': False
        })


class TestInstaller(MockFabricTestCase):
    def test_validate(self):
        obj = servos.Installer({})
        try:
            obj.validate()
            self.fail('installer did not enforce requirements')
        except ServoMissingFieldsException as e:
            self.assertEqual(e.fields, ['packages'])

    def test_validate_short(self):
        obj = servos.Installer('mysql')
        obj.validate()

    def test_defaults(self):
        servos.Installer({
            'packages': ['python', 'nmap', 'mysql']
        }).validate().go()
        self.assertEqual(self.mock.last, {
            'command': 'apt-get install -y python nmap mysql',
            'sudo': True
        })

    def test_short(self):
        servos.Installer('python').validate().go()
        self.assertEqual(self.mock.last, {
            'command': 'apt-get install -y python',
            'sudo': True
        })

    def test_command_override(self):
        servos.Installer({
            'command': 'pacman -S',
            'packages': ['python', 'nmap', 'mysql']
        }).validate().go()
        self.assertEqual(self.mock.last, {
            'command': 'pacman -S python nmap mysql',
            'sudo': True
        })


class TestHost(MockFabricTestCase):
    def test_validate_short(self):
        try:
            servos.Host('alexrecker.com').validate()
        except:
            self.fail('valid host failed validation')

    def test_validate_short_fail(self):
        try:
            servos.Host('').validate()
        except ServoMissingFieldsException as e:
            self.assertEqual(e.fields, ['host'])

    def test_run_short(self):
        servos.Host('alexrecker.com').validate().go()
        self.assertEqual(self.mock.last, {
            'file': '/etc/hosts',
            'append': '127.0.0.1     alexrecker.com',
            'sudo': True
        })


class TestPut(MockFabricTestCase):
    def test_validate_pass(self):
        try:
            servos.Put({
                'source': 'blah blah blah',
                'destination': 'blah blah blah'
            }).validate()
        except:
            self.fail('valid put config failed')

    def test_validate_fail(self):
        try:
            servos.Put({}).validate()
        except ServoMissingFieldsException as e:
            self.assertEqual(e.fields, ['source', 'destination'])


class TestClone(MockFabricTestCase):
    def test_validate_pass(self):
        try:
            servos.Clone({
                'url': 'google.com',
                'target': 'lskdjflksdflkdj'
            }).validate()
        except:
            self.fail('valid clone config failed')

    def test_validate_fail(self):
        try:
            servos.Clone({
                'url': 'google.com'
            }).validate()
            self.fail('invalid clone config passed')
        except ServoMissingFieldsException as e:
            self.assertEqual(e.fields, ['target'])

    def test_go(self):
        servos.Clone({
            'url': 'http://google.com/.git',
            'target': '~/google'
        }).validate().go()
        self.assertEqual(self.mock.last, {
            'command': 'git clone http://google.com/.git ~/google',
            'sudo': False
        })


class TestUntar(MockFabricTestCase):
    def test_go(self):
        servos.Untar({
            'source': '/tmp/test.tar.gz',
            'destination': '/tmp/test'
        }).validate().go()
        self.assertEqual(self.mock.last, {
            'command': 'tar xvf /tmp/test.tar.gz -C /tmp/test',
            'sudo': False
        })


class TestUnzip(MockFabricTestCase):
    def test_go(self):
        servos.Unzip({
            'source': '/tmp/test.zip',
            'destination': '/tmp/test'
        }).validate().go()
        self.assertEqual(self.mock.last, {
            'command': 'unzip /tmp/test.zip -d /tmp/test',
            'sudo': False
        })


class TestRemove(MockFabricTestCase):
    def test_go(self):
        servos.Remove({
            'target': '/tmp/test'
        }).validate().go()
        self.assertEqual(self.mock.last, {
            'command': 'rm /tmp/test',
            'sudo': False
        })


class TestSymlink(MockFabricTestCase):
    def test_go_1(self):
        servos.Symlink({
            'source': '/tmp/file',
            'destination': '/var/file_link'
        }).validate().go()
        self.assertEqual(self.mock.last, {
            'command': 'ln -s /tmp/file /var/file_link',
            'sudo': False
        })

    def test_go_2(self):
        servos.Symlink({
            'source': '/tmp/file',
            'destination': '/var/file_link',
            'soft': False,
            'sudo': True
        }).validate().go()
        self.assertEqual(self.mock.last, {
            'command': 'ln /tmp/file /var/file_link',
            'sudo': True
        })


class TestPayload(MockFabricTestCase):
    def test_go_zip(self):
        servos.Payload({
            'payload': '/local/test.zip',
            'destination': '/var/web/test'
        }).validate().go()
        self.assertEqual(self.mock.history, [{
            'put': '/local/test.zip',
            'destination': '/tmp',
            'sudo': False
        }, {
            'command': 'unzip /tmp/test.zip -d /var/web/test',
            'sudo': False
        }, {
            'command': 'rm /tmp/test.zip',
            'sudo': False
        }])

    def test_go_tar1(self):
        servos.Payload({
            'payload': '/local/test.tar',
            'destination': '/var/web/test',
            'temp': '/temp'
        }).validate().go()
        self.assertEqual(self.mock.history, [{
            'put': '/local/test.tar',
            'destination': '/temp',
            'sudo': False
        }, {
            'command': 'tar xvf /temp/test.tar -C /var/web/test',
            'sudo': False
        }, {
            'command': 'rm /temp/test.tar',
            'sudo': False
        }])

    def test_go_tar2(self):
        servos.Payload({
            'payload': '/local/test.tar.gz',
            'destination': '/var/web/test',
        }).validate().go()
        self.assertEqual(self.mock.history, [{
            'put': '/local/test.tar.gz',
            'destination': '/tmp',
            'sudo': False
        }, {
            'command': 'tar xvf /tmp/test.tar.gz -C /var/web/test',
            'sudo': False
        }, {
            'command': 'rm /tmp/test.tar.gz',
            'sudo': False
        }])

    def test_validate(self):
        try:
            servos.Payload({
                'payload': '/something',
                'destination': 'bleh'
            }).validate().go()
            self.fail('Invalid config passed')
        except ServoMissingFieldsException as e:
            self.assertEqual(e.fields, ['payload'])
