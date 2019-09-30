#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#https://github.com/stanley-godfrey/Tron-pg
'''
    4-player tron battle
“The strong one doesn't win, the one that wins is strong.”
                                            (Franz Anton Beckenbauer)
'''
from pymodule import momotaro,kintaro,urashima,yasha    #player's algorithm
from colors import pycolor
import pygame as pg            
import time
import random as rd
import numpy as np
import os
pg.init()                                               # pygame初期化
BLACK     = (0  , 0  , 0  )                             # ウインドウカラー(black)
WHITE     = (255, 255, 255)                             # 死亡色
P1_COLOR  = (255, 0  , 255)                              # プレイヤーカラー１(M)
P2_COLOR  = (255, 255, 0  )                              # プレイヤーカラー２(Y)
P3_COLOR  = (0  , 255, 255)                              # プレイヤーカラー３(C)
P4_COLOR  = (0  , 255, 0  )                              # プレイヤーカラー４(G)
MUSIC     = './music/steamboat_willie.mp3'              # ステージ音楽(Kinkin作曲予定)
P         = 20                                          # プレイヤーサイズ #only even number
win_w, win_h = 440, 500                            # ウインドウサイズ
offset       = win_h - win_w                       # エリア外余白 #60
w, h         = win_w , win_h-offset                # バトルエリア
screen       = pg.display.set_mode((win_w, win_h)) # ウインドウ生成
pg.display.set_caption('帰ってきた \
    ！第一回！陣取りゲーム！RETURNS(Take2)')       # ゲームタイトル
pg.mixer.music.load(MUSIC)                         # 音源ロード
pg.mixer.music.play(-1)                            # 音源ループ再生
SET           = 3                                    # 勝利に必要なセット数

#------------------------------------------------------------------------------------------------#
class Player:               #プレイヤー設定
    def __init__(self, x, y, direction, color,number):
        self.x       = x                                # プレイヤー座標　X
        self.y       = y                                # プレイヤー座標　Y
        self.bearing = direction                        # プレイヤー進行方向[x,y]
        self.color   = color                            # プレイヤー色
        self.number  = number                           # プレイヤー番号
        self.rect    = pg.Rect(self.x, self.y, P, P)    # プレイヤーオブジェクト(left,top,width,height)
    
    def __draw__(self):     # マス塗りメソッド
        self.rect    = pg.Rect(self.x, self.y, P, P)    # プレイヤーオブジェクト
        pg.draw.rect(screen, self.color, self.rect, 1)  # プレイヤーのマスを塗る
    
    def __move__(self):     # マス移動メソッド
        self.x      += self.bearing[0]                  #X軸方向
        self.y      += self.bearing[1]                  #Y軸方向

def new_game():             # New_Gameメソッド
    if     dead[0]:
        print('prayer 1 gets one point!')
        p_score[0] += 1
    elif   dead[1]: 
        print('prayer 2 gets one point!')
        p_score[1] += 1
    elif   dead[2]: 
        print('prayer 3 gets one point!')
        p_score[2] += 1
    elif   dead[3]: 
        print('prayer 4 gets one point!')
        p_score[3] += 1
    new_p1   = Player(rd.choice(start_c), rd.choice(start_c), rd.choice(start_d), P1_COLOR, 1)  # player1
    new_p2   = Player(rd.choice(start_c), rd.choice(start_c), rd.choice(start_d), P2_COLOR, 2)  # player2
    new_p3   = Player(rd.choice(start_c), rd.choice(start_c), rd.choice(start_d), P3_COLOR, 3)  # player3
    new_p4   = Player(rd.choice(start_c), rd.choice(start_c), rd.choice(start_d), P4_COLOR, 4)  # player4
    return new_p1, new_p2, new_p3, new_p4
#-------------------ゲーム設定---------------------------------------------------------------------------#

