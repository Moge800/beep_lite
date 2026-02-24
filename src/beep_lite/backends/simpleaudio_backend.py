"""Simpleaudio backend implementation."""

import io
import logging
import threading
import wave

from ..types import Sound

logger = logging.getLogger(__name__)


class SimpleaudioBackend:
    """Backend using simpleaudio library.

    This backend works on Windows, macOS, and Linux.
    Requires simpleaudio to be installed: pip install simpleaudio
    """

    def __init__(self) -> None:
        """Initialize the simpleaudio backend."""
        try:
            import simpleaudio  # type: ignore[import-not-found]

            self._simpleaudio = simpleaudio
        except ImportError as e:
            raise ImportError(
                "simpleaudio is not installed. "
                "Install it with: pip install simpleaudio"
            ) from e

    def play(self, sound: Sound, data: bytes) -> None:
        """Play a sound asynchronously using simpleaudio.

        Args:
            sound: The sound type to play.
            data: The WAV file data as bytes.
        """

        def _play_thread() -> None:
            try:
                with wave.open(io.BytesIO(data), "rb") as wav_reader:
                    wave_obj = self._simpleaudio.WaveObject.from_wave_read(wav_reader)
                    wave_obj.play()
            except Exception as e:
                logger.warning(f"simpleaudio playback failed for {sound.value}: {e}")

        # Play in a separate thread to avoid blocking
        thread = threading.Thread(target=_play_thread, daemon=True)
        thread.start()

    def is_available(self) -> bool:
        """Check if simpleaudio is available.

        Returns:
            True if simpleaudio is installed, False otherwise.
        """
        try:
            import simpleaudio  # type: ignore[import-not-found]  # noqa: F401

            return True
        except ImportError:
            return False
