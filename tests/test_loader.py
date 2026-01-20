"""Tests for WAV loader."""

from unittest.mock import MagicMock, patch

import pytest

from beep_lite.loader import (
    SoundNotFoundError,
    clear_cache,
    load_wav,
    preload_all,
)
from beep_lite.types import Sound


class TestLoadWav:
    """Test load_wav function."""

    def setup_method(self) -> None:
        """Clear cache before each test."""
        clear_cache()

    def teardown_method(self) -> None:
        """Clear cache after each test."""
        clear_cache()

    @patch("beep_lite.loader.resources.files")
    def test_load_wav_returns_bytes(self, mock_files: MagicMock) -> None:
        """load_wav should return bytes."""
        mock_asset = MagicMock()
        mock_asset.read_bytes.return_value = b"RIFF....WAVEfmt "
        mock_files.return_value.__truediv__.return_value.__truediv__.return_value = (
            mock_asset
        )

        result = load_wav(Sound.OK)

        assert isinstance(result, bytes)
        assert result == b"RIFF....WAVEfmt "

    @patch("beep_lite.loader.resources.files")
    def test_load_wav_uses_correct_filename(self, mock_files: MagicMock) -> None:
        """load_wav should use the correct filename based on Sound enum."""
        mock_assets = MagicMock()
        mock_files.return_value.__truediv__.return_value = mock_assets
        mock_file = MagicMock()
        mock_file.read_bytes.return_value = b"data"
        mock_assets.__truediv__.return_value = mock_file

        load_wav(Sound.SCAN_OK)

        mock_assets.__truediv__.assert_called_with("scan_ok.wav")

    @patch("beep_lite.loader.resources.files")
    def test_load_wav_raises_sound_not_found_error(self, mock_files: MagicMock) -> None:
        """load_wav should raise SoundNotFoundError when file is missing."""
        mock_assets = mock_files.return_value.__truediv__.return_value
        mock_file = mock_assets.__truediv__.return_value
        mock_file.read_bytes.side_effect = FileNotFoundError("File not found")

        with pytest.raises(SoundNotFoundError):
            load_wav(Sound.OK)

    @patch("beep_lite.loader.resources.files")
    def test_load_wav_caches_result(self, mock_files: MagicMock) -> None:
        """load_wav should cache results."""
        mock_asset = MagicMock()
        mock_asset.read_bytes.return_value = b"data"
        mock_files.return_value.__truediv__.return_value.__truediv__.return_value = (
            mock_asset
        )

        # Call twice
        load_wav(Sound.OK)
        load_wav(Sound.OK)

        # read_bytes should only be called once due to caching
        assert mock_asset.read_bytes.call_count == 1


class TestClearCache:
    """Test clear_cache function."""

    @patch("beep_lite.loader.resources.files")
    def test_clear_cache_clears_cached_data(self, mock_files: MagicMock) -> None:
        """clear_cache should clear the cache."""
        mock_asset = MagicMock()
        mock_asset.read_bytes.return_value = b"data"
        mock_files.return_value.__truediv__.return_value.__truediv__.return_value = (
            mock_asset
        )

        # Load and cache
        load_wav(Sound.OK)

        # Clear cache
        clear_cache()

        # Load again - should call read_bytes again
        load_wav(Sound.OK)

        assert mock_asset.read_bytes.call_count == 2


class TestPreloadAll:
    """Test preload_all function."""

    @patch("beep_lite.loader.load_wav")
    def test_preload_all_loads_all_sounds(self, mock_load_wav: MagicMock) -> None:
        """preload_all should attempt to load all sounds."""
        preload_all()

        # Should be called once for each Sound enum value
        assert mock_load_wav.call_count == len(Sound)

    @patch("beep_lite.loader.load_wav")
    def test_preload_all_does_not_raise_on_error(
        self, mock_load_wav: MagicMock
    ) -> None:
        """preload_all should not raise even if loading fails."""
        mock_load_wav.side_effect = SoundNotFoundError("File not found")

        # Should not raise
        preload_all()
