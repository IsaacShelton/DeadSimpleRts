# https://opengameart.org/content/lava-splash
# https://opengameart.org/content/5-break-crunch-impacts

import pygame
import math
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Get the current display resolution
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
# screen_width = 1200
# screen_height = 800

# Create a borderless window that fills the entire screen
# screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Set a caption (optional; won't be visible without borders)
pygame.display.set_caption("Borderless Fullscreen Window")

enemy_sound = pygame.mixer.Sound("enemy.wav")
enemy_big_sound = pygame.mixer.Sound("enemybig.wav")
house_sound = pygame.mixer.Sound("house.wav")

class House:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("house.png").convert_alpha()

    def update(self):
        screen.blit(self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2))

class Enemy:
    def __init__(self, nums, x, y, dx, dy):
        self.nums = nums
        self.x = x
        self.y = y
        self.r = 64

        self.image1 = pygame.image.load("enemy1.png").convert_alpha()
        self.image2 = pygame.image.load("enemy2.png").convert_alpha()
        self.image3 = pygame.image.load("enemy3.png").convert_alpha()

        self.image12 = pygame.image.load("enemy12.png").convert_alpha()
        self.image13 = pygame.image.load("enemy13.png").convert_alpha()
        self.image23 = pygame.image.load("enemy23.png").convert_alpha()

        self.dx = dx
        self.dy = dy
        self.speed = 2

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        if self.nums == [1]:
            image = self.image1
        if self.nums == [2]:
            image = self.image2
        if self.nums == [3]:
            image = self.image3
        if self.nums == [1, 2]:
            image = self.image12
        if self.nums == [1, 3]:
            image = self.image13
        if self.nums == [2, 3]:
            image = self.image23

        if len(self.nums) > 1:
            image = pygame.transform.scale2x(image)

        screen.blit(image, (self.x - image.get_width() / 2, self.y - image.get_height() / 2))

class Man:
    def __init__(self, num, x, y):
        self.num = num
        self.image = pygame.image.load("./man" + str(num) + ".png").convert_alpha()
        self.x = x
        self.y = y
        self.r = self.image.get_width() / 4
        self.tx = x
        self.ty = y
        self.action = "move"
        self.speed = 10

    def update(self):
        if math.dist((self.x, self.y), (self.tx, self.ty)) < self.speed:
            self.action = "idle"

        if self.action != "idle":
            dy = self.ty - self.y
            dx = self.tx - self.x
            direction = math.atan2(dy, dx)

            self.x += self.speed * math.cos(direction)
            self.y += self.speed * math.sin(direction)

        r = self.image.get_width() / 3
        screen.blit(self.image, (self.x - r, self.y - 1.5 * r))


men = [
    Man(1, 100, 400),
    Man(2, 400, 400),
    Man(3, 700, 400),
]

houses = [
    House(200, screen_height - 100),
    House(screen_width - 200, screen_height - 100),
]

enemies = []

def move(action):
    keys = pygame.key.get_pressed()
    mx, my = pygame.mouse.get_pos()

    if keys[pygame.K_1]:
        men[0].tx = mx - 64
        men[0].ty = my - 100
        men[0].action = action
    if keys[pygame.K_2]:
        men[1].tx = mx - 64
        men[1].ty = my - 100
        men[1].action = action
    if keys[pygame.K_3]:
        men[2].tx = mx - 64
        men[2].ty = my - 100
        men[2].action = action


score = 0
level = 0
health = 3
clock = pygame.time.Clock()
gameover = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    buttons = pygame.mouse.get_pressed()

    if buttons[0]:
        move("move")
    if buttons[2]:
        move("attack")

    for man in men:
        man.update()

    for i in range(len(men)):
        for j in range(len(men)):
            if i <= j:
                continue

            m1 = men[i]
            m2 = men[j]
            dist = math.dist((m1.x, m1.y), (m2.x, m2.y))

            if dist < m1.r + m2.r:
                dy = m2.y - m2.y
                dx = m1.x - m2.x
                direction = math.atan2(dy, dx) + math.pi / 4
                over = (-dist + m1.r + m2.r) / (m1.r + m2.r)
                force = 20 * over
                m1.x += force * math.cos(direction)
                m2.y += force * math.sin(direction)
                m2.x -= force * math.cos(direction)
                m2.y -= force * math.sin(direction)

    for i in range(len(enemies)):
        for j in range(len(enemies)):
            if i <= j:
                continue

            m1 = enemies[i]
            m2 = enemies[j]
            dist = math.dist((m1.x, m1.y), (m2.x, m2.y))

            if dist < m1.r + m2.r:
                dy = m2.y - m2.y
                dx = m1.x - m2.x
                direction = math.atan2(dy, dx) + math.pi / 4
                over = (-dist + m1.r + m2.r) / (m1.r + m2.r)
                force = 20 * over
                m1.x += force * math.cos(direction)
                m2.y += force * math.sin(direction)
                m2.x -= force * math.cos(direction)
                m2.y -= force * math.sin(direction)

    if not gameover:
        level = score // 10
        if random.randint(0, 120) <= level // 30:
            kinds = []
            if level >= 0:
                kinds.append([1])
            if level >= 1:
                kinds.append([2])
            if level >= 3:
                kinds.append([3])
            if level >= 4:
                kinds.append([1])
                kinds.append([1])
                kinds.append([2])
                kinds.append([2])
                kinds.append([3])
                kinds.append([3])
                kinds.append([1, 2])
                kinds.append([1, 3])
                kinds.append([2, 3])

            x = random.choice([200, screen_width - 200])
            y = -128
            dx = 0
            dy = 1

            if level >= 0 and random.randint(0, 10) == 0:
                x, dx = random.choice([(200, 1.5), (screen_width - 200, -1.5)])
            enemy = Enemy(random.choice(kinds), x, y, dx, dy)
            enemy.speed /= len(enemy.nums)
            enemy.speed += (level // 2) / 10
            enemies.append(enemy)

        for house in houses:
            house.update()

        for enemy in enemies:
            enemy.update()

            touching = []
            for man in men:
                if math.dist((man.x, man.y), (enemy.x, enemy.y)) < 192:
                    touching.append(man.num)

            all = True
            for num in enemy.nums:
                if num not in touching:
                    all = False

            if all and enemy in enemies:
                enemies.remove(enemy)
                if len(enemy.nums) > 1:
                    score += 5
                    enemy_big_sound.play()
                else:
                    score += 1
                    enemy_sound.play()

            for house in houses:
                if math.dist((house.x, house.y), (enemy.x, enemy.y)) < 128 and enemy in enemies:
                    health -= 1
                    enemies.remove(enemy)
                    house_sound.play()
                    if health <= 0:
                        gameover = True

    font = pygame.font.SysFont("Arial", 48)
    text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height - 140 - text.get_height() / 2))
    text = font.render("Level: " + str(level), True, (0, 0, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height - 80 - text.get_height() / 2))
    text = font.render("Health: " + str(health), True, (0, 0, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height - 20 - text.get_height() / 2))

    pygame.display.flip()
    screen.fill((255, 255, 255))
    clock.tick(60)

pygame.quit()
