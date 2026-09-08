import pytest

from panchanga_core.rules.karana import karana_name_for_index, MOVABLE_KARANAS


def test_fixed_karanas_at_expected_indices():
    assert karana_name_for_index(0) == "Kimstughna"
    assert karana_name_for_index(57) == "Shakuni"
    assert karana_name_for_index(58) == "Chatushpada"
    assert karana_name_for_index(59) == "Naga"


def test_movable_karanas_cycle_starting_after_kimstughna():
    # Indices 1-56 cycle through the 7 movable karanas 8 times.
    for i in range(1, 57):
        expected = MOVABLE_KARANAS[(i - 1) % 7]
        assert karana_name_for_index(i) == expected


def test_movable_karanas_cycle_exactly_eight_times():
    names = [karana_name_for_index(i) for i in range(1, 57)]
    assert len(names) == 56
    for karana in MOVABLE_KARANAS:
        assert names.count(karana) == 8


def test_bava_is_first_movable_karana():
    assert karana_name_for_index(1) == "Bava"


def test_out_of_range_raises_value_error():
    with pytest.raises(ValueError):
        karana_name_for_index(-1)
    with pytest.raises(ValueError):
        karana_name_for_index(60)
