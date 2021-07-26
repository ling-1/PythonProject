import pygame
from pygame.locals import *
from itertools import cycle
import random
SCREENWIDTH=822
SCREENHIGHT=260
FPS=30

class Map():
    def __init__(self,x,y):
        self.bg=pygame.image.load("resources/bg.png").convert_alpha()
        self.x=x
        self.y=y
    def map_rolling(self):
        if self.x<-790:
            self.x=800
        else:
            self.x-=15
    def map_update(self):
        SCREEN.blit(self.bg,(self.x,self.y))
class Dinosaur():
    def __init__(self):
        self.rect=pygame.Rect(0,0,0,0)
        self.jumpstate=False
        self.jumpheight=130
        self.lowest_y=140
        self.jumpvalue=0
        self.dinosaurindex=0
        self.dinosaurindexgen=cycle([0,1,2])
        self.dinosaur_img=(
            pygame.image.load("resources/dinosaur1.png").convert_alpha(),
            
            pygame.image.load("resources/dinosaur2.png").convert_alpha(),
            pygame.image.load("resources/dinosaur3.png").convert_alpha(),
            )
        self.jump_audio=pygame.mixer.Sound("resources/jump.wav")
        self.rect.size=self.dinosaur_img[0].get_size()
        self.x=50;
        self.y=self.lowest_y;
        self.rect.topleft=(self.x,self.y)
    def jump(self):
        self.jumpstate=True
    def move(self):
        if self.jumpstate:
            if self.rect.y>=self.lowest_y:
                self.jumpvalue=-5
            if self.rect.y<=self.lowest_y-self.jumpheight:
                self.jumpvalue=10
            self.rect.y+=self.jumpvalue
            if self.rect.y>=self.lowest_y:
                self.jumpstate=False
    def draw_dinosaur(self):
        dinosaurindex=next(self.dinosaurindexgen)
        SCREEN.blit(self.dinosaur_img[dinosaurindex],
                    (self.x,self.rect.y))
class Obstacle():
    score=1
    def __init__(self):
        self.rect=pygame.Rect(0,0,0,0)
        self.stone=pygame.image.load("resources/stone.png").convert_alpha()
        self.cacti=pygame.image.load("resources/cacti.png").convert_alpha()
        self.numbers=(pygame.image.load("resources/0.png").convert_alpha(),
                      pygame.image.load("resources/1.png").convert_alpha(),
                      pygame.image.load("resources/2.png").convert_alpha(),
                      pygame.image.load("resources/3.png").convert_alpha(),
                      pygame.image.load("resources/4.png").convert_alpha(),
                      pygame.image.load("resources/5.png").convert_alpha(),
                      pygame.image.load("resources/6.png").convert_alpha(),
                      pygame.image.load("resources/7.png").convert_alpha(),
                      pygame.image.load("resources/8.png").convert_alpha(),
                      pygame.image.load("resources/9.png").convert_alpha(),
                      )
        self.score_audio=pygame.mixer.Sound("resources/score.wav")
        r=random.randint(0,1)
        if r==0:
            self.image=self.stone
        else:
            self.image=self.cacti
        self.rect.size=self.image.get_size()
        self.width,self.height=self.rect.size
        self.x=800;
        self.y=200-(self.height/2)
        self.rect.center=(self.x,self.y)
    def obstacle_move(self):
        self.rect.x-=20
    def draw_obstacle(self):
        SCREEN.blit(self.image,(self.rect.x,self.rect.y))
    def getscore(self):
        self.score
        tmp=self.score;
        if tmp==1:
            self.score_audio.play()
        self.score=0;
        return tmp;
    def showscore(self,score):
        self.scoredigits=[int(x) for x in list(str(score))]
        totalwidth=0
        for digit in self.scoredigits:
            totalwidth+=self.numbers[digit].get_width()
        xoffset=(SCREENWIDTH-totalwidth)/2
        for digit in self.scoredigits:
            SCREEN.blit(self.numbers[digit],(xoffset,SCREENHIGHT*0.1))
            xoffset+=self.numbers[digit].get_width()
def game_over():
    bump_audio=pygame.mixer.Sound("resources/bump.wav")
    bump_audio.play()
    screen_w=pygame.display.Info().current_w
    screen_h=pygame.display.Info().current_h
    over_img=pygame.image.load("resources/gameover.png").convert_alpha()
    SCREEN.blit(over_img,((screen_w-over_img.get_width())/2,
                          (screen_h-over_img.get_height())/2))
                
def mainGame():
    score=0
    global SCREEN,FPSCLOCK
    over=False
    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHIGHT))
    pygame.display.set_caption("dinosaur")
    bg1=Map(0,0)#实例化对象
    bg2=Map(800,0)#两个地图滚动形成连接效果
    dinosaur=Dinosaur()#实例化恐龙对象
    addobstacletimer=0
    list=[]
    
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
            if event.type==KEYDOWN and event.key==K_SPACE:
                if dinosaur.rect.y>=dinosaur.lowest_y:
                    dinosaur.jump()
                    dinosaur.jump_audio.play()

                if over==True:
                    mainGame()
        if over==False:
            bg1.map_update()
            bg1.map_rolling()
            bg2.map_update()
            bg2.map_rolling()
            dinosaur.move()
            dinosaur.draw_dinosaur()
            if addobstacletimer>=1300:
                r=random.randint(0,100)
                if r>40:
                    obstacle=Obstacle()
                    list.append(obstacle)
                addobstacletimer=0
            for i in range(len(list)):
                list[i].obstacle_move()
                list[i].draw_obstacle()
                if pygame.sprite.collide_rect(dinosaur,list[i]):
                    over=True
                    game_over()
                else:

                    if(list[i].rect.x+list[i].rect.width)<dinosaur.rect.x:
                        score+=list[i].getscore()
                list[i].showscore(score)
        addobstacletimer+=20
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
if __name__=='__main__':
    mainGame()
