"""Integration tests using actual WAV files."""

import pytest

from beep_lite import (
    Sound,
    clear_cache,
    crit,
    mew,
    moo,
    ng,
    ok,
    play,
    preload_all,
    scan_ng,
    scan_ok,
    warn,
)
from beep_lite.loader import load_wav


class TestActualWavFiles:
    """Test that actual WAV files can be loaded."""

    def setup_method(self) -> None:
        """Clear cache before each test."""
        clear_cache()

    def teardown_method(self) -> None:
        """Clear cache after each test."""
        clear_cache()

    @pytest.mark.parametrize("sound", list(Sound))
    def test_all_wav_files_exist_and_load(self, sound: Sound) -> None:
        """All WAV files should exist and be loadable."""
        data = load_wav(sound)
        assert isinstance(data, bytes)
        assert len(data) > 0

    @pytest.mark.parametrize("sound", list(Sound))
    def test_wav_files_have_valid_riff_header(self, sound: Sound) -> None:
        """All WAV files should have valid RIFF header."""
        data = load_wav(sound)
        # WAV files start with "RIFF"
        assert data[:4] == b"RIFF", f"{sound.value}.wav should start with RIFF header"

    @pytest.mark.parametrize("sound", list(Sound))
    def test_wav_files_have_wave_format(self, sound: Sound) -> None:
        """All WAV files should have WAVE format marker."""
        data = load_wav(sound)
        # Bytes 8-12 should be "WAVE"
        assert (
            data[8:12] == b"WAVE"
        ), f"{sound.value}.wav should have WAVE format marker"

    def test_preload_all_succeeds(self) -> None:
        """preload_all should successfully load all sounds."""
        # Should not raise
        preload_all()

        # Verify all sounds are cached by loading again (should be instant)
        for sound in Sound:
            data = load_wav(sound)
            assert len(data) > 0


class TestActualPlayback:
    """Test actual sound playback (these tests produce sound!)."""

    @pytest.mark.parametrize(
        "func,name",
        [
            (ok, "ok"),
            (ng, "ng"),
            (warn, "warn"),
            (crit, "crit"),
            (moo, "moo"),
            (mew, "mew"),
            (scan_ok, "scan_ok"),
            (scan_ng, "scan_ng"),
        ],
    )
    def test_api_functions_do_not_raise(self, func, name: str) -> None:
        """All API functions should not raise with real WAV files."""
        # This will actually play the sound
        func()  # Should not raise

    @pytest.mark.parametrize("sound", list(Sound))
    def test_play_function_does_not_raise(self, sound: Sound) -> None:
        """play() should not raise for any sound."""
        play(sound)  # Should not raise
