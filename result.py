from pygame import *

# клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(
            self,
            player_image,
            player_x,
            player_y,
            player_speed
        ):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - 
        # прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас-спадкоємець для спрайту-гравця (керується стрілками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 60:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 60:
            self.rect.y += self.speed

class Player2(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 60:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 60:
            self.rect.y += self.speed
# клас-спадкоємець для спрайта-ворога (переміщається сам)
class Enemy(GameSprite):
    direction = "left"

    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

# клас для спрайтів-перешкод
class Wall(sprite.Sprite):
    def __init__(
        self,
        wall_x, 
        wall_y,
        wall_width,
        wall_height,
        color=(200, 0, 100)
    ):
        super().__init__()
        self.color = color
        self.width = wall_width
        self.height = wall_height
        # картинка стіни - прямокутник потрібних розмірів та кольору
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        # кожен спрайт повинен зберігати властивість rect - прямокутник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        

# Ігрова сцена:
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load(
    "background.jpg"), (win_width, win_height))

# Персонажі гри:
player = Player('hero.png', 5, win_height - 80, 4)
player2 = Player2('hero2.jpg', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 350, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

# стіни
w1 = Wall(100, 20, 570, 10)
w2 = Wall(100, 480, 350, 10)
w3 = Wall(100, 20, 10, 380)
w4 = Wall(200, 130, 10, 350)
w5 = Wall(450, 130, 10, 360)
w6 = Wall(300, 20, 10, 350)
w7 = Wall(390, 120, 130, 10)
w8 = Wall(670, 20, 10,200)
w9 =Wall(550, 210, 130, 10)
w10 =Wall(550, 210, 10, 100)

walls = [w1, w2, w3, w4, w5, w6, w7, w8, w9,w10]

barriers = [
    w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, monster
]

game = True
finish = False
clock = time.Clock()
FPS = 60

# написи
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

# музика
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        player2.update()
        monster.update()

        player.reset()
        player2.reset()
        monster.reset()
        final.reset()

    for wall in walls:
        wall.draw_wall()

    # Ситуація "Програш"
    for barrier in barriers:
        if sprite.collide_rect(player, barrier) or sprite.collide_rect(player2, barrier):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

    # Ситуація "Перемога"
    if sprite.collide_rect(player, final) and sprite.collide_rect(player2, final):
        finish = True
        window.blit(win, (200, 200))
        money.play()

    display.update()
    clock.tick(FPS)
