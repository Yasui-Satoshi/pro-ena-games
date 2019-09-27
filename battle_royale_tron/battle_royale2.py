#https://github.com/stanley-godfrey/Tron-Pygame
'''
    4-player tron battle
“The strong one doesn't win, the one that wins is strong.”
                                            (Franz Anton Beckenbauer)
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame               #pygameインポート
import time
import random
import numpy as np

pygame.init()               #pygame起動

BLACK     = (0  ,0  ,0  )   # ウインドウカラー(black)
WHITE     = (255,255,255)   # 死亡色
P1_COLOUR = (255,0  ,255)   # プレイヤーカラー１(C)
P2_COLOUR = (0  ,255,255)   # プレイヤーカラー２(M)
P3_COLOUR = (255,255,0  )   # プレイヤーカラー３(Y)
P4_COLOUR = (0  ,255,0  )   # プレイヤーカラー４(G)
P         = 2               # プレイヤーサイズ #only even number

class Player:               #プレイヤー設定
    def __init__(self, x, y, direction, colour):
        """
        init method for class
        """
        self.x       = x          # プレイヤー座標　X
        self.y       = y          # プレイヤー座標　Y
        self.speed   = 1          # プレイヤー速度  ?
        self.bearing = direction  # プレイヤー進行方向[x,y]
        self.colour  = colour     # プレイヤー色
        self.boost   = False      #false is boost active
        self.start_boost = time.time()  # used to control boost length
        self.boosts  = 3          #ブーストタイム(sec)
        self.rect    = pygame.Rect(self.x - P/2, self.y - P/2, P, P)  # プレイヤーオブジェクト(P*P)
        

    def __draw__(self):           #軌跡設定
        """
        method for drawing player
        """
        self.rect = pygame.Rect(self.x - P/2, self.y - P/2, P, P)  # redefines rectプレイヤーオブジェクト(2*2)
        pygame.draw.rect(screen, self.colour, self.rect, 0)  # draws player onto screen

    def __move__(self):           #移動設定
        """
        method for moving the player
        """
        if not self.boost:        # ブーストしてない時(通常)
            self.x += self.bearing[0]
            self.y += self.bearing[1]
        else:                     # ブーストしてる時
            self.x += self.bearing[0] * 2
            self.y += self.bearing[1] * 2   #2倍速

    def __boost__(self):          #ブースト設定
        """
        starts the player boost
        """
        if self.boosts > 0:
            self.boosts -= 1
            self.boost = True
            self.start_boost = time.time()


def new_game():                   #New_Game
    #new_p1 = Player(50, height / 2, (2, 0), P1_COLOUR)
    #new_p2 = Player(width - 50, height / 2, (-2, 0), P2_COLOUR)
    new_p1 = Player(50        , (height- offset)   / 4, ( P, 0), P1_COLOUR)  # player1
    new_p2 = Player(50        , (height- offset)*3 / 4, ( P, 0), P2_COLOUR)  # player2
    new_p3 = Player(width - 50, (height- offset)   / 4, (-P, 0), P3_COLOUR)  # player3
    new_p4 = Player(width - 50, (height- offset)*3 / 4, (-P, 0), P4_COLOUR)  # player4
    return new_p1, new_p2, new_p3, new_p4

#-------------------------------------------------------------------------------------#

width, height = 600, 660          # バトルエリア 
offset = height - width           # エリア外余白 #60
screen = pygame.display.set_mode((width, height))       # ウインドウ生成
pygame.display.set_caption("帰ってきた！第一回！陣取りゲーム！(Take2)RETURNS")# タイトル
font = pygame.font.Font(None, 72)                       #文字サイズ

clock = pygame.time.Clock()  # used to regulate FPS
check_time = time.time()  # used to check collisions with rects
objects = list()  # list of all the player objects
path = list()  # list of all the path rects in the game

p1 = Player(50        , (height- offset)   / 4, ( P, 0), P1_COLOUR)  # player1
p2 = Player(50        , (height- offset)*3 / 4, ( P, 0), P2_COLOUR)  # player2
p3 = Player(width - 50, (height- offset)   / 4, (-P, 0), P3_COLOUR)  # player3
p4 = Player(width - 50, (height- offset)*3 / 4, (-P, 0), P4_COLOUR)  # player4

objects.append(p1)
path.append((p1.rect, '1'))
objects.append(p2)
path.append((p2.rect, '2'))
objects.append(p3)
path.append((p3.rect, '3'))
objects.append(p4)
path.append((p4.rect, '4'))

#print(objects)
#print(path)

p_score = [0, 0, 0, 0]  # プレイヤースコア(勝利数)[p1,p2,p3,p4]
dead    = [0, 0, 0, 0]  # 死んだプレイヤーの数

wall_rects = [pygame.Rect([0, offset, 15, height]) , pygame.Rect([0, offset, width, 15]),\
              pygame.Rect([width - 15, offset, 15, height]),\
              pygame.Rect([0, height - 15, width, 15])]  # 外壁情報 600*600

done = True             #キーボードスイッチ
new  = True             #再戦スイッチ

while  done:            #done = True の間
    #キーボードイベントを取得(AIのみの場合不要)----------------------------------------
    for event in pygame.event.get():            # gets all event in last tick
        if   event.type == pygame.QUIT:         # close button pressed
            done = False
        elif event.type == pygame.KEYDOWN:  　　# keyboard key pressed
            # === Player 1 === #
            if   event.key == pygame.K_w:
                objects[0].bearing = (0, -P)
            elif event.key == pygame.K_s:
                objects[0].bearing = (0, P)     #           [W] 
            elif event.key == pygame.K_a:       #        [A]   [D]
                objects[0].bearing = (-P, 0)    #           [S]
            elif event.key == pygame.K_d:       #
                objects[0].bearing = (P, 0)     #          [Tab]
            elif event.key == pygame.K_TAB:
                objects[0].__boost__()
            # === Player 2 === #
            if   event.key == pygame.K_UP:
                objects[1].bearing = (0, -P)
            elif event.key == pygame.K_DOWN:    
                objects[1].bearing = (0, P)     #           [↑]
            elif event.key == pygame.K_LEFT:    #       [←]    [→]
                objects[1].bearing = (-P, 0)    #           [↓]
            elif event.key == pygame.K_RIGHT:   #
                objects[1].bearing = (P, 0)     #        R→[Shift]
            elif event.key == pygame.K_RSHIFT:  
                objects[1].__boost__()
            # === Player 3 === #
            if   event.key == pygame.K_t:
                objects[2].bearing = (0, -P)
            elif event.key == pygame.K_g:
                objects[2].bearing = (0, P)     #           [T]
            elif event.key == pygame.K_f:       #        [F]   [H]
                objects[2].bearing = (-P, 0)    #           [G]
            elif event.key == pygame.K_h:       #
                objects[2].bearing = (P, 0)     #        L←[Shift]  
            elif event.key == pygame.K_LSHIFT:
                objects[2].__boost__()
            # === Player 4 === #
            if   event.key == pygame.K_i:
                objects[3].bearing = (0, -P)
            elif event.key == pygame.K_k:
                objects[3].bearing = (0, P)     #           [I]
            elif event.key == pygame.K_j:       #        [J]   [L]
                objects[3].bearing = (-P, 0)    #           [K]
            elif event.key == pygame.K_l:       #
                objects[3].bearing = (P, 0)     #         [Space]
            elif event.key == pygame.K_SPACE:
                objects[3].__boost__()
    #--------------------------------------------------------------------------------------
    screen.fill(BLACK)                          # 背景書き込み
    for r in wall_rects: pygame.draw.rect(screen, (42, 42, 42), r, 0)# 壁書き込み


    for o in objects: #プレイヤーの行動結果
        if time.time() - o.start_boost >= 0.5:  # limits boost to 0.5s
            o.boost = False
        
        if o.colour ==WHITE:
            continue

        
        #衝突判定
        if (o.rect, '1') in path or (o.rect, '2') \
           in path or (o.rect, '3') in path or (o.rect, '4') in path \
           or o.rect.collidelist(wall_rects) > -1:  # パスか壁にぶつかった時
            # prevent player from hitting the path they just made
            if (time.time() - check_time) >= 0.1:
                check_time = time.time()

                if   o.colour == P1_COLOUR:
                    print("player 1 is dead!!")
                    dead[0] +=1
                    o.colour = WHITE
                    o.bearing = [0,0]
                    #p_score[1] += 1
                elif o.colour == P2_COLOUR:
                    print("player 2 is dead!!")
                    dead[1] +=1
                    o.colour = WHITE
                    o.bearing = [0,0]
                    #p_score[1] += 1
                elif o.colour == P2_COLOUR:
                    print("player 3 is dead!!")
                    dead[2] +=1
                    o.colour = WHITE
                    o.bearing = [0,0]
                    #p_score[1] += 1
                else:
                    print("player 3 is dead!!")
                    dead[3] +=1
                    o.colour = WHITE
                    o.bearing = [0,0]
                    #p_score[0] += 1

        else:  # 衝突してない時
            if o.colour == P1_COLOUR:
                path.append((o.rect, '1')) 
            elif o.colour == P2_COLOUR:
                path.append((o.rect, '2'))
            elif o.colour == P3_COLOUR:
                path.append((o.rect, '3'))
            else:
                path.append((o.rect, '4'))

        o.__draw__()
        o.__move__()
        dead_num = np.sum(dead)
        if dead_num ==3:
            if   dead[0]==0:p_score[0]+=1
            elif dead[1]==0:p_score[1]+=1
            elif dead[2]==0:p_score[2]+=1
            else           :p_score[3]+=1
            new = False
            new_p1, new_p2, new_p3, new_p4 = new_game()
            objects = [new_p1, new_p2, new_p3, new_p4]
            path = [(p1.rect, '1'), (p2.rect, '2'),(p3.rect, '3'),(p4.rect, '4')]
            break

    for r in path:
        if new is False:  # empties the path - needs to be here to prevent graphical glitches
            path = []
            new = True
            break
        if   r[1] == '1': pygame.draw.rect(screen, P1_COLOUR, r[0], 0)
        elif r[1] == '2': pygame.draw.rect(screen, P2_COLOUR, r[0], 0)
        elif r[1] == '3': pygame.draw.rect(screen, P3_COLOUR, r[0], 0)
        else: pygame.draw.rect(screen, P4_COLOUR, r[0], 0)


    # 現在のスコアを表示
    score_text = font.render('{0} : {1} : {2} : {3}'.format(p_score[0], p_score[1],p_score[2], p_score[3]), 1, (255, 153, 51))
    score_text_pos = score_text.get_rect()
    score_text_pos.centerx = int(width / 2)
    score_text_pos.centery = int(offset / 2)
    screen.blit(score_text, score_text_pos)

    pygame.display.flip()  # flips display
    clock.tick(60)         # regulates FPS

    sysfont = pygame.font.SysFont(None, 80,bold=True, italic=True)
    win1 = sysfont.render("player 1 WIN!!", True, (255,255,255))
    win2 = sysfont.render("player 2 WIN!!", True, (255,255,255))
    win3 = sysfont.render("player 3 WIN!!", True, (255,255,255))
    win4 = sysfont.render("player 4 WIN!!", True, (255,255,255))
    
    #3勝で勝利
    if p_score[0] == 3:
        print("player 1 WIN!!")
        screen.blit(win1, (50,200))
    elif p_score[1]== 3:
        print("player 2 WIN!!")
        screen.blit(win2, (50,200))
    elif p_score[2] == 3:
        print("player 3 WIN!!")
        screen.blit(win3, (50,200))
    elif p_score[3] == 3:
        print("player 4 WIN!!")
        screen.blit(win4, (50,200))
    
    pygame.display.update()
    
    if p_score[0]==3 or p_score[1]==3 or p_score[2]==3 or p_score[3]==3 :
        break
pygame.time.delay(1000)
pygame.quit()              # 終了
