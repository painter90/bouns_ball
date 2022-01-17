import pygame

pygame.init()
screen_width = 1920
screen_height = 1020
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("bouns ball")
block = []

class character:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.to_x = 0
        self.to_y = 0
        self.radius = 10
        self.color = (255, 255, 255)
        self.speed = 10
        self.reaction = False
        self.reaction_num = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, screen_width, screen_height):
        self.to_y = 0
        self.to_y += 9.8

        self.screen(screen_width, screen_height)
        
        if self.reaction:
            self.to_y -= self.reaction_num * 0.3
            self.reaction_num -= 1
    
    def move_fin(self, dt):
        self.x += self.to_x * dt / 50
        self.y += self.to_y * dt / 50


    def screen(self, screen_width, screen_height):
        if self.x <= self.radius:
            self.x = self.radius
        elif self.x >= screen_width - self.radius:
            self.x = screen_width - self.radius
        if self.y <= self.radius:
            self.y = self.radius
            self.reaction = False
        elif self.y >= screen_height - self.radius:
            self.reaction = True
            self.reaction_n()
    
    def reaction_n(self):
        if self.reaction:
            self.reaction_num = 100
    
    def enemy_rect(self, ene):
        if ene.y <= self.y + self.radius <= ene.y + ene.height/2 and (ene.x <= self.x + self.radius <= ene.x + ene.width or ene.x <= self.x - self.radius <= ene.x + ene.width):
            self.reaction = True
            self.reaction_n()
        elif ene.y + ene.height/2 <= self.y - self.radius <= ene.y + ene.height and (ene.x <= self.x + self.radius <= ene.x + ene.width or ene.x <= self.x - self.radius <= ene.x + ene.width):
            self.reaction = False
        elif ene.x <= self.x + self.radius <= ene.x + ene.width/2 and (ene.y <= self.y + self.radius <= ene.y + ene.height or ene.y <= self.y - self.radius <= ene.y + ene.height):
            self.x = ene.x - self.radius
        elif ene.x + ene.width/2 <= self.x - self.radius <= ene.x + ene.width and (ene.y <= self.y + self.radius <= ene.y + ene.height or ene.y <= self.y - self.radius <= ene.y + ene.height):
            self.x = ene.x + ene.width + self.radius
    
    def result(self):
        return self

class enemy():
    def __init__(self):
        self.x = 300
        self.y = 300
        self.width = 20
        self.height = 20
        self.color = (255, 255, 255)
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def result(self):
        return self

class fin_block():
    def __init__(self):
        self.x = 100
        self.y = 200
        self.width = 20
        self.height = 20
        self.color = (0, 255, 0)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def finish(self, char):
        if self.x <= char.x + char.radius and char.x - char.radius <= self.x + self.width:
            if self.y <= char.y + char.radius and char.y - char.radius <= self.y + self.height:
                return False
        return True

    def result(self):
        return self

def main_game():
    global game_run, fin

    circle = []
    circle = character()

    game_run =  True
    clock = pygame.time.Clock()

    while game_run:
        dt = clock.tick(120)
        screen.fill((0, 0, 0))

        pygame_event(circle)

        circle.move(screen_width, screen_height)
        for i in range(len(block)):
            circle.enemy_rect(block[i])
            block[i].draw()
        fin.draw()
        circle.move_fin(dt)
        circle.draw()
        if not game_run:
            break

        game_run = fin.finish(circle.result())

        pygame.display.flip()

    game_fin()

def game_fin():
    fin_run = True
    while fin_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fin_run = False
        
        pos = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()
        if press[0]:
            if pos[0] >= 0 and pos[0] <= 50 and pos[1] >= 0 and pos[1] <= 50:
                fin_run = False
                main_game() 
        
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 255), (0, 0, 50, 50))
        pygame.display.flip()

def pygame_event(circle):
    global game_run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                circle.to_x += circle.speed
            elif event.key == pygame.K_LEFT:
                circle.to_x -= circle.speed
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                circle.to_x += circle.speed
            elif event.key == pygame.K_RIGHT:
                circle.to_x -= circle.speed

def make_map():
    global fin
    map_run = True
    i = len(block)
    while map_run:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                map_run = False
        
        pos = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()
        try:
            if press[0]:
                block.append(enemy())
                block[i].x = pos[0]
                block[i].y = pos[1]
                i += 1
            elif press[1]:
                fin = fin_block()
                fin.x = pos[0]
                fin.y = pos[1]
        except:
            pass
        try:
            if press[2]:
                block.pop()
                i -= 1
        except:
            pass
        for j in range(len(block)):
            block[j].draw()
        try:
            fin.draw()
        except:
            pass
        
        pygame.display.flip()

def start():
    start_run = True
    font = pygame.font.SysFont("arial", 50)
    text = font.render("game start", True, (255, 255, 0))
    font = pygame.font.SysFont("arial", 30)
    text1 = font.render("push the space", True, (255, 255, 0))
    start_background = pygame.image.load("python/i_wanna_be_the_guy/start_background.jpg")
    while start_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game()
                elif event.key == pygame.K_m:
                    make_map()

        screen.blit(start_background, (0, 0))
        screen.blit(text, (80, 150))
        screen.blit(text1, (100, 200))
        pygame.display.flip()

start()