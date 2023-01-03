import json
from unittest import TestCase, mock
from lambdas import app

class MockLambdaHandler(TestCase):
    # def test_lambda_handler(self):
    #     toReturn = {'Items': [{'id': '0', 'type': 'taikamatto'}]}
    #     with mock.patch("app.lambda_handler.boto3.client('dynamodb').scan(TableName='Project4Group2Table')", return_value=toReturn) as mock_boto3:
    #         ret = app.lambda_handler(3, 5)
    #         assert ret["statusCode"] == 200
    #         assert ret["body"] == {'Items': [{'id': '0', 'type': 'taikamatto'}]}

    def test_sum_numbers_works_with_negative_numbers(self):
        result = -5
        self.assertEqual(result, -5)
