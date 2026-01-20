"""Tests for winsound backend."""

import sys
from unittest.mock import patch

import pytest

from beep_lite.types import Sound


class TestWinsoundBackend:
    """Test WinsoundBackend."""

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
    def test_winsound_backend_initializes_on_windows(self) -> None:
        """WinsoundBackend should initialize successfully on Windows."""
        from beep_lite.backends.winsound_backend import WinsoundBackend

        backend = WinsoundBackend()
        assert backend.is_available() is True

    @patch("beep_lite.backends.winsound_backend.sys.platform", "linux")
    def test_winsound_backend_raises_on_non_windows(self) -> None:
        """WinsoundBackend should raise ImportError on non-Windows."""
        # We need to reload the module with patched platform
        with pytest.raises(ImportError, match="only available on Windows"):
            from beep_lite.backends.winsound_backend import WinsoundBackend

            WinsoundBackend()

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
    def test_winsound_backend_play_does_not_raise(self) -> None:
        """WinsoundBackend.play should not raise on errors."""
        from beep_lite.backends.winsound_backend import WinsoundBackend

        backend = WinsoundBackend()

        # Play with invalid data - should not raise
        backend.play(Sound.OK, b"invalid wav data")
