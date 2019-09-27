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
pg.init()                           # pygame起動
BLACK     = (0  ,0  ,0  )           # ウインドウカラー(black)
WHITE     = (255,255,255)           # 死亡色
P1_COLOUR = (255,0  ,255)           # プレイヤーカラー１(C)
P2_COLOUR = (0  ,255,255)           # プレイヤーカラー２(M)
P3_COLOUR = (255,255,0  )           # プレイヤーカラー３(Y)
P4_COLOUR = (0  ,255,0  )           # プレイヤーカラー４(G)
#MUSIC     =   './music/bgm_maoudamashii_ethnic32.mp3'                # ステージ音楽(Kinkin作曲予定)
#------------------------------------------------------------------------------------------------#
class Player:                       #プレイヤー設定
    def __init__(self, x, y, direction, colour,num):
        """
        init method for class
        """
        self.x       = x            # プレイヤー座標　X
        self.y       = y            # プレイヤー座標　Y
        self.bearing = direction    # プレイヤー進行方向[x,y]
        self.colour  = colour       # プレイヤー色
        self.number  = num          # プレイヤー番号
        self.rect    = pg.Rect(self.x-P,self.y-P,P,P) # プレイヤーオブジェクト(left,top,width,height)
    
    def __draw__(self):             # 軌跡設定
        """
        method for drawing player
        """
        self.rect = pg.Rect(self.x-P,self.y-P,P,P)  # プレイヤーオブジェクト(2*2)
        pg.draw.rect(screen, self.colour, self.rect, 1)        # プレイヤーのマスを塗る

    def __move__(self):             # 移動設定
        """
        method for moving the player
        """
        self.x += self.bearing[0]   #X軸方向
        self.y += self.bearing[1]   #Y軸方向

def new_game():                     # New_Game
    new_p1 = Player(rd.choice(start_c),rd.choice(start_c),rd.choice(start_d), P1_COLOUR,1)  # player1
    new_p2 = Player(rd.choice(start_c),rd.choice(start_c),rd.choice(start_d), P2_COLOUR,2)  # player2
    new_p3 = Player(rd.choice(start_c),rd.choice(start_c),rd.choice(start_d), P3_COLOUR,3)  # player3
    new_p4 = Player(rd.choice(start_c),rd.choice(start_c),rd.choice(start_d), P4_COLOUR,4)  # player4
    return new_p1, new_p2, new_p3, new_p4
#------------------------------------------------------------------------------------------------#
#-------------------ゲーム設定-------------------------------------------------------------------#
P          = 20                                 # プレイヤーサイズ #only even number
window_w, window_h   = 500, 560                 # ウインドウサイズ
offset     = window_h - window_w                # エリア外余白 #60
w,h        = window_w  ,window_h-offset         # バトルエリア


screen     = pg.display.set_mode((window_w, window_h)) # ウインドウ生成
pg.display.set_caption("帰ってきた \
     ！第一回！陣取りゲーム！RETURNS(Take2)")   # ゲームタイトル
font       = pg.font.Font(None, 72)             # 文字サイズ
clock      = pg.time.Clock()                    # used to regulate FPS
check_time = time.time()                        # used to check collisions with rects
start_c    = np.array(range(4*P, w - 4*P, P))   # 開始座標
start_d    = [[P, 0], [-P, 0], [0, P], [0, -P]] # 開始方向 [→, ←, ↓, ↑]
p_score    = [0, 0, 0, 0]                       # プレイヤースコア(勝利数)[p1,p2,p3,p4]
dead       = [True, True, True, True]           # 死んだプレイヤーの情報　[True:生存,False:死亡]
dead_cnt   = np.sum(dead)                       # 生存プレイヤー数

p1 = Player(rd.choice(start_c),rd.choice(start_c),rd.choice(start_d), P1_COLOUR,1)  # player1 (x,y,directtion,color,number)
p2 = Player(rd.choice(start_c),rd.choice(start_c),rd.choice(start_d), P2_COLOUR,2)  # player2
p3 = Player(rd.choice(start_c),rd.choice(start_c),rd.choice(start_d), P3_COLOUR,3)  # player3
p4 = Player(rd.choice(start_c),rd.choice(start_c),rd.choice(start_d), P4_COLOUR,4)  # player4

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
#pg.mixer.music.load(MUSIC) #音源
#pg.mixer.music.play(-1)

