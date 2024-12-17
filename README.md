# SDXL 用 LoRA を Modal で作るスクリプト
SDXL 用の LoRA を [Modal](https://modal.com/) で作成するためのサンプルスクリプトです。

## Modal とは
[Modal](https://modal.com/) は任意の Python のコードをクラウド上で実行するための環境です。AI や ML に親和性が高く、GPU を使用した環境が安価に使用できます。
無料プランでも毎月30ドル分のクレジットがもらえます。

料金は CPU、メモリ、GPU の使用時間に応じて課金され、A10G を一時間動かしても1ドルちょっとなので、比較的気軽に LoRA 生成ができます。

## 準備
Python 3.10 以降が必要です。

```
git clone sdxl-lora-gen-with-modal
cd sdxl-lora-gen-with-modal
python -m venv venv
venv/Script/activate
pip install -r requirements.txt
```

Modal のサイトに登録しておきます。
`python -m modal setup` を実行して初期設定をしておきます。

## 使い方
例：東北キリタンの LoRA を作る

1. 素材をダウンロードする  
[AI画像モデル用学習データ](https://zunko.jp/con_illust.html)が配布されているので、「02_LoRA学習用データ_B氏提供版_背景透過」から kiritan をダウンロード。

2. 素材の加工  
SDXL の学習に 1024 x 1024 のサイズが良いらしいので素材ファイルの画像を加工します。
`python resizer.py kiritan` でそれぞれのファイルサイズを 1024 x 1024 に修正します。

3. ベースモデルのアップロード  
LoRA 作成の元となるベースモデルを Modal にアップロードしておきます。
```
modal volume create models
modal volume put models <モデルファイル名> /
```

ここまでで基本となる準備は完了です。
4と5を満足するまで繰り返します。

4. 設定ファイルを素材フォルダに入れる  
`config.toml` と `dataset.toml` を編集し、素材フォルダ（kiritan）にコピーします。  
基本的には `pretrained_model_name_or_path = '/model/<モデルファイル名>'` のファイル名を修正します。  
他のパラメータは各種サイトを参考に設定して下さい。  
例：https://hoshikat.hatenablog.com/entry/2023/05/26/223229  
作成結果を見ながら調整してみてください。

5. トレーニングを開始する  
`modal run generate_lora.py --name kiritan` と実行すると素材ファイルのアップロードと LoRA のトレーニングが開始されます。  
状況はコンソールと、Modal のサイトから確認できます。  
問題がありそうだったら Modal の Logs から Stop Now で止めてください。
トレーニングは A10G で 30 分ぐらいかかります。  
完了すると kiritan.safetensors がローカルに作成されます。

## 後始末
結果に満足したら Modal のストレージを消しておきましょう。
```
modal volume delete inputs
modal volume delete outputs
modal volume delete models
```

## Tips
- 他のデータセットで試したい場合、オプションの `--name` の名前と素材のディレクトリ名をあわせてください
- GPU を変更したい場合は `generate_lora.py` の `GPU = "A10G"` のところを変更してください
- 設定ファイルの書き方は [sd-script](https://github.com/kohya-ss/sd-scripts) 等を参照ください
