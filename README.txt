データ分析に関するプログラミング（JupyterNnotebook上のPythonコード）の一部をpdf形式で掲載


01resampling1sec.pdf
視線データについて、約1/60秒間隔を1秒間隔の整った時系列に変換

counting.pdf
視線データについて、座標系の範囲ごとにデータを確認
マウスキーボード入力について、クリック（タップ）回数、キー種別ごとのタップ回数を確認

CreateNewLabels.pdf
機械学習向けの特徴量データを作成
関数の呼び出し記録を基に、各関数がある引数で呼び出された回数をそれぞれカウント

experiment.py
提出作品。以下experiment.pyで収集されるデータの一例
｜ーsample_ex.csv       :視線データ
｜ーsample_ex_click.csv :マウス入力データ
｜ーsample_ex_key.csv   :キーボード入力データ