def main(): 
    clock        = pg.time.Clock()                      # used to regulate FPS
    check_time   = time.time()                          # used to check collisions with rects
    start_c      = np.array(range(2*P, w-2*P, P))       # 開始座標リスト[40, 60, ...,360,380]
    start_d      = [(0, -P), (-P, 0), (P, 0), (0, P)]   # 開始方向 [↑, ←, →, ↓]
    dead         = [True, True, True, True]             # 死んだプレイヤーの情報　[True:生存, False:死亡]
    survivor     = np.sum(dead)                         # 生存プレイヤー数
    p_score      = [0, 0, 0, 0]                         # プレイヤースコア(勝利数)[p1, p2, p3, p4]

    p1 = Player(rd.choice(start_c), rd.choice(start_c) ,rd.choice(start_d), P1_COLOR, 1)  # player1 (x, y, directtion, color, number)
    p2 = Player(rd.choice(start_c), rd.choice(start_c) ,rd.choice(start_d), P2_COLOR, 2)  # player2
    p3 = Player(rd.choice(start_c), rd.choice(start_c) ,rd.choice(start_d), P3_COLOR, 3)  # player3
    p4 = Player(rd.choice(start_c), rd.choice(start_c) ,rd.choice(start_d), P4_COLOR, 4)  # player4

    objects     = list([p1, p2, p3, p4])               # プレイヤー情報
    all_cell    = list()                               # セル情報
    wall        = list([pg.Rect(0,0,P,h), pg.Rect(0,0,w,P), pg.Rect(w-P,0,P,h), pg.Rect(0,h-P,w,P)]) # 外壁情報     
    momotaro.momotaro()                                # プレイヤー1のアルゴリズム
    kintaro.kintaro()                                  # プレイヤー2のアルゴリズム
    urashima.urashima()                                # プレイヤー3のアルゴリズム
    yasha.yasha()                                      # プレイヤー4のアルゴリズム

    done = True 
    new  = True
    #------------------------------------------------------------------------------------------#
    while  done:
        screen.fill(BLACK)                                          # 背景書き込み
        for i in wall: pg.draw.rect(screen, (100, 100, 100), i, 0)  # 壁書き込み
        for o in objects: #プレイヤーの行動結果
            if not dead[o.number-1]: continue                       #死亡済みプレイヤーはスキップ    
            o.__draw__()  # 現在位置描画
            # アルゴリズム記述-----------------------------------------------------------------#

            #----------------------------------------------------------------------------------#
            o.__move__()  # １ターン移動
            #衝突判定--------------------------------------------------------------------------#      
            if (o.rect,'1') in all_cell or (o.rect,'2') in all_cell or (o.rect,'3') in all_cell \
                 or (o.rect,'4') in all_cell or o.rect.collidelist(wall) != -1:   # 衝突した時
                if (time.time() - check_time) >= 0.1:
                    check_time        = time.time()
                    dead[o.number-1]  = False                                     # 死亡に変更
                    survivor          = np.sum(dead)                              # 生存者の合計
                    print('player' + str(o.number)+ ' is dead!!')
                    print(dead)
                    print('Survivor: ' + str(survivor))
                    print('-----------------------------------')
                    if survivor == 1:
                        for r in all_cell:
                            if   dead[0]: pg.draw.rect(screen, P1_COLOR, r[0], 0) # すべての色を勝利プレイヤーの色に染める
                            elif dead[1]: pg.draw.rect(screen, P2_COLOR, r[0], 0)
                            elif dead[2]: pg.draw.rect(screen, P3_COLOR, r[0], 0)
                            elif dead[3]: pg.draw.rect(screen, P4_COLOR, r[0], 0)
                        pg.time.delay(500)
                        new           = False
                        new_p1, new_p2, new_p3, new_p4 = new_game()
                        objects       = list([new_p1, new_p2, new_p3, new_p4])
                        all_cell      = list([(p1.rect,'1'), (p2.rect,'2'), (p3.rect,'3'), (p4.rect,'4')])
                        dead          = [True, True, True, True] 
                        print('===================================')  
            else:                                                               # 衝突してない時
                if   o.color == P1_COLOR: all_cell.append((o.rect,'1'))         # all_cellにセル情報を追加する 
                elif o.color == P2_COLOR: all_cell.append((o.rect,'2'))
                elif o.color == P3_COLOR: all_cell.append((o.rect,'3'))
                elif o.color == P4_COLOR: all_cell.append((o.rect,'4'))
            pg.time.delay(100)
            #--------------------------------------------------------------------------------------------#
        for r in all_cell:                                                      #全セル描画
            if new is False:                                                    # new_game時にセル情報を空にする
                all_cell = []
                new = True
                break
            if   r[1] == '1': pg.draw.rect(screen, P1_COLOR, r[0], 1) if dead[0] else pg.draw.rect(screen, WHITE, r[0], 0)
            elif r[1] == '2': pg.draw.rect(screen, P2_COLOR, r[0], 1) if dead[1] else pg.draw.rect(screen, WHITE, r[0], 0)
            elif r[1] == '3': pg.draw.rect(screen, P3_COLOR, r[0], 1) if dead[2] else pg.draw.rect(screen, WHITE, r[0], 0)
            elif r[1] == '4': pg.draw.rect(screen, P4_COLOR, r[0], 1) if dead[3] else pg.draw.rect(screen, WHITE, r[0], 0)
        pg.time.delay(200)
        #------------------------------------------------------------------------------------------------#
        # 現在のスコアを表示
        score_font = pg.font.Font(None, 72) 
        score_text = score_font.render('{0} : {1} : {2} : {3}'.format(p_score[0], p_score[1],p_score[2], p_score[3]), 1, (255, 153, 51))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = int(win_w / 2)
        score_text_pos.centery = int(win_h - offset / 2)
        screen.blit(score_text, score_text_pos)
        sysfont = pg.font.SysFont(None, 60, bold = True, italic = True)
        win1 = sysfont.render('player 1 WIN!!', True, WHITE)
        win2 = sysfont.render('player 2 WIN!!', True, WHITE)
        win3 = sysfont.render('player 3 WIN!!', True, WHITE)
        win4 = sysfont.render('player 4 WIN!!', True, WHITE)
        pg.display.flip()      # flips display
        clock.tick(60)         # regulates FPS
        #3勝で勝利
        if   p_score[0] == SET:
            print('player 1 WIN!!')
            screen.blit(win1, (70, 150))
        elif p_score[1] == SET:
            print('player 2 WIN!!')
            screen.blit(win2, (70, 150))
        elif p_score[2] == SET:
            print('player 3 WIN!!')
            screen.blit(win3, (70, 150))
        elif p_score[3] == SET:
            print('player 4 WIN!!')
            screen.blit(win4, (70, 150))
        if p_score[0] == SET or p_score[1] == SET or p_score[2] == SET or p_score[3] == SET: done = False
        pg.display.update()
    #---------------------------------------------------------------------------------------------------#
    pg.time.delay(2000)
    pg.quit()              # pygame初期化解除

if __name__ == "__main__":
    main()

#pygame備忘録
'''
pygame.draw.rect(Surface, color, Rect, width=0): return Rect
pygame.Rect(left, top, width, height): return Rect
pygame.Rect.collidelist(list): return index
'''
