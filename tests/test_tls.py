import ssl
import unittest

import certifi
from botocore.httpsession import get_cert_path


class TrustStoreTests(unittest.TestCase):
    def test_botocore_uses_certifi(self):
        self.assertEqual(get_cert_path(True), certifi.where())

    def test_compromised_ca_roots_are_not_trusted(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(cafile=get_cert_path(True))
        names = {
            value
            for certificate in context.get_ca_certs()
            for rdn in certificate["subject"]
            for key, value in rdn
            if key == "commonName"
        }
        self.assertTrue(names)
        self.assertNotIn("AAA Certificate Services", names)
        self.assertNotIn("emSign ECC Root CA - G3", names)


if __name__ == "__main__":
    unittest.main()
