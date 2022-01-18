import pygame

############################################################################################
# set screen
pygame.init()
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("bouns ball")

############################################################################################
# 
block = []

############################################################################################
# charactre class
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

############################################################################################
# enemy class
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

############################################################################################
# finish block class
class fin_block():
    def __init__(self):
        self.x = 0
        self.y = 0
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

############################################################################################
# main game
def main_game():
    global game_run, fin

    # character init
    circle = character()

    # setting
    game_run =  True
    clock = pygame.time.Clock()

    while game_run:
        dt = clock.tick(120)

        # key event
        pygame_event(circle)

        circle.move(screen_width, screen_height)

        screen.fill((0, 0, 0))
        for i in range(len(block)):
            circle.enemy_rect(block[i])
            block[i].draw()
        try:
            fin.draw()
        except:
            fin = fin_block()
            fin.draw()
        circle.move_fin(dt)
        circle.draw()

        # finish game
        if not game_run:
            break

        game_run = fin.finish(circle.result())

        pygame.display.flip()

    game_fin()

############################################################################################
# game finish screen
def game_fin():
    fin_run = True
    while fin_run:

        # key event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fin_run = False
        
        # mouse event
        pos = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()

        # if press retry button retry game
        if press[0]:
            if pos[0] >= 0 and pos[0] <= 50 and pos[1] >= 0 and pos[1] <= 50:
                fin_run = False
                main_game() 
        
        # screen draw
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 255), (0, 0, 50, 50))
        pygame.display.flip()

############################################################################################
# game key event
def pygame_event(circle):
    global game_run
    # key event
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

############################################################################################
# game map making
def make_map():
    global fin
    map_run = True
    i = len(block)

    while map_run:

        screen.fill((0, 0, 0))
        # key event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                map_run = False
        
        # mouse event
        pos = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()

        # if mouse left click make block
        # if mouse middle click make finish block
        # if mouse right click remove block
        try:
            if press[0]:
                block.append(enemy())
                block[i].x = pos[0]
                block[i].y = pos[1]
                i += 1
            if press[1]:
                fin = fin_block()
                fin.x = pos[0]
                fin.y = pos[1]
            if press[2]:
                block.pop()
                i -= 1
        except:
            pass
            
        # screen draw
        for j in range(len(block)):
            block[j].draw()
        try:
            fin.draw()
        except:
            pass
        
        pygame.display.flip()

############################################################################################
# start screen
def start():
    start_run = True
    m = False

    # font setting
    font = pygame.font.SysFont("arial", 50)
    text = font.render("game start", True, (255, 255, 0))
    font = pygame.font.SysFont("arial", 30)
    text1 = font.render("push the space", True, (255, 255, 0))
    font = pygame.font.SysFont("arial", 20)
    text_con = font.render("continue", True, (255, 255, 0))
    text_make_map = font.render("make map", True, (255, 255, 0))
    text_setting = font.render("setting", True, (255, 255, 0))
    text_quit = font.render("quit", True, (255, 255, 0))

    # load back ground image
    # change image path to your own
    start_background = pygame.image.load("python/i_wanna_be_the_guy/start_background.jpg")

    while start_run:

        # key event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game()
                elif event.key == pygame.K_m:
                    if m:
                        m = False
                    else:
                        m = True

        # screen draw
        screen.blit(start_background, (0, 0))
        screen.blit(text, (80, 150))
        screen.blit(text1, (100, 200))
        if m:
            pygame.draw.rect(screen, (128, 128, 128), (0, 0, screen_width/3, screen_height))
            pygame.draw.rect(screen, (100, 100, 100), (10, 10, screen_width/3 - 20, 40))
            pygame.draw.rect(screen, (100, 100, 100), (10, 60, screen_width/3 - 20, 40))
            pygame.draw.rect(screen, (100, 100, 100), (10, 110, screen_width/3 - 20, 40))
            pygame.draw.rect(screen, (100, 100, 100), (10, 160, screen_width/3 - 20, 40))
            screen.blit(text_con, (30, 15))
            screen.blit(text_make_map, (20, 65))
            screen.blit(text_setting, (35, 115))
            screen.blit(text_quit, (50, 165))
        pygame.display.flip()

############################################################################################
# start
start()
