from datetime import datetime

import pytest

from panchanga_core.rules.vara_and_kalam import gulika_kalam, rahu_kalam, yamaganda


def test_rahu_kalam_ordered_for_correctly_paired_sunrise_sunset():
    sunrise_utc = datetime(2026, 11, 1, 0, 47)
    sunset_utc = datetime(2026, 11, 1, 12, 25)

    window = rahu_kalam(sunrise_utc, sunset_utc, "Sunday")

    assert window.start_utc < window.end_utc
    assert sunrise_utc <= window.start_utc
    assert window.end_utc <= sunset_utc


@pytest.mark.parametrize("rule", [rahu_kalam, yamaganda, gulika_kalam])
def test_inverted_sunrise_sunset_raises_instead_of_producing_backwards_window(rule):
    # This is the exact failure mode from issue #7: a sample instant that
    # falls between today's sunrise and today's sunset causes "next
    # occurrence after this instant" semantics to pair today's sunset with
    # TOMORROW's sunrise, so sunrise_utc ends up after sunset_utc.
    sunrise_utc = datetime(2026, 11, 2, 0, 47)  # tomorrow's sunrise
    sunset_utc = datetime(2026, 11, 1, 12, 25)  # today's sunset

    with pytest.raises(ValueError):
        rule(sunrise_utc, sunset_utc, "Sunday")
