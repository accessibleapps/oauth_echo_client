"""Local regressions for OAuth Echo construction and request forwarding."""

import importlib
import sys
import unittest
from unittest.mock import Mock, patch


class OAuthEchoClientTests(unittest.TestCase):
    def setUp(self):
        self.oauth2 = Mock()
        with patch.dict(sys.modules, {"oauth2": self.oauth2}):
            sys.modules.pop("oauth_echo_client", None)
            self.module = importlib.import_module("oauth_echo_client")

    def test_constructor_preserves_supplied_oauth_realm(self):
        with patch.object(self.module.requests, "session"):
            client = self.module.OAuthEchoClient(
                oauth_realm="https://api.example.test",
                consumer_key="consumer",
                consumer_secret="secret",
            )

        self.assertEqual(client.oauth_realm, "https://api.example.test")

    def test_post_signs_and_forwards_keyword_parameters(self):
        # Isolate post() from construction so both regressions fail independently.
        client = self.module.OAuthEchoClient.__new__(self.module.OAuthEchoClient)
        client.consumer = object()
        client.access_token = None
        client.callback_url = "https://api.example.test/verify"
        client.signature_method = object()
        client.API_key = "example-api-key"
        client.oauth_realm = "https://api.example.test"
        client.session = Mock()
        client.session.post.return_value.content = b"response"
        request = self.oauth2.Request.from_consumer_and_token.return_value
        request.to_header.return_value = {"Authorization": "signed-example"}

        result = client.post(
            "https://echo.example.test/post", data={"text": "example"}, media=False
        )

        request.set_parameter.assert_any_call("media", False)
        request.to_header.assert_called_once_with(realm=client.oauth_realm)
        client.session.post.assert_called_once_with(
            "https://echo.example.test/post",
            data={"text": "example"},
            params={"media": False},
            headers={
                "X-Verify-Credentials-Authorization": "signed-example",
                "X-Auth-Service-Provider": client.callback_url,
            },
        )
        client.session.post.return_value.raise_for_status.assert_called_once_with()
        self.assertEqual(result, b"response")


if __name__ == "__main__":
    unittest.main()
