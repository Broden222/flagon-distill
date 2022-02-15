#
# Copyright 2022 The Applied Research Laboratory for Intelligence and Security (ARLIS)
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import distill
import testing_utils
import pytest

def test_segments_constructor():
    segments = distill.Segments()
    assert len(segments) == 0
    assert segments.get_segment_list() == []

def test_segments_general():
    data = testing_utils.setup("./data/sample_data.json", "integer")
    sorted_dict = data[1]

    segments = distill.generate_fixed_time_segments(sorted_dict, 5)

    assert type(segments) == distill.Segments
    assert len(segments) == 4

    index = 0
    for segment in segments:
        assert segment.segment_name == str(index)
        index += 1

def test_segments_subscript():
    data = testing_utils.setup("./data/sample_data.json", "integer")
    sorted_dict = data[1]

    segments = distill.generate_fixed_time_segments(sorted_dict, 5)

    assert type(segments["0"]) == distill.Segment
    assert segments["0"].get_segment_name() == "0"
    assert segments[0].get_segment_name() == "0"
    assert segments["1"].get_segment_name() == "1"
    assert segments[1].get_segment_name() == "1"
    assert segments["2"].get_segment_name() == "2"
    assert segments[2].get_segment_name() == "2"
    assert segments["3"].get_segment_name() == "3"
    assert segments[3].get_segment_name() == "3"

def test_get_segment_list():
    data = testing_utils.setup("./data/sample_data.json", "integer")
    sorted_dict = data[1]

    segments = distill.generate_fixed_time_segments(sorted_dict, 5)

    segments_list = segments.get_segment_list()
    assert type(segments_list) == list
    assert len(segments_list) == 4

def test_get_segment_name_dict():
    data = testing_utils.setup("./data/sample_data.json", "integer")
    sorted_dict = data[1]

    segments = distill.generate_fixed_time_segments(sorted_dict, 5)

    segments_dict = segments.get_segment_name_dict()
    assert type(segments_dict) == dict
    assert len(segments_dict) == 4

def test_get_segment_name_dict_error():
    with pytest.raises(distill.SegmentationError):
        data = testing_utils.setup("./data/sample_data.json", "integer")
        sorted_dict = data[1]

        segments = distill.generate_fixed_time_segments(sorted_dict, 5)
        for segment in segments:
            segment.segment_name = "test"

        segments.get_segment_name_dict()

def test_get_num_logs():
    data = testing_utils.setup("./data/sample_data.json", "integer")
    sorted_dict = data[1]

    segments = distill.generate_fixed_time_segments(sorted_dict, 5)
    assert len(segments) == 4

    result1 = segments.get_num_logs(3)
    assert len(result1) == 3

    for segment in result1:
        assert segment.num_logs >= 3

    result2 = segments.get_num_logs(20)
    assert len(result2) == 0

def test_get_segments_before_integer():
    data = testing_utils.setup("./data/sample_data.json", "integer")
    sorted_dict = data[1]

    segments = distill.generate_fixed_time_segments(sorted_dict, 5)

    result1 = segments.get_segments_before(1623691895656)
    assert len(result1) == 0

    result2 = segments.get_segments_before(1623691900656)
    assert len(result2) == 1
    assert result2[0].segment_name == "0"

    result3 = segments.get_segments_before(1623691905656)
    assert len(result3) == 2
    assert result3[0].segment_name == "0"
    assert result3[1].segment_name == "1"

    result4 = segments.get_segments_before(1623691910656)
    assert len(result4) == 3
    assert result4[0].segment_name == "0"
    assert result4[1].segment_name == "1"
    assert result4[2].segment_name == "2"

    result5 = segments.get_segments_before(2623691910656)
    assert len(result5) == 4
    assert result5[0].segment_name == "0"
    assert result5[1].segment_name == "1"
    assert result5[2].segment_name == "2"
    assert result5[3].segment_name == "3"

def test_get_segments_before_datetime():
    data = testing_utils.setup("./data/sample_data.json", "datetime")
    sorted_dict = data[1]

    segments = distill.generate_fixed_time_segments(sorted_dict, 5)

    result1 = segments.get_segments_before(testing_utils.to_datetime(1623691895656))
    assert len(result1) == 0

    result2 = segments.get_segments_before(testing_utils.to_datetime(1623691900656))
    assert len(result2) == 1
    assert result2[0].segment_name == "0"

    result3 = segments.get_segments_before(testing_utils.to_datetime(1623691905656))
    assert len(result3) == 2
    assert result3[0].segment_name == "0"
    assert result3[1].segment_name == "1"

    result4 = segments.get_segments_before(testing_utils.to_datetime(1623691910656))
    assert len(result4) == 3
    assert result4[0].segment_name == "0"
    assert result4[1].segment_name == "1"
    assert result4[2].segment_name == "2"

    result5 = segments.get_segments_before(testing_utils.to_datetime(2623691910656))
    assert len(result5) == 4
    assert result5[0].segment_name == "0"
    assert result5[1].segment_name == "1"
    assert result5[2].segment_name == "2"
    assert result5[3].segment_name == "3"

def test_get_segments_before_error_1():
    with pytest.raises(TypeError):
        data = testing_utils.setup("./data/sample_data.json", "integer")
        sorted_dict = data[1]

        segments = distill.generate_fixed_time_segments(sorted_dict, 5)

        segments.get_segments_before(testing_utils.to_datetime(1623691895656))

def test_get_segments_before_error_2():
    with pytest.raises(TypeError):
        data = testing_utils.setup("./data/sample_data.json", "integer")
        sorted_dict = data[1]

        segments = distill.generate_fixed_time_segments(sorted_dict, 5)

        segments.get_segments_before("random")

