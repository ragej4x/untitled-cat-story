import pygame as pg
import csv, math
window = pg.display.set_mode((1024, 620))

pg.init()
renderScale = 3
display = pg.Surface((window.get_width()//renderScale, window.get_height()//renderScale))
pg.display.set_caption("LOMI")
clock = pg.Clock()



def debug():
    font = pg.font.Font("data/rainyhearts.ttf", 16)
    fps = str(int(clock.get_fps()))
    renderFPS = font.render(f"frames: {fps}", True, (200,200,200))
    window.blit(renderFPS, (3, 3))



    print(f"PlayerVelocity:{player.x_Vel, player.y_Vel} PlayerPos:{player.x ,player.y} JumpCounter:{player.jumpCounter} Fps:{clock.get_fps()} MousePos: {mouse[0]//renderScale, mouse[1]//renderScale}")

def eventHandler():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
            #pg.quit()

    
    rescale = pg.transform.scale(display,(window.get_width(), window.get_height()))
    window.blit(rescale, (0,0))

    debug()
    pg.display.flip()
    clock.tick(60)




#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




#MAP
    
class Map_class():
    def __init__(self) -> None:
        self.tile_image = pg.image.load("data/sprites/tiles/tilesheet.png")
        self.tileSurface = pg.Surface((24,24))
        self.tiles = []
        for tile in range (11):
            self.tiles.append(-24 * tile)

    def update_map(self):
        
        #print(self.tiles)
        y = 0
        with open ("data/mapdata.dat") as file:
            data = csv.reader(file, delimiter= ",")

            for row in data:
                x = -1
                for column in range(len(row)):
                    x += 1

                    if row[column] == "1":
                        self.ground = pg.draw.rect(display, (255,255,255), (x * 24 - camera.cameraX , y * 24 - camera.cameraY, 24 , 24),1)

                    #COLLISION
                        if self.ground.colliderect(player.player_rect.x + player.x_Vel , player.player_rect.y, player.player_rect.width , player.player_rect.height) and eventKey[pg.K_d]:
                            player.x_Vel = 0
                            #player.gravity = 1

                        if self.ground.colliderect(player.player_rect.x + player.x_Vel , player.player_rect.y, player.player_rect.width , player.player_rect.height) and eventKey[pg.K_a]:
                            player.x_Vel = 0
                            #player.gravity = 1


                        if self.ground.colliderect(player.player_rect.x, player.player_rect.y + player.y_Vel, player.player_rect.width , player.player_rect.height):
                            
                            player.y_Vel = 0
                            #self.onGround = True

                            if abs((player.player_rect.top + player.y_Vel) - self.ground.bottom) < 20:
                                self.jumpVel = 0
                                player.y_Vel = self.ground.bottom - player.player_rect.top
            
                            
                    #for i in range(11):

                    if row[column] == str(3):
                    
                        self.tileSurface.blit(self.tile_image, (self.tiles[3], 0))
                        
                        display.blit(self.tileSurface, (x * 24 - camera.cameraX , y * 24 - camera.cameraY ))

                            

                        
                y += 1

map = Map_class()


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#PLAYER
class Player_class():
    def __init__(self, x , y ) -> None:
        self.x = x
        self.y = y

        self.player_rect = pg.Rect((self.x , self.y, 16, 16))

        #movement var
        self.left = False
        self.right = True
        self.jump = False
        self.jumpVel = 10
        self.jumpCounter = 10

        self.speed = 3

        #weapon
        self.sword_animation_frame = 0
        
        
    def rect(self):
        self.player_rect = pg.Rect((self.x - camera.cameraX + 3, self.y - camera.cameraY+ 3, 10,15))
        pg.draw.rect(display, (0,255,0), self.player_rect, 1)
    def movement(self, eventKey):
        self.x_Vel = 0
        self.y_Vel = 0

        if eventKey[pg.K_d]:
            self.x_Vel += self.speed
            self.right = True
            self.left = False

        if eventKey[pg.K_a]:
            self.x_Vel -= self.speed
            self.right = False
            self.left = True

        if eventKey[pg.K_w] and self.jumpCounter == 10:
            self.jump = True
            self.jumpCounter = 0

        if self.jump == True :
            self.y_Vel -= self.jumpVel
            self.jumpVel -= 0.3
            
            if self.jumpVel < 0:
                self.jump = False
                self.jumpVel = 10

        self.jumpCounter += 0.2
        if self.jumpCounter > 10:
            self.jumpCounter = 10
        #gravity
        self.gravity = 5
        self.y_Vel += self.gravity
        if self.y_Vel > self.gravity:
            self.y_Vel = self.gravity



        
    def updateAnimation(self, window):

        if self.left == True and not eventKey[pg.K_a] and not eventKey[pg.K_d]:
            animate.idleAnimationLeft(window)
            
        if self.right == True and not eventKey[pg.K_a] and not eventKey[pg.K_d]:
            animate.idleAnimationRight(window)

        if eventKey[pg.K_a]:
            animate.runAnimationLeft(window)

        if eventKey[pg.K_d]:
            animate.runAnimationRight(window)

        if self.jump == True and self.left == True and not eventKey[pg.K_a] and not eventKey[pg.K_d]:
            animate.jumpAnimationLeft(window)

        if self.jump == True and self.left == True and not eventKey[pg.K_a] and not eventKey[pg.K_d]:
            animate.jumpAnimationRight(window) 
    




    def player_atk_func(self):
        self.sword_rect = pg.Rect((self.x - camera.cameraX,self.y - camera.cameraY + 12, 6, 2))
        

            

        


        if mouse[0]//renderScale >= self.player_rect.x:
            self.right = True
            self.left = False
            self.sword_rect.x = self.player_rect.right + 5
            
            
        
        if mouse[0]//renderScale <= self.player_rect.x:
            self.right = False
            self.left = True
            self.sword_rect.x = self.player_rect.left - 10

        pg.draw.rect(display, (255,255,255), self.sword_rect) 
    

    #objects
    


player = Player_class(0,100)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#CAMERA
class cameraClass():
    def __init__(self):
         self.cameraX = player.x - 1024/6.3
         self.cameraY = player.y - 620/5.5
         self.cameraSpeed = 3
         self.cameraFixSpeed = 4

    def update(self, display, keyinput):
        camCenter = pg.Rect((1024/6.3 ,620/6.5 , 5,5))

        angle = math.atan2(player.y - self.cameraY - 620/6.5, player.x - self.cameraX - 1024/6.3)
        cdx = math.cos(angle)
        cdy = math.sin(angle)


        if not camCenter.colliderect(player.player_rect):
            self.cameraX += cdx * self.cameraSpeed
            self.cameraY += cdy * self.cameraSpeed

        if self.cameraX > player.x - 90:
            self.cameraSpeed = self.cameraFixSpeed
            
        elif self.cameraX + 220 < player.x:
            self.cameraSpeed = self.cameraFixSpeed
           # print("AAAA")
            
        #elif self.cameraY > player.y - 70:
        elif self.cameraY + 60 >  player.y:
            self.cameraSpeed = self.cameraFixSpeed

        elif self.cameraY + 160 <  player.y:
            self.cameraSpeed = player.gravity

        else:
            self.cameraSpeed = 3

camera = cameraClass()


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class animationClass():
    def __init__(self) -> None:
        self.idleImage = pg.image.load("data/sprites/idle_sprite.png")
        self.idleFrames = []
        self.idleSurface = pg.Surface((16,17))
        self.idleCount = 0

        self.runImage = pg.image.load("data/sprites/run_sprite.png")
        self.runFrames = []
        self.runSurface = pg.Surface((16,17))
        self.runCount = 0

        self.jumpImage = pg.image.load("data/sprites/jump_sprite.png")
        self.jumpFrames = []
        self.jumpSurface = pg.Surface((16,17))
        self.jumpCount = 0

        #WEAPON

        self.atk1Image = pg.image.load("data/sprites/atk1_sprite.png")
        self.atk1WeaponImage = pg.image.load("data/sprites/atk1_sprite.png")
        self.atk1Frames = []
        self.atk1Surface = pg.Surface((16,17))
        self.atk1Count = 0



    def idleAnimationLeft(self, window):
        self.idleSurface.fill(0)
        self.idleSurface.set_colorkey(0)

        for num in range(6):
            self.idleFrames.append(-16 * num)
        
        self.idleImageFlipped = pg.transform.flip(self.idleImage, True, False)
        self.idleSurface.blit(self.idleImageFlipped,(self.idleFrames[int(self.idleCount)], 0))
        self.idleCount += 0.12
        

        window.blit(self.idleSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))


    def idleAnimationRight(self, window):
        self.idleSurface.fill(0)
        self.idleSurface.set_colorkey(0)

        for num in range(6):
            self.idleFrames.append(-16 * num)

        
        self.idleSurface.blit(self.idleImage,(self.idleFrames[int(self.idleCount)], 0))
        self.idleCount += 0.12

        window.blit(self.idleSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))


    def runAnimationLeft(self, window):
        self.runSurface.fill(0)
        self.runSurface.set_colorkey(0)

        for num in range(8):
            self.runFrames.append(-16 * num)
        
        self.runImageFlipped = pg.transform.flip(self.runImage, True, False)
        self.runSurface.blit(self.runImageFlipped,(self.runFrames[int(self.runCount)], 0))
        
        self.runCount += 0.2
        window.blit(self.runSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))
        

    def runAnimationRight(self, window):
        self.runSurface.fill(0)
        self.runSurface.set_colorkey(0)

        for num in range(8):
            self.runFrames.append(-16 * num)
        
        
        self.runSurface.blit(self.runImage,(self.runFrames[int(self.runCount)], 0))
        
        self.runCount += 0.2
        window.blit(self.runSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))


    def jumpAnimationLeft(self, window):
        self.jumpSurface.fill(0)
        self.jumpSurface.set_colorkey(0)

        for num in range(12):
            self.jumpFrames.append(-16 * num)
        
        self.jumpImageFlipped = pg.transform.flip(self.jumpImage, True, False)
        self.jumpSurface.blit(self.jumpImageFlipped,(self.jumpFrames[int(self.jumpCount)], 0))
        
        self.jumpCount += 0.12
        window.blit(self.jumpSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))

    def jumpAnimationRight(self, window):
        self.jumpSurface.fill(0)
        self.jumpSurface.set_colorkey(0)

        for num in range(12):
            self.jumpFrames.append(-16 * num)
        
        
        self.jumpSurface.blit(self.jumpImage,(self.jumpFrames[int(self.jumpCount)], 0))
        
        self.jumpCount += 0.12
        window.blit(self.jumpSurface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))

    #ATK ANIMATION


    def atk1AnimationLeft(self, window):
        self.atk1Surface.fill(0)
        self.atk1Surface.set_colorkey(0)

        for num in range(6):
            self.atk1Frames.append(-16 * num)
        
        self.atk1ImageFlipped = pg.transform.flip(self.atk1Image, True, False)
        self.atk1Surface.blit(self.atk1ImageFlipped,(self.atk1Frames[int(self.atk1Count)], 0))
        self.atk1Count += 0.12
        

        window.blit(self.atk1Surface,(player.x - camera.cameraX, player.y - camera.cameraY + 3))



animate = animationClass()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++





#MAIN
while True:

    #KEY EVENTS
    mouse = pg.mouse.get_pos()
    eventKey = pg.key.get_pressed()

    #window.fill((255,0,255))
    display.fill((30,30,30))



    #CALL FUNC AND CLASS

    player.movement(eventKey)
    player.rect()
    map.update_map()
    
    camera.update(display, eventKey)

    player.player_atk_func()
    player.updateAnimation(display)

    player.x += player.x_Vel
    player.y += player.y_Vel

    eventHandler()

