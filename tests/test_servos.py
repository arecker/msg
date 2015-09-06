from unittest import TestCase

from msg.server import Accessor
from msg.servos import BaseServo, HandShake, Installer
from msg import server
from msg.server import api
from msg.exceptions import ServoMissingFieldsException
from mocks import MockFabric


class TestBaseServo(TestCase):
    '''
    exercises base servo class
    '''
    def test_init_accessor_passes(self):
        '''
        should pass through to accessor api
        '''
        obj = BaseServo()
        self.assertEqual(obj.run, Accessor.run)
        self.assertEqual(obj.sudo, Accessor.sudo)

    def test_init_data_dict(self):
        '''
        should save off data, or default to an empty
        dict if none given
        '''
        obj = BaseServo()
        self.assertEqual(obj.config, {})
        expected = {
            'one': 1,
            'two': True,
            'three': 'hello'
        }
        obj = BaseServo(expected)
        self.assertEqual(obj.config, expected)

    def test_defaults_loaded_in_config(self):
        '''
        should load the config object with
        specified defaults
        '''
        class MockServo(BaseServo):
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
        '''
        custom servo without defined
        routines should raise a NI expection
        '''
        class MockServo(BaseServo):
            pass

        for method in ['go', 'nuke']:
            with self.assertRaises(NotImplementedError):
                getattr(MockServo(), method)()

    def test_validate_no_required(self):
        '''
        servo should validate config just fine
        if no required fields defined
        '''
        class MockServo(BaseServo):
            pass

        try:
            MockServo().validate()
        except:
            self.fail('failed to validate with no required fields')

    def test_validate_pass(self):
        '''
        servo should validate when required fields are fulfilled
        '''
        class MockServo(BaseServo):
            required = ['something']

        try:
            MockServo({'something': 'hello'}).validate()
        except:
            self.fail('failed to validate with good config')

    def test_validate_fail(self):
        '''
        servo should raise when config is missing required
        fields.  should store missing items in the exception
        '''
        class MockServo(BaseServo):
            required = ['something', 'here']
        mock = {'something': 'hello'}
        obj = MockServo(mock)
        with self.assertRaises(ServoMissingFieldsException):
            obj.validate()

        try:
            obj.validate()
        except ServoMissingFieldsException as e:
            self.assertEqual(e.fields, ['here', ])


class ServoTestCase(TestCase):
    def setUp(self):
        server.api = self.mock = MockFabric()

    def tearDown(self):
        server.api = api


class TestHandShake(ServoTestCase):
    '''
    exercise the Handshake servo
    '''
    def test_default_go(self):
        '''
        should execute a message with the
        default value if none given
        '''
        HandShake().go()
        self.assertEqual(
            self.mock.last_command,
            'echo "Hellooooooo nurse"'
        )

    def test_go(self):
        '''
        should execute with a custom message
        '''
        HandShake({'hello': 'test message'}).go()
        self.assertEqual(
            self.mock.last_command,
            'echo "test message"'
        )

    def test_default_nuke(self):
        HandShake().nuke()
        self.assertEqual(
            self.mock.last_command,
            'echo "You ever see a podrace?"'
        )

    def test_nuke(self):
        HandShake({'goodbye': 'test message'}).nuke()
        self.assertEqual(
            self.mock.last_command,
            'echo "test message"'
        )


class TestInstaller(ServoTestCase):
    '''
    excercise installer servo
    '''
    def test_validate(self):
        obj = Installer({})
        try:
            obj.validate()
            self.fail('installer did not enforce requirements')
        except ServoMissingFieldsException as e:
            self.assertEqual(e.fields, ['packages'])

    def test_defaults(self):
        Installer({
            'packages': [
                'python',
                'nmap',
                'mysql'
            ]
        }).validate().go()
        self.assertEqual(
            self.mock.last_command,
            'sudo apt-get install -y python nmap mysql'
        )

    def test_command_override(self):
        Installer({
            'command': 'sudo pacman -S',
            'packages': [
                'python',
                'nmap',
                'mysql'
            ]
        }).validate().go()
        self.assertEqual(
            self.mock.last_command,
            'sudo pacman -S python nmap mysql'
        )
