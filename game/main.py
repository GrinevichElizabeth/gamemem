import pygame
import os
import time 
pygame.init()

def path_file(file_name):
    path_folder = os.path.abspath(__file__ + "/..")
    path = os.path.join(path_folder, file_name)
    return path


WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 40
YELLOW = (255, 210, 0)
GRAY = (80, 80, 80)
DARKER_GRAY = (50, 50, 50)
BLACK = (0, 0, 0)


window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

background = pygame.image.load(path_file('floor.PNG'))
background = pygame.transform.scale(background, (WIN_WIDTH, WIN_HEIGHT))
win_img = pygame.image.load(path_file("win_img.png"))
win_img = pygame.transform.scale(win_img, (WIN_WIDTH, WIN_HEIGHT))

loss_img =  pygame.image.load(path_file("loss_img.png"))
loss_img = pygame.transform.scale(loss_img, (WIN_WIDTH, WIN_HEIGHT))

title_img = pygame.image.load(path_file("title_screen.png"))
title_img = pygame.transform.scale(title_img, (WIN_WIDTH, WIN_HEIGHT))



pygame.mixer.music.load(path_file("main_sound.mp3"))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

music_win = pygame.mixer.Sound(path_file("win_sound.wav"))
music_win.set_volume(0.1)
music_loss = pygame.mixer.Sound(path_file("loss_sound.wav"))
music_loss.set_volume(0.1)
music_shoot = pygame.mixer.Sound(path_file("pew_sound.wav"))
music_shoot.set_volume(0.1)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, file_name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.scale(self.image, (width, height))
        

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def __init__(self, x, y, width, height, file_name, speed, direction, min_coord, max_coord):
        super().__init__(x, y, width, height, file_name)
        self.speed = speed
        self.direction = direction
        self.min_coord = min_coord
        self.max_coord = max_coord
    
    def update(self):
        if self.direction == "left" or self.direction == "right":
            if self.direction == "left":
                self.rect.x -= self.speed
            if self.direction == "right":
                self.rect.x += self.speed

            if self.rect.right >= self.max_coord:
                self.direction = "left"
            if self.rect.left <= self.min_coord:
                self.direction = "right"
        
        elif self.direction == "up" or self.direction == "down":
            if self.direction == "down":
                self.rect.y += self.speed 
            if self.direction == "up":
                self.rect.y -= self.speed

            if self.rect.top <= self.min_coord:
                self.direction = "down"
            if self.rect.bottom >= self.max_coord:
                self.direction = "up"

class Player(GameSprite):
    def __init__(self, x, y, width, height, file_name):
        super().__init__(x, y, width, height, file_name)
        self.speed_x = 0
        self.speed_y = 0 
        self.direction = "left"
        self.image_L = self.image
        self.image_R = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self.rect.left > 0 and self.speed_x < 0 or self.speed_x > 0 and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed_x
        walls_collide = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for wall in walls_collide:
                self.rect.right = min(self.rect.right, wall.rect.left)
        elif self.speed_x < 0:
            for wall in walls_collide:
                self.rect.left = max(self.rect.left, wall.rect.right)
        

        if self.rect.top > 0 and self.speed_y < 0 or self.speed_y > 0 and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speed_y
        walls_collide = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_y < 0:
            for wall in walls_collide:
                self.rect.top = max(self.rect.top, wall.rect.bottom) 
        elif self.speed_y > 0:
            for wall in walls_collide:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
    

    def shoot(self):
        if self.direction == "right":
            bullet = Bullet(self.rect.right, self.rect.centery, 25, 25, path_file("bullet.jpg"), 5)
            bullets.add(bullet)
        if self.direction == "left":
            bullet = Bullet(self.rect.left - 10, self.rect.centery, 25, 25, path_file("bullet.jpg"), -5)
            bullets.add(bullet)


class Bullet(GameSprite):
    def __init__(self, x, y, width, height, img, speed):
        super().__init__(x, y, width, height, img)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed

        if self.rect.left > WIN_WIDTH or self.rect.right < 0:
            self.kill()



class Button():
    def __init__(self, color, x, y, width, height,  text):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.font30 = pygame.font.SysFont("arial", 30)
        self.text = self.font30.render(text, True, BLACK)
    
    def button_show(self, px_x, px_y):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text, (self.rect.x + px_x, self.rect.y + px_y))

button_start = Button(GRAY, 310, 100, 100, 50, "start")
button_exit = Button(GRAY, 310, 180, 100, 50, "exit")
button_retry = Button(GRAY, 310, 180, 100, 50, "retry")
button_return = Button(GRAY, 310, 180, 100, 50, "return to menu")
    
