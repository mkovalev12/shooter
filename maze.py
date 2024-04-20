from pygame import *

window = display.set_mode((900, 600))
display.set_caption('Labyrinth')

background = image.load('background.jpg')
background = transform.scale(background, (900, 600))

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, img, x_pos, y_pos, speed):
        super().__init__()
        self.img = transform.scale(image.load(img), (60, 60))
        self.rect = self.img.get_rect()
        self.rect = x_pos
        self.rect = y_pos
        self.speed = speed

    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))
    
    
    class Enemy(GameSprite):
        direction = 'left'
        def update(self):
            if self.rect.x >= 800:
                self.direction = 'left'
            if self.rect.x <= 500:
                self.direction = 'right'

            if self.direction == 'left':
                self.rect.x -= self.speed
            if self.direction == 'right':
                self.rect.x += self.speed



class Player(GameSprite):
    def update(self):
        pressed = key.get_pressed()
        if pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if pressed[K_d] and self.rect.y < 840:
            self.rect.x += self.speed
        if pressed[K_s] and self.rect.x < 540:
            self.rect.y += self.speed
        if pressed[K_w] and self.rect.y < 0:
            self.rect.y -= self.speed

class Wall(sprite.Sprite):
    def __init__(self, colors, width, height, pos_x, pos_y):
        super.colors = colors
        self.width = width
        self.height = height
        self.img = Surface((self.width, self.height))
        self.rect = self.img.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.img.fill(self.colors)


    def draw(self):
        window.blit(self.img, self.rect)
                       

player = Player('hero.png', 50, 500, 10)
enemy = Enemy('cyborg.png', 800, 400, 5)
goal = GameSprite('treasure.png', 700, 500, 0)

w1 = Wall((255,255,255), 10, 150, 445, 15)
w2 = Wall((255,255,255), 200, 10, 450, 155)
w3 = Wall((255,255,255), 140, 10, 445, 15)

game = True
finish = False

font.init()
ft = font.Font(None, 85)
win = ft.render('YOU WIN!', True, (0,255,0))
lose = ft.render('YOU LOSE!', True, (255, 0, 0))


while game:
    if not finish:
        window.blit(background, (0,0))
        player.draw()
        enemy.draw()
        goal.draw()
        player.update()
        enemy.update()
        w1.draw()
        w2.draw()
        w3.draw()

        
        if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3):
            finish = True
            kick.play()
            window.blit(lose, (350, 200))
        
        if sprite.collide_rect(player, goal):
            finish = True
            money.play()
            window.blit(win, (350, 200))

    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)