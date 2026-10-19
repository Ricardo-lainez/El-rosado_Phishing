import socket
import unittest

from laboratorio.server import open_listener


class ServerBindingTests(unittest.TestCase):
    @unittest.skipUnless(hasattr(socket, "SO_EXCLUSIVEADDRUSE"), "Exclusividad de Windows")
    def test_local_instance_prevents_overlapping_lan_instance(self):
        with open_listener("127.0.0.1", 0) as first:
            port = first.getsockname()[1]
            with self.assertRaises(OSError):
                with open_listener("0.0.0.0", port):
                    pass

    @unittest.skipUnless(hasattr(socket, "SO_EXCLUSIVEADDRUSE"), "Exclusividad de Windows")
    def test_lan_instance_prevents_overlapping_local_instance(self):
        with open_listener("0.0.0.0", 0) as first:
            port = first.getsockname()[1]
            with self.assertRaises(OSError):
                with open_listener("127.0.0.1", port):
                    pass
