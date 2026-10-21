import unittest
from unittest.mock import Mock

import boto3
from botocore.stub import Stubber

from aws_quota.check.ec2 import ElasticIpCountCheck


class ElasticIpCountCheckTests(unittest.TestCase):
    def test_counts_only_customer_managed_addresses(self):
        cases = [
            ("empty", [], 0),
            ("customer", [{"PublicIp": "192.0.2.1"}, {"PublicIp": "192.0.2.2"}], 2),
            ("service", [{"ServiceManaged": "alb"}] * 5, 0),
            ("mixed", [{"PublicIp": "192.0.2.1"}, {"ServiceManaged": "alb"}], 1),
            ("other services", [{"ServiceManaged": service} for service in ("nlb", "rnat", "rds")], 0),
        ]
        client = boto3.client(
            "ec2", region_name="us-east-1",
            aws_access_key_id="testing", aws_secret_access_key="testing",
        )
        session = Mock()
        session.client.side_effect = lambda service, **kwargs: client if service == "ec2" else Mock()
        check = ElasticIpCountCheck(session)
        for name, addresses, expected in cases:
            with self.subTest(name=name), Stubber(client) as stubber:
                stubber.add_response("describe_addresses", {"Addresses": addresses}, {})
                self.assertEqual(check.current, expected)
                stubber.assert_no_pending_responses()


if __name__ == "__main__":
    unittest.main()
