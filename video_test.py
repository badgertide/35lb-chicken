import unittest
from unittest.mock import Mock, patch
from pathlib import Path


def setup_context():
    # sys_stub = Mock()
    json5_stub = Mock()
    utils_stub = Mock()
    constants = Mock()
    cut_config = Mock()

    json5_stub.parse.return_value = "test_data"
    utils_stub.log.return_value = ""
    utils_stub.run.return_value = ""
    utils_stub.run_capture.return_value = "test_data"

    constants.FILLER_TYPES = ["test_filler"]
    constants.MAX_LOOPS = 5
    constants.CUT_FILE_PREFIX = "test-"

    cut_config.get_selected_fillers.return_value = ["test_filler"]

    return {
        "mocks": {
            "json5": json5_stub,
            "utils": utils_stub,
            "constants": constants,
            "cut_config": cut_config,
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
        self.config_patcher = patch("video.cut_config", self.mocks["cut_config"])
        self.config_patcher.start()

        import video
        self.unit = video

    def tearDown(self):
        self.open_patcher.stop()
        self.json5_patcher.stop()
        self.utils_patcher.stop()
        self.constants_patcher.stop()
        self.config_patcher.stop()

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
            {"start": 0,"end": 10.0,"label": 'generic'},
            {"start": 10.0,"end": 20.0,"label": 'generic'},
            {"start": 20.0,"end": 40.0,"label": 'generic'},
        ]
        expected_result = [
            {"start": 0, "end": 10.0, "label": 'generic'},
            {"start": 10.0, "end": 20.0, "label": 'generic'},
            {"start": 20.0, "end": 40.0, "label": 'generic'},
        ]
        def mock_slice_generic_side_effects(a, b):
            return [a]
        self.slice_generic_patcher = patch("video.slice_generic_by_fillers", side_effect=mock_slice_generic_side_effects)
        self.slice_generic_patcher.start()

        result = self.unit.parse_segment_cuts(dummy_base_segments)

        self.slice_generic_patcher.stop()
        self.assertEqual(result, expected_result)

    def test_psc__no_cuts__out_of_order(self):
        dummy_base_segments = [
            {"start": 20.0,"end": 40.0,"label": 'generic'},
            {"start": 10.0,"end": 20.0,"label": 'generic'},
            {"start": 0,"end": 10.0,"label": 'generic'},
        ]
        expected_result = [
            {"start": 0,"end": 10.0,"label": 'generic'},
            {"start": 10.0,"end": 20.0,"label": 'generic'},
            {"start": 20.0,"end": 40.0,"label": 'generic'},
        ]
        def mock_slice_generic_side_effects(a, b):
            return [a]
        self.slice_generic_patcher = patch("video.slice_generic_by_fillers", side_effect=mock_slice_generic_side_effects)
        self.slice_generic_patcher.start()

        result = self.unit.parse_segment_cuts(dummy_base_segments)

        self.slice_generic_patcher.stop()
        self.assertEqual(result, expected_result)

    def test_psc__no_cuts__out_of_order__generic_first(self):
        dummy_base_segments = [
            {"start": 0,"end": 5.0,"label": 'themeopen'},
            {"start": 20.0,"end": 40.0,"label": 'generic'},
            {"start": 10.0,"end": 20.0,"label": 'generic'},
            {"start": 0,"end": 10.0,"label": 'generic'},
        ]
        # if "generic" starts at the same time as any other segment, it should be first in line
        expected_result = [
            {"start": 0,"end": 10.0,"label": 'generic'},
            {"start": 0,"end": 5.0,"label": 'themeopen'},
            {"start": 10.0,"end": 20.0,"label": 'generic'},
            {"start": 20.0,"end": 40.0,"label": 'generic'},
        ]
        def mock_slice_generic_side_effects(a, b):
            return [a]
        self.slice_generic_patcher = patch("video.slice_generic_by_fillers", side_effect=mock_slice_generic_side_effects)
        self.slice_generic_patcher.start()

        result = self.unit.parse_segment_cuts(dummy_base_segments)

        self.slice_generic_patcher.stop()
        self.assertEqual(result, expected_result)
    
    def test_psc__one_cut(self):
        dummy_base_segments = [
            {"start": 0,"end": 10.0,"label": 'generic'},
            {"start": 5.0,"end": 7.0,"label": 'test_filler'},
            {"start": 20.0,"end": 40.0,"label": 'generic'},
        ]
        # if "generic" starts at the same time as any other segment, it should be first in line
        expected_result = [
            {"start": 0,"end": 5.0,"label": 'generic'},
            {"start": 7.0,"end": 10.0,"label": 'generic'},
            {"start": 20.0,"end": 40.0,"label": 'generic'},
        ]
        def mock_slice_generic_side_effects(a, b):
            if (a, b) == (dummy_base_segments[0], [dummy_base_segments[1]]):
                return expected_result[0:2]
            return [a]
        self.slice_generic_patcher = patch("video.slice_generic_by_fillers", side_effect=mock_slice_generic_side_effects)
        self.slice_generic_patcher.start()

        result = self.unit.parse_segment_cuts(dummy_base_segments)

        self.slice_generic_patcher.stop()
        self.assertEqual(result, expected_result)

    def test_psc__two_cuts(self):
        dummy_base_segments = [
            {"start": 0,"end": 40.0,"label": 'generic'},
            {"start": 5.0,"end": 7.0,"label": 'test_filler'},
            {"start": 20.0,"end": 35.0,"label": 'test_filler'},
        ]
        # two cuts from the middle of a segment will result in 3 segments
        expected_result = [
            {"start": 0,"end": 5.0,"label": 'generic'},
            {"start": 7.0,"end": 20.0,"label": 'generic'},
            {"start": 35.0,"end": 40.0,"label": 'generic'},
        ]
        def mock_slice_generic_side_effects(a, b):
            generic = {"start": 0,"end": 40.0,"label": 'generic'}
            fillers = [
                {"start": 5.0,"end": 7.0,"label": 'test_filler'},
                {"start": 20.0,"end": 35.0,"label": 'test_filler'}]
            if (a, b) == (generic, fillers):
                return expected_result
            return []
        self.slice_generic_patcher = patch("video.slice_generic_by_fillers", side_effect=mock_slice_generic_side_effects)
        self.slice_generic_patcher.start()

        result = self.unit.parse_segment_cuts(dummy_base_segments)

        self.slice_generic_patcher.stop()
        self.assertEqual(result, expected_result)

    # ==== slice_filler_from_segment ====

    def test_sffs__filler_is_in_middle(self):
        dummy_generic = {"start": 0,"end": 40.0,"filename": 'genericFilename'}
        dummy_filler = {"start": 10.0,"end": 15.0,"filename": 'fillerFilename'}
        
        expected_result = [
            {"start": 0,"end": 10.0, "duration": 10.0,"filename": 'genericFilename_0'},
            {"start": 15.0,"end": 40.0, "duration": 25.0,"filename": 'genericFilename_1'},
        ]

        result = self.unit.slice_filler_from_segment(dummy_generic, dummy_filler)

        self.assertEqual(result, expected_result)

    def test_sffs__filler_is_at_start(self):
        dummy_generic = {"start": 0,"end": 40.0,"filename": 'genericFilename'}
        dummy_filler = {"start": 0,"end": 15.0,"filename": 'fillerFilename'}
        
        expected_result = [
            {"start": 15.0,"end": 40.0, "duration": 25.0,"filename": 'genericFilename_1'},
        ]

        result = self.unit.slice_filler_from_segment(dummy_generic, dummy_filler)

        self.assertEqual(result, expected_result)

    def test_sffs__filler_is_at_end(self):
        dummy_generic = {"start": 0,"end": 40.0,"filename": 'genericFilename'}
        dummy_filler = {"start": 10.0,"end": 40.0,"filename": 'fillerFilename'}
        
        expected_result = [
            {"start": 0,"end": 10.0, "duration": 10.0,"filename": 'genericFilename_0'},
        ]

        result = self.unit.slice_filler_from_segment(dummy_generic, dummy_filler)

        self.assertEqual(result, expected_result)

    def test_sffs__filler_matches_segment(self):
        dummy_generic = {"start": 0,"end": 40.0,"filename": 'genericFilename'}
        dummy_filler = {"start": 0,"end": 40.0,"filename": 'fillerFilename'}
        
        expected_result = []

        result = self.unit.slice_filler_from_segment(dummy_generic, dummy_filler)

        self.assertEqual(result, expected_result)

    # ==== slice_generic_by_fillers ====

    @unittest.expectedFailure
    def test_sgbf__no_filler(self):
        dummy_generic = {"start": 10.0,"end": 20.0,"label": 'generic', "filename": ""}
        dummy_fillers = []
        expected_result = [
            {"start": 10.0,"end": 20.0,"label": 'generic'},
        ]
        self.slice_filler_patcher = patch("video.slice_filler_from_segment", side_effect=expected_result)
        self.slice_filler_patcher.start()

        result = self.unit.slice_generic_by_fillers(dummy_generic, dummy_fillers)

        self.slice_filler_patcher.stop()
        self.assertEqual(result, expected_result)

    @unittest.expectedFailure
    def test_sgbf__no_intersecting_filler(self):
        dummy_generic = {"start": 10.0,"end": 20.0,"label": 'generic', "filename": ""}
        dummy_fillers = [{"start": 30.0,"end": 35.0,"label": 'test_filler'}]
        expected_result = [
            {"start": 10.0,"end": 20.0,"label": 'generic'},
        ]
        self.slice_filler_patcher = patch("video.slice_filler_from_segment", side_effect=expected_result)
        self.slice_filler_patcher.start()

        result = self.unit.slice_generic_by_fillers(dummy_generic, dummy_fillers)

        self.slice_filler_patcher.stop()
        self.assertEqual(result, expected_result)

    def test_sgbf__one_filler(self):
        dummy_generic = {"start": 10.0,"end": 20.0,"label": 'generic', "filename": ""}
        dummy_fillers = [
            {"start": 15.0,"end": 16.0,"label": 'test_filler'}
        ]
        expected_result = [
            {"start": 10.0,"end": 15.0,"label": 'generic'},
            {"start": 16.0,"end": 20.0,"label": 'generic'},
        ]
        def mock_slice_filler_side_effects(a, b):
            return expected_result
        self.slice_filler_patcher = patch("video.slice_filler_from_segment", side_effect=mock_slice_filler_side_effects)
        self.slice_filler_patcher.start()

        result = self.unit.slice_generic_by_fillers(dummy_generic, dummy_fillers)

        self.slice_filler_patcher.stop()
        self.assertEqual(result, expected_result)

    def test_sgbf__two_filler(self):
        dummy_generic = {"start": 10.0,"end": 20.0,"label": 'generic', "filename": ""}
        dummy_fillers = [
            {"start": 11.0,"end": 13.0,"label": 'test_filler'},
            {"start": 15.0,"end": 16.0,"label": 'test_filler'}
        ]
        expected_result = [
            {"start": 10.0,"end": 11.0,"label": 'generic'},
            {"start": 13.0,"end": 15.0,"label": 'generic'},
            {"start": 16.0,"end": 20.0,"label": 'generic'},
        ]
        mock_slice_filler_side_effects = [
            [{"start": 10.0,"end": 11.0,"label": 'generic'}, {"start": 13.0,"end": 20.0,"label": 'generic'}],
            [{"start": 13.0,"end": 15.0,"label": 'generic'}, {"start": 16.0,"end": 20.0,"label": 'generic'}]
        ]
        self.slice_filler_patcher = patch("video.slice_filler_from_segment", side_effect=mock_slice_filler_side_effects)
        self.slice_filler_patcher.start()

        result = self.unit.slice_generic_by_fillers(dummy_generic, dummy_fillers)

        self.slice_filler_patcher.stop()
        self.assertEqual(result, expected_result)

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