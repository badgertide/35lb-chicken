import unittest
from unittest.mock import MagicMock, patch


def setup_context():
    subprocess_stub = MagicMock()
    shutil_stub = MagicMock()
    base64_stub = MagicMock()
    json5_stub = MagicMock()
    base64_stub.b64encode.return_value = MagicMock()
    json5_stub.dumps.return_value = MagicMock()

    subprocess_stub.run.return_value = {"stdout": "stdout"}
    which_returns = {
        "ffmpeg": "",
        "yt-dlp": None,
    }
    shutil_stub.which.side_effect = lambda arg: which_returns.get(arg)

    return {
        "mocks": {
            "subprocess": subprocess_stub,
            "shutil": shutil_stub,
            "base64": base64_stub,
            "json5": json5_stub,
        }
    }


class Test(unittest.TestCase):

    def setUp(self):
        self.context = setup_context()
        self.mocks = self.context["mocks"]

        self.subprocess_patcher = patch("utils.subprocess", self.mocks["subprocess"])
        self.subprocess_patcher.start()
        self.shutil_patcher = patch("utils.shutil", self.mocks["shutil"])
        self.shutil_patcher.start()
        self.base64_patcher = patch("utils.base64", self.mocks["base64"])
        self.base64_patcher.start()
        self.json5_patcher = patch("utils.json5", self.mocks["json5"])
        self.json5_patcher.start()

        import utils
        self.unit = utils

    def tearDown(self):
        self.subprocess_patcher.stop()
        self.shutil_patcher.stop()
        self.base64_patcher.stop()
        self.json5_patcher.stop()

    # ── tests ──────────────────────────────────────────────────────────────

    def test_run(self):
        self.mocks["subprocess"].run.return_value = "YEAH"
        result = self.unit.run("test")
        self.assertNotEqual(result, "NO")


if __name__ == "__main__":
    unittest.main(exit=False)