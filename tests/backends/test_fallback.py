"""Tests for fallback backend."""

from io import StringIO
from unittest.mock import patch

from beep_lite.backends.fallback_backend import FallbackBackend
from beep_lite.types import Sound


class TestFallbackBackend:
    """Test FallbackBackend."""

    def test_fallback_backend_is_always_available(self) -> None:
        """FallbackBackend should always be available."""
        backend = FallbackBackend()
        assert backend.is_available() is True

    def test_fallback_backend_outputs_bell_character(self) -> None:
        """FallbackBackend.play should output bell character."""
        backend = FallbackBackend()

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            backend.play(Sound.OK, b"ignored")
            assert mock_stderr.getvalue() == "\a"

    def test_fallback_backend_does_not_raise_on_error(self) -> None:
        """FallbackBackend.play should not raise on errors."""
        backend = FallbackBackend()

        # Mock stderr to raise an exception
        with patch("sys.stderr.write", side_effect=Exception("Test error")):
            # Should not raise
            backend.play(Sound.OK, b"data")

    def test_fallback_backend_ignores_sound_type(self) -> None:
        """FallbackBackend should produce same output for all sound types."""
        backend = FallbackBackend()

        outputs = []
        for sound in Sound:
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                backend.play(sound, b"data")
                outputs.append(mock_stderr.getvalue())

        # All outputs should be the same (bell character)
        assert all(output == "\a" for output in outputs)
