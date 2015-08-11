import boto.dynamodb2
import credstash

from moto import mock_dynamodb2, mock_kms
from unittest import TestCase


class CredstashTester(TestCase):
    def test_pass(self):
        assert True

    @mock_dynamodb2
    def test_table_create(self):
        table_name = "test_table"
        credstash.createDdbTable(table=table_name)
        
        conn =  boto.dynamodb2.connect_to_region(
            'us-west-2',
            aws_access_key_id="ak",
            aws_secret_access_key="sk")
        assert conn.list_tables()["TableNames"] == [table_name]

    @mock_dynamodb2
    @mock_kms
    def test_encrypt(self):
        # set up fake KMS master key
        kms = boto.connect_kms()
        create_resp = kms.create_key()
        key_id = create_resp['KeyMetadata']['KeyId']
        resp = kms.create_alias('alias/credstash', key_id)

        credstash.createDdbTable()

        name = "password"
        secret = "super secret"

        credstash.putSecret(name, secret, 1)
        resp = credstash.getSecret(name)
        assert resp == secret
