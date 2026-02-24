"""Tests for simpleaudio backend."""

from unittest.mock import MagicMock, patch

import pytest


class _ImmediateThread:
    """Thread stub that executes target immediately (for deterministic tests)."""

    def __init__(self, target, daemon=True):  # noqa: ANN001, FBT002
        self._target = target

    def start(self) -> None:
        self._target()


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

    @patch("beep_lite.backends.simpleaudio_backend.simpleaudio", create=True)
    def test_simpleaudio_backend_play_uses_wave_read(self, mock_sa: MagicMock) -> None:
        """play() should decode wav bytes and call from_wave_read."""
        with patch.dict("sys.modules", {"simpleaudio": mock_sa}):
            from beep_lite.backends.simpleaudio_backend import SimpleaudioBackend
            from beep_lite.types import Sound

            backend = SimpleaudioBackend()

            mock_wave_obj = MagicMock()
            backend._simpleaudio.WaveObject.from_wave_read.return_value = mock_wave_obj

            # Minimal valid WAV bytes (RIFF/WAVE header)
            wav_bytes = (
                b"RIFF"
                + (36).to_bytes(4, "little")
                + b"WAVEfmt "
                + (16).to_bytes(4, "little")
                + (1).to_bytes(2, "little")
                + (1).to_bytes(2, "little")
                + (8000).to_bytes(4, "little")
                + (16000).to_bytes(4, "little")
                + (2).to_bytes(2, "little")
                + (16).to_bytes(2, "little")
                + b"data"
                + (0).to_bytes(4, "little")
            )

            with patch(
                "beep_lite.backends.simpleaudio_backend.threading.Thread",
                _ImmediateThread,
            ):
                backend.play(Sound.OK, wav_bytes)

            backend._simpleaudio.WaveObject.from_wave_read.assert_called_once()
            mock_wave_obj.play.assert_called_once()
