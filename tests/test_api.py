"""Tests for public API."""

from unittest.mock import MagicMock, patch

from beep_lite import Sound, crit, mew, moo, ng, ok, play, scan_ng, scan_ok, warn


class TestApiExceptionSafety:
    """Test that all API functions are exception-safe."""

    @patch("beep_lite.api.play_sound")
    def test_ok_does_not_raise_on_error(self, mock_play: MagicMock) -> None:
        """ok() should not raise even when playback fails."""
        mock_play.side_effect = Exception("Test error")
        ok()  # Should not raise

    @patch("beep_lite.api.play_sound")
    def test_ng_does_not_raise_on_error(self, mock_play: MagicMock) -> None:
        """ng() should not raise even when playback fails."""
        mock_play.side_effect = Exception("Test error")
        ng()  # Should not raise

    @patch("beep_lite.api.play_sound")
    def test_warn_does_not_raise_on_error(self, mock_play: MagicMock) -> None:
        """warn() should not raise even when playback fails."""
        mock_play.side_effect = Exception("Test error")
        warn()  # Should not raise

    @patch("beep_lite.api.play_sound")
    def test_crit_does_not_raise_on_error(self, mock_play: MagicMock) -> None:
        """crit() should not raise even when playback fails."""
        mock_play.side_effect = Exception("Test error")
        crit()  # Should not raise

    @patch("beep_lite.api.play_sound")
    def test_moo_does_not_raise_on_error(self, mock_play: MagicMock) -> None:
        """moo() should not raise even when playback fails."""
        mock_play.side_effect = Exception("Test error")
        moo()  # Should not raise

    @patch("beep_lite.api.play_sound")
    def test_mew_does_not_raise_on_error(self, mock_play: MagicMock) -> None:
        """mew() should not raise even when playback fails."""
        mock_play.side_effect = Exception("Test error")
        mew()  # Should not raise

    @patch("beep_lite.api.play_sound")
    def test_scan_ok_does_not_raise_on_error(self, mock_play: MagicMock) -> None:
        """scan_ok() should not raise even when playback fails."""
        mock_play.side_effect = Exception("Test error")
        scan_ok()  # Should not raise

    @patch("beep_lite.api.play_sound")
    def test_scan_ng_does_not_raise_on_error(self, mock_play: MagicMock) -> None:
        """scan_ng() should not raise even when playback fails."""
        mock_play.side_effect = Exception("Test error")
        scan_ng()  # Should not raise

    @patch("beep_lite.api.play_sound")
    def test_play_does_not_raise_on_error(self, mock_play: MagicMock) -> None:
        """play() should not raise even when playback fails."""
        mock_play.side_effect = Exception("Test error")
        play(Sound.OK)  # Should not raise


class TestApiCallsCorrectSound:
    """Test that API functions call play_sound with correct Sound enum."""

    @patch("beep_lite.api.play_sound")
    def test_ok_plays_ok_sound(self, mock_play: MagicMock) -> None:
        """ok() should play Sound.OK."""
        ok()
        mock_play.assert_called_once_with(Sound.OK)

    @patch("beep_lite.api.play_sound")
    def test_ng_plays_ng_sound(self, mock_play: MagicMock) -> None:
        """ng() should play Sound.NG."""
        ng()
        mock_play.assert_called_once_with(Sound.NG)

    @patch("beep_lite.api.play_sound")
    def test_warn_plays_warn_sound(self, mock_play: MagicMock) -> None:
        """warn() should play Sound.WARN."""
        warn()
        mock_play.assert_called_once_with(Sound.WARN)

    @patch("beep_lite.api.play_sound")
    def test_crit_plays_crit_sound(self, mock_play: MagicMock) -> None:
        """crit() should play Sound.CRIT."""
        crit()
        mock_play.assert_called_once_with(Sound.CRIT)

    @patch("beep_lite.api.play_sound")
    def test_moo_plays_moo_sound(self, mock_play: MagicMock) -> None:
        """moo() should play Sound.MOO."""
        moo()
        mock_play.assert_called_once_with(Sound.MOO)

    @patch("beep_lite.api.play_sound")
    def test_mew_plays_mew_sound(self, mock_play: MagicMock) -> None:
        """mew() should play Sound.MEW."""
        mew()
        mock_play.assert_called_once_with(Sound.MEW)

    @patch("beep_lite.api.play_sound")
    def test_scan_ok_plays_scan_ok_sound(self, mock_play: MagicMock) -> None:
        """scan_ok() should play Sound.SCAN_OK."""
        scan_ok()
        mock_play.assert_called_once_with(Sound.SCAN_OK)

    @patch("beep_lite.api.play_sound")
    def test_scan_ng_plays_scan_ng_sound(self, mock_play: MagicMock) -> None:
        """scan_ng() should play Sound.SCAN_NG."""
        scan_ng()
        mock_play.assert_called_once_with(Sound.SCAN_NG)

    @patch("beep_lite.api.play_sound")
    def test_play_with_sound_enum(self, mock_play: MagicMock) -> None:
        """play() should accept Sound enum and call play_sound."""
        play(Sound.SCAN_OK)
        mock_play.assert_called_once_with(Sound.SCAN_OK)
