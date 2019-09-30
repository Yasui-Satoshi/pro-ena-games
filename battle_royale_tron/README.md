# Battle_royale_tron
トロンゲーム
![Ena_Ken_Games](https://user-images.githubusercontent.com/39481709/65900245-82f10300-e3f0-11e9-9081-f09b8acbee25.jpg)
## ルール
このゲームは４人のアルゴリズムを競わせるゲームです  
壁、またはプレイヤーの通ったマスに入ってしまうと脱落です  
脱落したプレイヤーの描いたマスは勝敗が決まるまで残ります  
生存者が１になると、生存プレイヤーに１点が入ります  
３点先取したプレイヤーが、ゲームの勝者です  
## 設定
||||
|:---|:---|:---|
|プレイヤーサイズ| 20×20 | P |
|マップサイズ| 700×700 | w,h |
|1Pのアルゴリズム|momotaro.py|mom.turn|
|2Pのアルゴリズム|kintaro.py|kin.turn|
|3Pのアルゴリズム|urashima.py|ura.turn|
|4Pのアルゴリズム|yasha.py|yas.turn|

## 実行環境
ubuntu16.04LTS  
python3系  
numpy  
pygame  

### numpyのインストール
`$ pip install numpy`
### pygameのインストール
`$ pip install pygame`

## 各プログラムの説明
- battle_royale.py  
対戦に使用するプログラムです  
`$ python3 battle_royale.py`でゲームが起動します  
編集可の部分以外はできるだけ変更しないでください  
- momotaro.py  
1Pのアルゴリズムを記述するプログラムです  
デフォルトでは前方に壁があると右に進路を変えるアルゴリズムが組んであります  
- kintaro.py  
2Pのアルゴリズムを記述するプログラムです  
デフォルトでは前方に壁があると右に進路を変えるアルゴリズムが組んであります  
- urashima.py  
3Pのアルゴリズムを記述するプログラムです  
デフォルトでは前方に壁があると右に進路を変えるアルゴリズムが組んであります  
- momotaro.py  
4Pのアルゴリズムを記述するプログラムです  
デフォルトでは前方に壁があると"左"に進路を変えるアルゴリズムが組んであります  
 

