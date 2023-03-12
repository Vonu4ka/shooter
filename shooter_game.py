from pygame import *
from random import randint
from time import time as timer

display.set_caption('гуль-проект')

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))

font2 = font.SysFont('Arial', 36)

score = 0
goal = 25
lost = 0
max_lost = 8
life = 5


win_width = 700
win_height = 500
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
window = display.set_mode((win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15,20, -15)
        bullets.add(bullet)
            
player = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_height - 80)
            lost = lost + 1

ufos = sprite.Group()
for i in range(1, 6):
    ufo = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50,  randint(1,5))
    ufos.add(ufo)
  
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_height - 80)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid  = Asteroid('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

num_fire = 0
real_time = False
finish = False
game = True
while game:
    clock.tick(FPS)
    window.blit(background, (0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and real_time == False:
                    last_time = timer()
                    real_time = True
    if not finish:
        window.blit(background, (0,0))

        text = font2.render('Счет: ' +str(score), 1, (255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render('Пропущено: ' +str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))
    
        player.update()
        player.reset()
        ufos.update()
        ufos.draw(window)
        bullets.update() 
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if real_time == True:
            now_time = timer()

            if now_time - last_time < 1:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                real_time = False

        collides = sprite.groupcollide(ufos, bullets, True, True)
        for c in collides:
            score = score + 1
            ufo  = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            ufos.add(ufo)

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if sprite.spritecollide(player, ufos, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, ufos, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))

        if life == 5:
            life_color = (0, 150, 0)
        if life == 4:
            life_color = (0, 150, 0)
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0 , 0)      
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))  

        display.update()