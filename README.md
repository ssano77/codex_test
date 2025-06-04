# codex_test

このリポジトリにはPythonで実装した簡単なリバーシ（オセロ）ゲームが含まれています。

## 実行方法
1. [`uv`](https://github.com/astral-sh/uv) を使って依存関係を自動的にインストールする場合
   ```
   uv run reversi.py
   ```
   これにより Pygame がインストールされ、ゲームが起動します。
2. 従来の方法で実行する場合
   ```
   pip install pygame
   python3 reversi.py
   ```
   - 黒石（プレイヤー）はマウスで操作します。
   - 白石（AI）は自動で手を選択します。

ゲーム画面を閉じると終了します。
