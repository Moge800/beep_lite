"""Tests for Sound enum type."""

import pytest

from beep_lite.types import Sound


class TestSound:
    """Test cases for Sound enum."""

    def test_all_sound_values_are_strings(self) -> None:
        """All Sound enum values should be strings."""
        for sound in Sound:
            assert isinstance(sound.value, str)

    def test_sound_count(self) -> None:
        """Should have exactly 8 sound types."""
        assert len(Sound) == 8

    def test_expected_sounds_exist(self) -> None:
        """All expected sound types should be defined."""
        expected = ["ok", "ng", "warn", "crit", "moo", "mew", "scan_ok", "scan_ng"]
        actual = [s.value for s in Sound]
        assert sorted(actual) == sorted(expected)

    def test_sound_from_value(self) -> None:
        """Should be able to create Sound from string value."""
        assert Sound("ok") == Sound.OK
        assert Sound("ng") == Sound.NG
        assert Sound("scan_ok") == Sound.SCAN_OK

    def test_invalid_sound_value_raises(self) -> None:
        """Invalid sound value should raise ValueError."""
        with pytest.raises(ValueError):
            Sound("invalid")