player = Player(5, 110, 85, 70, path_file('creature.png'))

enemies = pygame.sprite.Group()
enemy1 = Enemy(0, 430, 70, 70, path_file('enemy.png'), 4, "right", 0, 360)
enemy2 = Enemy(390, 0, 50, 60, path_file('enemy2.png'), 2, "right", 390, 720)
enemies.add(enemy1, enemy2)



goal = GameSprite(434, 260, 100, 70, path_file("void.png"))

walls = pygame.sprite.Group()
wall1 = GameSprite(0, 210, 100, 25, path_file('walls.PNG'))
wall2 = GameSprite(100, 100, 25, 135, path_file('walls.PNG')) 
wall3 = GameSprite(110, 310, 145, 25, path_file('walls.PNG'))
wall4 = GameSprite(230, 0, 25, 310, path_file('walls.PNG'))
wall5 = GameSprite(100, 310, 25, 85, path_file('walls.PNG'))
wall6 = GameSprite(360, 180, 25, 340, path_file('walls.PNG'))
wall7 = GameSprite(380, 180, 225, 25, path_file('walls.PNG'))
wall8 = GameSprite(580, 180, 25, 205, path_file('walls.PNG'))
wall9 = GameSprite(480, 360, 125, 25, path_file('walls.PNG'))
wall10 = GameSprite(380, 0, 25, 85, path_file('walls.PNG'))
wall11 = GameSprite(510, 120, 25, 60, path_file('walls.PNG'))
wall12 = GameSprite(230, 310, 25, 85, path_file('walls.PNG'))
wall13 = GameSprite(480, 480, 25, 25, path_file('walls.PNG'))
walls.add(wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9, wall10, wall11, wall12, wall13)

bullets = pygame.sprite.Group()

lives = pygame.sprite.Group()
life1 = GameSprite(0, 470, 25, 25, path_file("life.png"))
life2 = GameSprite(30, 470, 25, 25, path_file("life.png"))
life3 = GameSprite(60, 470, 25, 25, path_file("life.png"))
lives.add(life1, life2, life3)



level = 0
count = 0

game = True
play = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if level == 0:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if button_start.rect.collidepoint(x, y):
                    button_start.color = DARKER_GRAY
                elif button_exit.rect.collidepoint(x,y):
                    button_exit.color = DARKER_GRAY
                
                
                else:
                    button_start.color = GRAY
                    button_exit.color = GRAY
                    
                    

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y == event.pos
                if button_start.rect.collidepoint(x, y):
                    level = 1
                elif button_exit.rect.collidepoint(x,y):
                    game = False
                
                


        elif level == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 5
                    player.direction = "right"
                    player.image = player.image_R
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = -5
                    player.direction = "left"
                    player.image = player.image_L
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = -5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 5
                if event.key == pygame.K_SPACE:
                    player.shoot()
                    music_shoot.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 0


        elif level == 2:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if button_retry.rect.collidepoint(x,y):
                    button_retry.color = DARKER_GRAY
                else:
                    button_retry.color = GRAY
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_retry.rect.collidepoint(x, y):
                    level = 1
                

        
        elif level == 3:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if button_return.rect.collidepoint(x,y):
                    button_return.color = DARKER_GRAY
                else:
                    button_return.color = GRAY

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_return.rect.collidepoint(x, y):
                            level = 0



    if level == 0:
        window.blit(title_img, (0, 0))
        button_start.button_show(5, 5)
        button_exit.button_show(5, 5)
    elif level == 1:
        if play:
            window.blit(background, (0, 0))

            player.reset()
            player.update()

            enemies.draw(window)
            enemies.update()

            bullets.draw(window)
            bullets.update()


            goal.reset()

            walls.draw(window)
            lives.draw(window)

            if pygame.sprite.collide_rect(player, goal):
                play = False
                pygame.mixer.music.stop()
                music_win.play()
                level = 3
    
            if pygame.sprite.spritecollide(player, enemies, False):
                count += 1
                pygame.sprite.Group.remove(lives, life3)
                
                if count == 2:
                    pygame.sprite.Group.remove(lives, life2)
                elif count == 3:
                    pygame.sprite.Group.remove(lives, life1)
                
                
                    play = False
                    pygame.mixer.music.stop()
                    music_loss.play()
                    level = 2 


            pygame.sprite.groupcollide(bullets, walls, True, False)
            pygame.sprite.groupcollide(bullets, enemies, True, True)
    if level == 2:
        window.blit(loss_img, (0, 0))
        button_retry.button_show(5, 5)
        
            
    if level == 3:
        window.blit(win_img, (0, 0))
        button_return.button_show(5, 5)
        
            


    clock.tick(FPS)
    pygame.display.update()