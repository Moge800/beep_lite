# beep-lite 🔊

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/beep-lite.svg)](https://badge.fury.io/py/beep-lite)

シンプルで使いやすいクロスプラットフォーム通知音再生ライブラリ。

Windows / macOS / Linux で同一の WAV 音源を利用し、**軽量・低依存・確実な再生**を実現します。

**[English](README.md)**

## ✨ 特徴

- **クロスプラットフォーム**: Windows / macOS / Linux 対応
- **軽量**: numpy などの重量依存なし（約 30KB）
- **例外安全**: 再生失敗してもアプリを停止させない
- **非同期再生**: UI をブロックしない
- **PyInstaller 対応**: 単体実行ファイルに同梱可能

## 📦 インストール

```bash
pip install beep-lite
```

### オプション: 高品質オーディオバックエンド

```bash
pip install beep-lite[audio]
```

## 🚀 使い方

```python
import beep_lite as beep

# 基本的な通知音
beep.ok()       # ✅ 正常完了
beep.ng()       # ❌ 異常・失敗
beep.warn()     # ⚠️ 注意喚起
beep.crit()     # 🚨 緊急・要対応

# 遊び心のある通知
beep.moo()      # 🐄 低音系
beep.mew()      # 🐱 高音系

# スキャン結果
beep.scan_ok()  # 📗 スキャン成功
beep.scan_ng()  # 📕 スキャン失敗
```

### Sound 列挙型を使う

```python
from beep_lite import play, Sound

play(Sound.OK)
play(Sound.SCAN_NG)
```

### 起動時にプリロード（オプション）

```python
from beep_lite import preload_all

# アプリ起動時に呼び出すと、初回再生のレイテンシを軽減
preload_all()
```

## 🎵 サウンド一覧

| 関数 | Sound 列挙型 | 用途 | 音の特徴 |
|------|-------------|------|----------|
| `ok()` | `Sound.OK` | 正常完了 | 明るい短音・上昇系 |
| `ng()` | `Sound.NG` | 異常・失敗 | 下降・やや長め |
| `warn()` | `Sound.WARN` | 注意喚起 | 同音2回 |
| `crit()` | `Sound.CRIT` | 緊急・要対応 | 低音3連 |
| `moo()` | `Sound.MOO` | 遊び心（低音） | 低域スイープ |
| `mew()` | `Sound.MEW` | 遊び心（高音） | 高域スイープ |
| `scan_ok()` | `Sound.SCAN_OK` | スキャン成功 | 極短で鋭い |
| `scan_ng()` | `Sound.SCAN_NG` | スキャン失敗 | 低短音 |

## 🔧 バックエンド

環境に応じて最適なバックエンドを自動選択します：

| 優先度 | バックエンド | 対応 OS | 依存 |
|--------|-------------|---------|------|
| 1 | winsound | Windows | なし（標準ライブラリ） |
| 2 | simpleaudio | 全 OS | `pip install simpleaudio` |
| 3 | terminal bell | 全 OS | なし（フォールバック） |

## 📋 要件

- Python 3.10+

### Linux / Raspberry Pi での追加要件

`[audio]` オプションで `simpleaudio` を使う場合、ALSA 開発ライブラリが必要です：

```bash
# Debian / Ubuntu / Raspberry Pi OS
sudo apt-get install libasound2-dev

# インストール
pip install beep-lite[audio]
```

> **Note**: `[audio]` なしでインストールした場合は terminal bell（`\a`）にフォールバックするため、追加パッケージは不要です。

## 🎯 ユースケース

### バーコードスキャナー

```python
def on_scan(barcode: str) -> None:
    if validate(barcode):
        beep.scan_ok()
        process(barcode)
    else:
        beep.scan_ng()
```

### 長時間処理の完了通知

```python
def heavy_task() -> None:
    try:
        # 重い処理...
        result = process_data()
        beep.ok()
    except Exception:
        beep.ng()
        raise
```

### GUI アプリでのバリデーション

```python
def on_submit() -> None:
    if not validate_form():
        beep.warn()
        show_error("入力内容を確認してください")
        return
    save_data()
    beep.ok()
```

## 🏭 PyInstaller での利用

```bash
pyinstaller --collect-data beep_lite your_app.py
```

または `.spec` ファイルで:

```python
datas=[('path/to/beep_lite/assets', 'beep_lite/assets')]
```
```

## 📄 ライセンス

MIT License

## 📬 リンク

<!-- - [PyPI](https://pypi.org/project/beep-lite/) -->
- [GitHub](https://github.com/Moge800/beep-lite)
