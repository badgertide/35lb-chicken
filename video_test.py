import unittest
from unittest.mock import Mock, patch
from pathlib import Path


def setup_context():
    # sys_stub = Mock()
    json5_stub = Mock()
    utils_stub = Mock()
    constants = Mock()

    json5_stub.parse.return_value = "test_data"
    utils_stub.log.return_value = ""
    utils_stub.run.return_value = ""
    utils_stub.run_capture.return_value = "test_data"
    constants.FILLER_TYPES = ["filler"]
    constants.MAX_LOOPS = 5,
    constants.CUT_FILE_PREFIX = "test-"

    return {
        "mocks": {
            "json5": json5_stub,
            "utils": utils_stub,
            "constants": constants,
        }
    }


class Test(unittest.TestCase):

    def setUp(self):
        self.context = setup_context()
        self.mocks = self.context["mocks"]
        self.open_patcher = patch("builtins.open", unittest.mock.mock_open(read_data="testData"))
        self.open_patcher.start()
        #///

        self.json5_patcher = patch("video.json5", self.mocks["json5"])
        self.json5_patcher.start()
        self.utils_patcher = patch("video.Utils", self.mocks["utils"])
        self.utils_patcher.start()
        self.constants_patcher = patch("video.c", self.mocks["constants"])
        self.constants_patcher.start()

        import video
        self.unit = video

    def tearDown(self):
        self.open_patcher.stop()
        self.json5_patcher.stop()
        self.utils_patcher.stop()
        self.constants_patcher.stop()

    # === tests
    # ===============================================================

    # ==== load_segments_from_map ====

    def test_lsfm_one_segment_passes(self):
        dummy_llc_data = {
            "version": 2,
            "mediaFileName": 'Test File.mkv',
            "cutSegments": [
                {
                "start": 0,
                "end": 10.0,
                "name": 'test',
                "selected": True,
                },
            ],
        }
        expected_result = [
            {
                "start": 0,
                "end": 10.0,
                "duration": 10.0,
                "filename": "segment_00",
                "label": "test",
            }
        ]
        dummy_llc = [dummy_llc_data]
        self.mocks["json5"].parse.return_value = dummy_llc

        result = self.unit.load_segments_from_map(Path(r"test\filepath"))

        self.assertEqual(result, expected_result)
    
    def test_lsfm_two_segments_passes(self):
        dummy_llc_data = {
            "version": 2,
            "mediaFileName": 'Test File.mkv',
            "cutSegments": [
                {
                "start": 0,
                "end": 10.0,
                "name": 'test',
                "selected": True,
                },
                {
                "start": 10.0,
                "end": 20.0,
                "name": 'also test',
                "selected": True,
                },
            ],
        }
        expected_result = [
            {
                "start": 0,
                "end": 10.0,
                "duration": 10.0,
                "filename": "segment_00",
                "label": "test",
            },
            {
                "start": 10.0,
                "end": 20.0,
                "duration": 10.0,
                "filename": "segment_01",
                "label": "also test",
            }
        ]
        dummy_llc = [dummy_llc_data]
        self.mocks["json5"].parse.return_value = dummy_llc

        result = self.unit.load_segments_from_map(Path(r"test\filepath"))

        self.assertEqual(result, expected_result)

    def test_lsfm_skip_blank_label_one_result(self):
        dummy_llc_data = {
            "version": 2,
            "mediaFileName": 'Test File.mkv',
            "cutSegments": [
                {
                "start": 0,
                "end": 10.0,
                "selected": True,
                },
                {
                "start": 10.0,
                "end": 20.0,
                "name": 'test',
                "selected": True,
                },
            ],
        }
        expected_result = [
            {
                "start": 10.0,
                "end": 20.0,
                "duration": 10.0,
                "filename": "segment_01",
                "label": "test",
            }
        ]
        dummy_llc = [dummy_llc_data]
        self.mocks["json5"].parse.return_value = dummy_llc

        result = self.unit.load_segments_from_map(Path(r"test\filepath"))

        self.assertEqual(result, expected_result)

    def test_lsfm_blank_label_no_results_raises_error(self):
        dummy_llc_data = {
            "version": 2,
            "mediaFileName": 'Test File.mkv',
            "cutSegments": [
                {
                "start": 0,
                "end": 10.0,
                "selected": True,
                },
            ],
        }
        dummy_llc = [dummy_llc_data]
        self.mocks["json5"].parse.return_value = dummy_llc

        self.assertRaises(RuntimeError, self.unit.load_segments_from_map, Path(r"test\filepath"))
    
    def test_lsfm_negative_duration_raises_error(self):
        dummy_llc_data = {
            "version": 2,
            "mediaFileName": 'Test File.mkv',
            "cutSegments": [
                {
                "start": 10.0,
                "end": 0,
                "name": 'test',
                "selected": True,
                },
            ],
        }
        dummy_llc = [dummy_llc_data]
        self.mocks["json5"].parse.return_value = dummy_llc

        self.assertRaises(ValueError, self.unit.load_segments_from_map, Path(r"test\filepath"))

    # ==== parse_segment_cuts ====

    # This function cuts up all segments, discards unwanted filler, and returns
    # all of the segments in order. Any non-generic segments are automatically
    # accepted. Any generic segments are checked for overlapping filler segments
    # and sliced accordingly.
    # INPUT:
    #     base_segments: [
    #     	{label: string, start: float, end: float, ...}
    #     ]
    #     options: {filler_type: int}
    # OUTPUT:
    #     sliced_segments: [
    #     	{label: string, start: float, end: float, ...},
    #     	{label: string, start: float, end: float, ...}
    #     ]

    def test_psc__no_cuts(self):
        dummy_base_segments = [
            {
            "start": 0,
            "end": 10.0,
            "label": 'generic'
            },
            {
            "start": 10.0,
            "end": 20.0,
            "label": 'generic'
            },
            {
            "start": 20.0,
            "end": 40.0,
            "label": 'generic'
            },
        ]
        dummy_options = [1,1,0,1,1,1,2,1,4,0] # Default
        expected_result = [
            {
            "start": 0,
            "end": 10.0,
            "label": 'generic'
            },
            {
            "start": 10.0,
            "end": 20.0,
            "label": 'generic'
            },
            {
            "start": 20.0,
            "end": 40.0,
            "label": 'generic'
            },
        ]
        self.slice_generic_patcher = patch("video.slice_generic_by_fillers", return_value=expected_result)

        result = self.unit.parse_segment_cuts(dummy_base_segments, dummy_options)

        self.assertEqual(result, expected_result)
    
    # ==== slice_generic_by_fillers ====

    def test_sgbf__case(self):
        self.assertEqual(True, 1)
    
    # ==== ffprobe_streams ====

    def test_fs__case(self):
        self.assertEqual(True, 1)
    
    # ==== build_ffmpeg_streammaps ====

    def test_bfs__case(self):
        self.assertEqual(True, 1)
    
    # ==== make_reencode_segment ====

    def test_mrs__case(self):
        self.assertEqual(True, 1)
    
    # ==== concat_segments ====

    def test_cs__case(self):
        self.assertEqual(True, 1)
    
    # ==== process_file ====

    def test_pf__case(self):
        self.assertEqual(True, 1)

if __name__ == "__main__":
    unittest.main(exit=False)