def test_get_segments_of_type():
    data = testing_utils.setup("./data/sample_data.json", "datetime")
    sorted_data = data[0]
    sorted_dict = data[1]

    # Create Segments with fixed time
    segments = distill.generate_fixed_time_segments(sorted_dict, 5)

    # Create Segments with create_segment
    start_end_vals = []
    start_end_vals.append((sorted_data[0][1]['clientTime'], sorted_data[18][1]['clientTime']))
    start_end_vals.append((sorted_data[5][1]['clientTime'], sorted_data[6][1]['clientTime']))
    start_end_vals.append((sorted_data[3][1]['clientTime'], sorted_data[9][1]['clientTime']))

    segment_names = ["test_segment_all", "test_segment_same_client_time", "test_segment_extra_log"]

    create_segments = distill.create_segment(sorted_dict, segment_names, start_end_vals)

    segments.append_segments(create_segments)
    assert len(segments) == 7

    only_fixed_time = segments.get_segments_of_type(distill.Segment_Type.FIXED_TIME)
    assert len(only_fixed_time) == 4
    for segment in only_fixed_time:
        assert segment.segment_type == distill.Segment_Type.FIXED_TIME

    only_create = segments.get_segments_of_type(distill.Segment_Type.CREATE)
    assert len(only_create) == 3
    for segment in only_create:
        assert segment.segment_type == distill.Segment_Type.CREATE

    only_deadspace = segments.get_segments_of_type(distill.Segment_Type.DEADSPACE)
    assert len(only_deadspace) == 0

def test_get_segments_of_type_error():
    with pytest.raises(TypeError):
        data = testing_utils.setup("./data/sample_data.json", "datetime")
        sorted_dict = data[1]
        segments = distill.generate_fixed_time_segments(sorted_dict, 5)
        segments.get_segments_of_type("random")

def test_append():
    data = testing_utils.setup("./data/sample_data.json", "integer")
    sorted_data = data[0]
    sorted_dict = data[1]

    # Create Segments with fixed time
    segments = distill.generate_fixed_time_segments(sorted_dict, 5)

    # Create Segments with create_segment
    start_end_vals = []
    start_end_vals.append((sorted_data[0][1]['clientTime'], sorted_data[18][1]['clientTime']))
    start_end_vals.append((sorted_data[5][1]['clientTime'], sorted_data[6][1]['clientTime']))
    start_end_vals.append((sorted_data[3][1]['clientTime'], sorted_data[9][1]['clientTime']))
    segment_names = ["test_segment_all", "test_segment_same_client_time", "test_segment_extra_log"]
    create_segments = distill.create_segment(sorted_dict, segment_names, start_end_vals)

    segments.append(create_segments[0])

    assert len(segments) == 5
    assert segments[-1].segment_name == "test_segment_all"

def test_append_error():
    with pytest.raises(TypeError):
        data = testing_utils.setup("./data/sample_data.json", "integer")
        sorted_dict = data[1]

        # Create Segments with fixed time
        segments = distill.generate_fixed_time_segments(sorted_dict, 5)

        segments.append("random")

def test_append_segments():
    data = testing_utils.setup("./data/sample_data.json", "integer")
    sorted_data = data[0]
    sorted_dict = data[1]

    # Create Segments with fixed time
    segments = distill.generate_fixed_time_segments(sorted_dict, 5)

    # Create Segments with create_segment
    start_end_vals = []
    start_end_vals.append((sorted_data[0][1]['clientTime'], sorted_data[18][1]['clientTime']))
    start_end_vals.append((sorted_data[5][1]['clientTime'], sorted_data[6][1]['clientTime']))
    start_end_vals.append((sorted_data[3][1]['clientTime'], sorted_data[9][1]['clientTime']))
    segment_names = ["test_segment_all", "test_segment_same_client_time", "test_segment_extra_log"]
    create_segments = distill.create_segment(sorted_dict, segment_names, start_end_vals)

    segments.append_segments(create_segments)
    assert len(segments) == 7
    assert segments[0].segment_name == "0"
    assert segments[1].segment_name == "1"
    assert segments[2].segment_name == "2"
    assert segments[3].segment_name == "3"
    assert segments[4].segment_name == "test_segment_all"
    assert segments[5].segment_name == "test_segment_same_client_time"
    assert segments[6].segment_name == "test_segment_extra_log"

def test_append_segments_error():
    with pytest.raises(TypeError):
        data = testing_utils.setup("./data/sample_data.json", "integer")
        sorted_dict = data[1]

        # Create Segments with fixed time
        segments = distill.generate_fixed_time_segments(sorted_dict, 5)

        segments.append_segments("random")

def test_delete():
    data = testing_utils.setup("./data/sample_data.json", "integer")
    sorted_dict = data[1]

    # Create Segments with fixed time
    segments = distill.generate_fixed_time_segments(sorted_dict, 5)
    assert len(segments) == 4

    segments.delete("2")
    assert len(segments) == 3
    assert segments[0].segment_name == "0"
    assert segments[1].segment_name == "1"
    assert segments[2].segment_name == "3"

def test_delete_error():
    with pytest.raises(distill.SegmentationError):
        data = testing_utils.setup("./data/sample_data.json", "integer")
        sorted_dict = data[1]

        # Create Segments with fixed time
        segments = distill.generate_fixed_time_segments(sorted_dict, 5)

        segments.delete("random")

def test_str():
    segment = distill.Segment("segment_name", (1, 2), 5, ["uid1", "uid2"])

    # Create Segments with fixed time
    segments = distill.Segments([segment])

    assert str(segments) == "Segments: [\n" \
                            "Segment: name=segment_name, num_logs=5, start=1, end=2, type=None\n" \
                            "]"