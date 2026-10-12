# 小さな紹介・操作テストサイト

キャラクター紹介と、あいさつ回数・定型メッセージを試す静的サイトです。通信するAI機能、バックエンド、入力フォーム、データ保存はありません。

## 実行

`python3 -m http.server 8000` を実行し、`http://localhost:8000` を開きます。ビルド・追加依存関係は不要です。既存のGitHub Pagesがmainのルートから自動公開します。

## 検査

作業開始時のSHAを使い、`python3 .github/mandatory.py --base <SHA> --fix` と、同じ引数の通常検査を実行します。

ブラウザ検査: Python PlaywrightとChromiumがある環境で `python3 tests/browser.py http://localhost:8000`。`CHROMIUM_PATH` でブラウザ実行ファイル、`SCREENSHOT_DIR` でスクリーンショットの出力先を指定できます。Desktop・iPhone相当のviewport、連続操作、reset、再読み込み、keyboard、motion軽減、JavaScript無効時を検査します。実機Safariの検査とは区別してください。
