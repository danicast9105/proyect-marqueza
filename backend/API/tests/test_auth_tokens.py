import unittest

from Services.auth_tokens import (
    InvalidAccessToken,
    TokenConfigurationError,
    create_access_token,
    verify_access_token,
)


class AccessTokenTests(unittest.TestCase):
    secret = "test-secret-with-at-least-32-characters"

    def test_created_token_contains_subject_and_role(self):
        token, token_id = create_access_token("user-123", "Administrador", self.secret, 3600)

        payload = verify_access_token(token, self.secret)

        self.assertEqual(payload["sub"], "user-123")
        self.assertEqual(payload["role"], "Administrador")
        self.assertEqual(payload["jti"], token_id)
        self.assertGreater(payload["exp"], payload["iat"])

    def test_expired_token_is_rejected(self):
        token, _ = create_access_token("user-123", "Administrador", self.secret, 1)

        with self.assertRaises(InvalidAccessToken):
            verify_access_token(token, self.secret, now=9999999999)

    def test_token_signed_with_another_secret_is_rejected(self):
        token, _ = create_access_token("user-123", "Administrador", self.secret, 3600)

        with self.assertRaises(InvalidAccessToken):
            verify_access_token(token, "different-secret-with-at-least-32-characters")

    def test_persistent_token_has_no_expiration_and_is_unique(self):
        first_token, first_id = create_access_token("user-123", "Administrador", self.secret)
        second_token, second_id = create_access_token("user-123", "Administrador", self.secret)

        first_payload = verify_access_token(first_token, self.secret, now=9999999999)
        self.assertNotIn("exp", first_payload)
        self.assertNotEqual(first_id, second_id)
        self.assertNotEqual(first_token, second_token)

    def test_malformed_token_is_rejected(self):
        with self.assertRaises(InvalidAccessToken):
            verify_access_token("not-a-token", self.secret)

    def test_non_ascii_token_is_rejected(self):
        with self.assertRaises(InvalidAccessToken):
            verify_access_token("á.invalid", self.secret)

    def test_short_secret_is_rejected(self):
        with self.assertRaises(TokenConfigurationError):
            create_access_token("user-123", "Administrador", "too-short", 3600)


if __name__ == "__main__":
    unittest.main()
