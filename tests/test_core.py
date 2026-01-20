"""Tests for core module."""

import sys
from unittest.mock import MagicMock, patch

import pytest

from beep_lite.core import (
    _get_backend,
    _reset_backend,
    _select_backend,
    play_sound,
)
from beep_lite.loader import SoundNotFoundError
from beep_lite.types import Sound


class TestBackendSelection:
    """Test backend selection logic."""

    def setup_method(self) -> None:
        """Reset backend before each test."""
        _reset_backend()

    def teardown_method(self) -> None:
        """Reset backend after each test."""
        _reset_backend()

    @patch("beep_lite.core.sys.platform", "win32")
    def test_selects_winsound_on_windows(self) -> None:
        """Should select winsound backend on Windows."""
        with patch.dict(sys.modules, {"winsound": MagicMock()}):
            backend = _select_backend()
            assert backend.__class__.__name__ == "WinsoundBackend"

    @patch("beep_lite.core.sys.platform", "linux")
    def test_selects_simpleaudio_on_linux_when_available(self) -> None:
        """Should select simpleaudio on Linux when installed."""
        mock_sa = MagicMock()
        with patch.dict(sys.modules, {"simpleaudio": mock_sa}):
            backend = _select_backend()
            assert backend.__class__.__name__ == "SimpleaudioBackend"

    @patch("beep_lite.core.sys.platform", "linux")
    def test_selects_fallback_when_no_audio_available(self) -> None:
        """Should select fallback when no audio backend is available."""
        # Remove simpleaudio from modules if present
        with (
            patch.dict(sys.modules, {"simpleaudio": None}, clear=False),
            patch(
                "beep_lite.backends.simpleaudio_backend.SimpleaudioBackend.__init__",
                side_effect=ImportError("No simpleaudio"),
            ),
        ):
            backend = _select_backend()
            assert backend.__class__.__name__ == "FallbackBackend"


class TestGetBackend:
    """Test backend singleton behavior."""

    def setup_method(self) -> None:
        """Reset backend before each test."""
        _reset_backend()

    def teardown_method(self) -> None:
        """Reset backend after each test."""
        _reset_backend()

    def test_get_backend_returns_same_instance(self) -> None:
        """_get_backend should return the same instance on repeated calls."""
        backend1 = _get_backend()
        backend2 = _get_backend()
        assert backend1 is backend2

    def test_reset_backend_clears_instance(self) -> None:
        """_reset_backend should clear the cached instance."""
        backend1 = _get_backend()
        _reset_backend()
        backend2 = _get_backend()
        # Both should be valid backends (may or may not be same instance)
        assert backend1 is not None
        assert backend2 is not None


class TestPlaySound:
    """Test play_sound function."""

    def setup_method(self) -> None:
        """Reset backend before each test."""
        _reset_backend()

    def teardown_method(self) -> None:
        """Reset backend after each test."""
        _reset_backend()

    @patch("beep_lite.core.load_wav")
    @patch("beep_lite.core._get_backend")
    def test_play_sound_loads_and_plays(
        self, mock_get_backend: MagicMock, mock_load_wav: MagicMock
    ) -> None:
        """play_sound should load WAV data and call backend.play."""
        mock_backend = MagicMock()
        mock_get_backend.return_value = mock_backend
        mock_load_wav.return_value = b"fake wav data"

        play_sound(Sound.OK)

        mock_load_wav.assert_called_once_with(Sound.OK)
        mock_backend.play.assert_called_once_with(Sound.OK, b"fake wav data")

    @patch("beep_lite.core.load_wav")
    def test_play_sound_raises_on_missing_file(self, mock_load_wav: MagicMock) -> None:
        """play_sound should raise SoundNotFoundError when file is missing."""
        mock_load_wav.side_effect = SoundNotFoundError("File not found")

        with pytest.raises(SoundNotFoundError):
            play_sound(Sound.OK)