#-------------------------------------------------------------------------------------------------#
done = True             #スイッチ
new  = True

while  done:                             #done = True の間
    #キーボードイベントを取得(AIのみの場合不要)----------------------------------------
    for event in pg.event.get():        # gets all event in last tick
        if   event.type == pg.QUIT:     # close button pressed
            done = False
        elif event.type == pg.KEYDOWN:  # keyboard key pressed
            # === Player 1 === #
            if   event.key == pg.K_w   : objects[0].bearing = ( 0,-P) #    [W] 
            elif event.key == pg.K_s   : objects[0].bearing = ( 0, P) # [A]   [D]   
            elif event.key == pg.K_a   : objects[0].bearing = (-P, 0) #    [S]
            elif event.key == pg.K_d   : objects[0].bearing = ( P, 0) #   [Tab]
            # === Player 2 === #
            if   event.key == pg.K_UP  : objects[1].bearing = ( 0,-P) #    [↑]
            elif event.key == pg.K_DOWN: objects[1].bearing = ( 0, P) #[←]    [→]
            elif event.key == pg.K_LEFT: objects[1].bearing = (-P, 0) #    [↓]
            # === Player 3 === #
            if   event.key == pg.K_t   : objects[2].bearing = ( 0,-P) #    [T]
            elif event.key == pg.K_g   : objects[2].bearing = ( 0, P) # [F]   [H]
            elif event.key == pg.K_f   : objects[2].bearing = (-P, 0) #    [G]
            elif event.key == pg.K_h   : objects[2].bearing = ( P, 0) #  [LShift]  
            # === Player 4 === #
            if   event.key == pg.K_i   : objects[3].bearing = ( 0,-P) #    [I]
            elif event.key == pg.K_k   : objects[3].bearing = ( 0, P) # [J]   [L]  
            elif event.key == pg.K_j   : objects[3].bearing = (-P, 0) #    [K]
            elif event.key == pg.K_l   : objects[3].bearing = ( P, 0) #  [Space]
    #--------------------------------------------------------------------------------------
    screen.fill(BLACK)                          # 背景書き込み
    for i in wall: pg.draw.rect(screen, (100, 100, 100), i, 0)# 壁書き込み
    
    for o in objects: #プレイヤーの行動結果
        if not dead[o.number-1]: #死亡済みプレイヤーはスキップ
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
        if o.rect.collidelist(wall) > -1 : #壁にぶつかると死亡(プレイヤーマスは死なない)
            if (time.time() - check_time) >= 0.1:
                check_time       = time.time()
                dead[o.number-1] = False
                dead_cnt         = np.sum(dead)
                o.colour         = WHITE
                o.bearing        = [0,0]
                print("player" + str(o.number)+ " is dead!!")
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
            if   o.colour == P1_COLOUR: 
                all_cell.append((o.rect,'1')) 
                momotaro_cell.append(o.rect)
            elif o.colour == P2_COLOUR: 
                all_cell.append((o.rect,'2'))
                kintaro_cell.append(o.rect)
            elif o.colour == P3_COLOUR: 
                all_cell.append((o.rect,'3'))
                urashima_cell.append(o.rect)
            elif o.colour == P4_COLOUR: 
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
        if   r[1] == '1': pg.draw.rect(screen, P1_COLOUR, r[0], 1)
        elif r[1] == '2': pg.draw.rect(screen, P2_COLOUR, r[0], 1)
        elif r[1] == '3': pg.draw.rect(screen, P3_COLOUR, r[0], 1)
        elif r[1] == '4': pg.draw.rect(screen, P4_COLOUR, r[0], 1)
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
    win1 = sysfont.render("player 1 WIN!!", True, P1_COLOUR)
    win2 = sysfont.render("player 2 WIN!!", True, P2_COLOUR)
    win3 = sysfont.render("player 3 WIN!!", True, P3_COLOUR)
    win4 = sysfont.render("player 4 WIN!!", True, P4_COLOUR)
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
