#https://github.com/stanley-godfrey/Tron-pg
'''
    4-player tron battle
“The strong one doesn't win, the one that wins is strong.”
                                            (Franz Anton Beckenbauer)
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pymodule import momotaro,kintaro,urashima,yasha #player's algorithm
from colors import pycolor
import pygame as pg            
import time
import random as rd
import numpy as np
import os
pg.init()                          # pygame起動
BLACK    = (0  ,0  ,0  )           # ウインドウカラー(black)
WHITE    = (255,255,255)           # 死亡色
P1_COLOR = (255,0  ,255)           # プレイヤーカラー１(C)
P2_COLOR = (0  ,255,255)           # プレイヤーカラー２(M)
P3_COLOR = (255,255,0  )           # プレイヤーカラー３(Y)
P4_COLOR = (0  ,255,0  )           # プレイヤーカラー４(G)
MUSIC    = './music/bgm.mp3'       # ステージ音楽(Kinkin作曲予定)
#------------------------------------------------------------------------------------------------#
class Player:                      #プレイヤー設定
    def __init__(self, coordinate, direction, color,num):
        """
        init method for class
        """
        self.coordinate = coordinate                     #プレイヤー座標[x,y]
        self.x         = self.coordinate[0]                  # プレイヤー座標　x
        self.y         = self.coordinate[1]                  # プレイヤー座標　y

        self.point     = [(self.x/P)-1 , (self.y/P)-1]  # バトルフィールドプレイヤー座標(x,y)
        self.direction = direction                      # プレイヤー進行方向[x,y]
        self.color     = color                          # プレイヤー色
        self.num       = num                            # プレイヤー番号
        self.rect      = pg.Rect(self.x,self.y,P,P) # プレイヤーオブジェクト(left,top,width,height)
    
    def __draw__(self):                 # 軌跡設定
        """
        method for drawing player
        """
        self.rect      = pg.Rect(self.x,self.y,P,P)  # プレイヤーオブジェクト
        pg.draw.rect(screen, self.color, self.rect, 1)        # プレイヤーのマスを塗る

    def __move__(self):                 # 移動設定
        """
        method for moving the player
        """
        self.x += self.direction[0]     #X軸方向
        self.y += self.direction[1]     #Y軸方向

def new_game():                         # New_Game
    new_p1 = Player(p_coordinate[0] , p_direction[0] , P1_COLOR,1)  # player1
    new_p2 = Player(p_coordinate[1] , p_direction[0] , P2_COLOR,2)  # player2
    new_p3 = Player(p_coordinate[2] , p_direction[0] , P3_COLOR,3)  # player3
    new_p4 = Player(p_coordinate[3] , p_direction[0] , P4_COLOR,4)  # player4    
    return new_p1, new_p2, new_p3, new_p4

def create_field():
    battle_field            = np.full([b_w,b_h],-1)
    battle_field[2:20,2:20] = 0
    #print(*battle_field, sep='\n')
    print(battle_field[2][2])
    return battle_field
    '''
           0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 
           ----------------------------------------------------------------
    A,0  |-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1|
    B,1  |-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1|
    C,2  |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    D,3  |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    E,4  |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    F,5  |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    G,6  |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    H,7  |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    I,8  |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    J,9  |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    K,10 |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    L,11 |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    M,12 |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    N,13 |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    O,14 |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    P,15 |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    Q,16 |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    R,17 |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    S,18 |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    T,19 |-1 -1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 -1 -1|
    U,20 |-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1|
    V,21 |-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1|
           ----------------------------------------------------------------
           0:None , -1:Wall , 1:P1_Cell , 2:P2_Cell , 3:P3_Cell , 4:P4_Cell
    '''
#------------------------------------------------------------------------------------------------#
#-------------------ゲーム設定-------------------------------------------------------------------#
P                  = 20                                # プレイヤーサイズ #only even num
window_w, window_h = 480, 540                          # ウインドウサイズ #480*560
offset             = window_h - window_w               # エリア外余白     #60
w,h                = window_w, window_h-offset         # エリア           #480*480
b_w,b_h            = window_w//P ,(window_h-offset)//P # マスエリア       #24*24
print('width = '+str(w)+'height = '+str(h))
battle_field  = create_field()

screen        = pg.display.set_mode((window_w, window_h)) # ウインドウ生成
pg.display.set_caption("帰ってきた \
     ！第一回！陣取りゲーム！RETURNS(Take2)")          # ゲームタイトル
font          = pg.font.Font(None, 72)                    # 文字サイズ
clock         = pg.time.Clock()                           # used to regulate FPS
check_time    = time.time()                               # used to check collisions with rects

start_c       = np.array(range(4*P, w - 4*P, P))          # 開始座標
start_d       = [[P, 0], [-P, 0], [0, P], [0, -P]]        # 開始方向 [→, ←, ↓, ↑]
p_coordinate  = [rd.choice(start_c),rd.choice(start_c)]
p_direction   = [rd.choice(start_d)]

p_score       = [0, 0, 0, 0]                              # プレイヤースコア(勝利数)[p1,p2,p3,p4]
dead          = [True, True, True, True]                  # 死んだプレイヤーの情報　[True:生存,False:死亡]
dead_cnt      = np.sum(dead)                              # 生存プレイヤー数

p1 = Player(p_coordinate , p_direction[0] , P1_COLOR,1)  # player1
p2 = Player(p_coordinate[1] , p_direction[0] , P2_COLOR,2)  # player2
p3 = Player(p_coordinate[2] , p_direction[0] , P3_COLOR,3)  # player3
p4 = Player(p_coordinate[3] , p_direction[0] , P4_COLOR,4)  # player4

objects   = list([ p1          , p2          , p3          , p4          ]) # プレイヤー情報
all_cell  = list([(p1.rect,'1'),(p2.rect,'2'),(p3.rect,'3'),(p4.rect,'4')]) # セル情報(プレイヤー番号あり)
wall_cell = list([ p1.rect     , p2.rect     , p3.rect     , p4.rect     ]) # セル情報(プレイヤー番号なし)
wall_cell = list([ p1.rect     , p2.rect     , p3.rect     , p4.rect     ]) # セル情報(プレイヤー番号なし)
momotaro_cell, kintaro_cell = list(p1.rect), list(p2.rect)                  # 単体パス
urashima_cell, yasha_cell   = list(p3.rect), list(p4.rect)
wall      = list([pg.Rect(0,0,2*P,h) , pg.Rect(0,0,w,2*P) ,\
           pg.Rect(w-2*P,0,2*P,h) , pg.Rect(0,h-2*P,w,2*P)])                # 外壁情報 600*600

momotaro.momotaro()
kintaro.kintaro()
urashima.urashima()
yasha.yasha()
pg.mixer.music.load(MUSIC) #音源
pg.mixer.music.play(-1)

#-------------------------------------------------------------------------------------------------#
done = True             #スイッチ
new  = True

while  done:                             #done = True の間
    screen.fill(BLACK)                          # 背景書き込み
    for i in wall: pg.draw.rect(screen, (100, 100, 100), i, 0)# 壁書き込み
    
    for o in objects: #プレイヤーの行動結果
        if not dead[o.num-1]: #死亡済みプレイヤーはスキップ
            continue
        #衝突判定------------------------------------------------------------------------------      
        '''
        print('all_cell')
        print(*all_cell, sep='\n')
        print('--------------------------')
        print('wall_cell')
        print(*wall_cell , sep='\n')
        print('--------------------------')
        '''
        #if (o.rect,'1') in all_cell or (o.rect,'2') in all_cell or (o.rect,'3') in all_cell \
        #  or (o.rect,'4') in all_cell or o.rect.collidelist(wall) != -1:
        #if o.rect.collidelist(wall_cell) > -1 or o.rect.collidelist(wall) > -1 :
        #if o.rect.collidelist(wall) > -1 : #壁にぶつかると死亡(プレイヤーマスは死なない)
        if battle_field[0][0] != 0 :
            if (time.time() - check_time) >= 0.1:
                check_time       = time.time()
                dead[o.num-1] = False
                dead_cnt         = np.sum(dead)
                o.color         = WHITE
                o.direction        = [0,0]
                print("player" + str(o.num)+ " is dead!!")
                print(dead)
                print("Survivor: " + str(dead_cnt) )
                print('--------------------------')
                
                if dead_cnt <= 1:
                    if     dead[0]: 
                            print("prayer 1 gets one point!")
                            p_score[0] += 1
                    elif   dead[1]: 
                            print("prayer 2 gets one point!")
                            p_score[1] += 1
                    elif   dead[2]: 
                            print("prayer 3 gets one point!")
                            p_score[2] += 1
                    elif   dead[3]: 
                            print("prayer 4 gets one point!")
                            p_score[3] += 1
                    
                    elif   dead_cnt == 0:
                        pass
                    
                    new          = False
                    new_p1, new_p2, new_p3, new_p4 = new_game()
                    objects      = [new_p1 , new_p2 , new_p3 , new_p4]
                    all_cell     = [(p1.rect,'1'), (p2.rect,'2'),(p3.rect,'3'),(p4.rect,'4')]
                    wall_cell    = [ p1.rect     , p2.rect      , p3.rect     , p4.rect     ]
                    dead       = [True, True, True, True] 
                    print("##########################")
                    pg.time.delay(1000)
                    break

            #pg.display.update()
        
        else:  # 衝突してない時
            wall_cell.append(o.rect)
            if   o.color == P1_COLOR: 
                all_cell.append((o.rect,'1')) 
                momotaro_cell.append(o.rect)
            elif o.color == P2_COLOR: 
                all_cell.append((o.rect,'2'))
                kintaro_cell.append(o.rect)
            elif o.color == P3_COLOR: 
                all_cell.append((o.rect,'3'))
                urashima_cell.append(o.rect)
            elif o.color == P4_COLOR: 
                all_cell.append((o.rect,'4'))
                yasha_cell.append(o.rect)

        o.__draw__()
        o.__move__()
        pg.time.delay(100)
    #--------------------------------------------------------------------------------------#
    
    for r in all_cell:
        if new is False:  # empties the all_cell - needs to be here to prevent graphical glitches
            all_cell = []
            new = True
            break
        if   r[1] == '1': pg.draw.rect(screen, P1_COLOR, r[0], 1)
        elif r[1] == '2': pg.draw.rect(screen, P2_COLOR, r[0], 1)
        elif r[1] == '3': pg.draw.rect(screen, P3_COLOR, r[0], 1)
        elif r[1] == '4': pg.draw.rect(screen, P4_COLOR, r[0], 1)
        #pg.time.delay(20)
    
    
    # 現在のスコアを表示
    score_text = font.render('{0} : {1} : {2} : {3}'.format(p_score[0], p_score[1],p_score[2], p_score[3]), 1, (255, 153, 51))
    score_text_pos = score_text.get_rect()
    score_text_pos.centerx = int(window_w / 2)
    score_text_pos.centery = int(window_h - offset / 2)
    screen.blit(score_text, score_text_pos)

    pg.display.flip()      # flips display
    clock.tick(30)         # regulates FPS
    
    sysfont = pg.font.SysFont(None, 60,bold=True, italic=True)
    win1 = sysfont.render("player 1 WIN!!", True, P1_COLOR)
    win2 = sysfont.render("player 2 WIN!!", True, P2_COLOR)
    win3 = sysfont.render("player 3 WIN!!", True, P3_COLOR)
    win4 = sysfont.render("player 4 WIN!!", True, P4_COLOR)
    #3勝で勝利
    if   p_score[0] == 3:
        print("player 1 WIN!!")
        screen.blit(win1, (50,200))
    elif p_score[1] == 3:
        print("player 2 WIN!!")
        screen.blit(win2, (50,200))
    elif p_score[2] == 3:
        print("player 3 WIN!!")
        screen.blit(win3, (50,200))
    elif p_score[3] == 3:
        print("player 4 WIN!!")
        screen.blit(win4, (50,200))
    if p_score[0]==3 or p_score[1]==3 or p_score[2]==3 or p_score[3]==3 :
        done = False
    pg.display.update()

pg.time.delay(2000)
pg.quit()              # 終了

#pygame備忘録
'''
pygame.draw.rect(Surface, color, Rect, width=0): return Rect
pygame.Rect(left, top, width, height): return Rect
pygame.Rect.collidelist(list): return index
'''
