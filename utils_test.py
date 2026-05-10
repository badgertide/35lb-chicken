import unittest
from unittest.mock import Mock, patch


def setup_context():
    subprocess_stub = Mock()
    shutil_stub = Mock()
    base64_stub = Mock()
    json5_stub = Mock()
    base64_stub.b64encode.return_value = Mock()
    json5_stub.dumps.return_value = Mock()

    subprocess_stub.run.return_value = Mock(stdout="stdout")
    which_returns = {
        "ffmpeg": "ffmpeg/path",
        "yt-dlp": "yt-dlp/path",
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
        self.print_patcher = patch("builtins.print")
        self.print_patcher.start()

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
        self.print_patcher.stop()
        self.subprocess_patcher.stop()
        self.shutil_patcher.stop()
        self.base64_patcher.stop()
        self.json5_patcher.stop()

    # === tests
    # ===============================================================

    def test_run(self):
        result = self.unit.run("test")
        self.assertEqual(result, None)
        self.mocks["subprocess"].run.assert_called_with("test", check=True)

    # ==========

    def test_run_capture(self):
        result = self.unit.run_capture("test")
        args, kwargs = self.mocks["subprocess"].run.call_args

        self.assertEqual(result, "stdout")
        self.assertEqual(args[0], "test")

    # ==========


    def test_time_to_seconds__zero(self):
        result = self.unit.time_to_seconds("0:00:00")
        self.assertEqual(result, 0.0)

    def test_time_to_seconds__hour(self):
        result = self.unit.time_to_seconds("1:00:00")
        self.assertEqual(result, 3600.0)

    def test_time_to_seconds__negative_hour(self):
        result = self.unit.time_to_seconds("-1:00:00")
        self.assertEqual(result, -3600.0)

    def test_time_to_seconds__arbitrary(self):
        result = self.unit.time_to_seconds("46:12:53.12345")
        self.assertEqual(result, 166373.12345)

    def test_time_to_seconds__invalid_timestamp_minutes(self):
        self.assertRaises(ValueError, self.unit.time_to_seconds, "12:00")

    def test_time_to_seconds__invalid_timestamp_seconds(self):
        self.assertRaises(ValueError, self.unit.time_to_seconds, "53")

    # ==========

    def test_check_dependency__ffmpeg_exists(self):
        result = self.unit.check_dependency("ffmpeg")
        self.assertTrue(result)

    def test_check_dependency__ytdlp_exists(self):
        result = self.unit.check_dependency("yt-dlp")
        self.assertTrue(result)

    def test_check_dependency__not_exists(self):
        result = self.unit.check_dependency("invalid-package")
        self.assertFalse(result)

    # ==========

    def test_replace_element_with_list__first(self):
        result = self.unit.replace_element_with_list([1,2,3], [4,5,6], 0)
        self.assertEqual(result, [4,5,6,2,3])

    def test_replace_element_with_list__mid(self):
        result = self.unit.replace_element_with_list([1,2,3], [4,5,6], 1)
        self.assertEqual(result, [1,4,5,6,3])

    def test_replace_element_with_list__last(self):
        result = self.unit.replace_element_with_list([1,2,3], [4,5,6], 2)
        self.assertEqual(result, [1,2,4,5,6])

    def test_replace_element_with_list__empty(self):
        result = self.unit.replace_element_with_list([1,2,3], [], 1)
        self.assertEqual(result, [1,3])

if __name__ == "__main__":
    unittest.main(exit=False)