"""Tests for simpleaudio backend."""

from unittest.mock import MagicMock, patch

import pytest


class TestSimpleaudioBackend:
    """Test SimpleaudioBackend."""

    def test_simpleaudio_backend_raises_when_not_installed(self) -> None:
        """SimpleaudioBackend should raise ImportError when not installed."""
        with (
            patch.dict("sys.modules", {"simpleaudio": None}),
            pytest.raises(ImportError, match="simpleaudio is not installed"),
        ):
            # Force reimport
            import importlib

            import beep_lite.backends.simpleaudio_backend as sa_module

            importlib.reload(sa_module)
            sa_module.SimpleaudioBackend()

    @patch("beep_lite.backends.simpleaudio_backend.simpleaudio", create=True)
    def test_simpleaudio_backend_initializes_when_installed(
        self, mock_sa: MagicMock
    ) -> None:
        """SimpleaudioBackend should initialize when simpleaudio is installed."""
        with patch.dict("sys.modules", {"simpleaudio": mock_sa}):
            from beep_lite.backends.simpleaudio_backend import SimpleaudioBackend

            backend = SimpleaudioBackend()
            assert backend is not None

    @patch("beep_lite.backends.simpleaudio_backend.simpleaudio", create=True)
    def test_simpleaudio_backend_is_available(self, mock_sa: MagicMock) -> None:
        """SimpleaudioBackend.is_available should return True when installed."""
        with patch.dict("sys.modules", {"simpleaudio": mock_sa}):
            from beep_lite.backends.simpleaudio_backend import SimpleaudioBackend

            backend = SimpleaudioBackend()
            assert backend.is_available() is True


class TestBytesIOWrapper:
    """Test _BytesIOWrapper helper class."""

    def test_bytes_io_wrapper_read(self) -> None:
        """_BytesIOWrapper should support read operations."""
        from beep_lite.backends.simpleaudio_backend import _BytesIOWrapper

        wrapper = _BytesIOWrapper(b"hello world")

        assert wrapper.read(5) == b"hello"
        assert wrapper.read(1) == b" "
        assert wrapper.read() == b"world"

    def test_bytes_io_wrapper_seek_and_tell(self) -> None:
        """_BytesIOWrapper should support seek and tell operations."""
        from beep_lite.backends.simpleaudio_backend import _BytesIOWrapper

        wrapper = _BytesIOWrapper(b"hello world")

        assert wrapper.tell() == 0
        wrapper.seek(6)
        assert wrapper.tell() == 6
        assert wrapper.read(5) == b"world"

    def test_bytes_io_wrapper_seek_whence(self) -> None:
        """_BytesIOWrapper should support different whence values."""
        from beep_lite.backends.simpleaudio_backend import _BytesIOWrapper

        wrapper = _BytesIOWrapper(b"hello world")

        # SEEK_SET (0)
        wrapper.seek(5, 0)
        assert wrapper.tell() == 5

        # SEEK_CUR (1)
        wrapper.seek(2, 1)
        assert wrapper.tell() == 7

        # SEEK_END (2)
        wrapper.seek(-3, 2)
        assert wrapper.tell() == 8
