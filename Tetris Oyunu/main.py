import pygame
import random

pygame.init()

WIDTH = 500
HEIGHT = 600
BLOCK = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

pygame.mixer.music.load("audio/music.ogg")
pygame.mixer.music.play(-1)

clear_sound = pygame.mixer.Sound("audio/clear.ogg")
rotate_sound = pygame.mixer.Sound("audio/rotate.ogg")

cols = 10
rows = 20

grid = [[(0,0,0) for _ in range(cols)] for _ in range(rows)]

shapes = [
    ([[1,1,1,1]], (0,255,255)),
    ([[1,1],[1,1]], (255,255,0)),
    ([[0,1,0],[1,1,1]], (200,0,200)),
    ([[1,0,0],[1,1,1]], (255,165,0)),
    ([[0,0,1],[1,1,1]], (0,0,255)),
    ([[1,1,0],[0,1,1]], (0,255,0)),
    ([[0,1,1],[1,1,0]], (255,0,0))
]

font = pygame.font.SysFont("arial",30)

def new_piece():
    shape,color = random.choice(shapes)
    return {"shape":shape,"color":color,"x":cols//2-2,"y":0}

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

def valid(piece):
    for y,row in enumerate(piece["shape"]):
        for x,val in enumerate(row):
            if val:
                px = piece["x"] + x
                py = piece["y"] + y
                if px < 0 or px >= cols or py >= rows:
                    return False
                if py >= 0 and grid[py][px] != (0,0,0):
                    return False
    return True

def merge(piece):
    for y,row in enumerate(piece["shape"]):
        for x,val in enumerate(row):
            if val:
                grid[piece["y"]+y][piece["x"]+x] = piece["color"]

def clear_lines():
    global score
    new_grid=[]
    lines=0
    for row in grid:
        if (0,0,0) not in row:
            lines+=1
        else:
            new_grid.append(row)

    for i in range(lines):
        new_grid.insert(0,[(0,0,0) for _ in range(cols)])

    for y in range(rows):
        grid[y]=new_grid[y]

    score += lines*100
    if lines>0:
        clear_sound.play()

def draw_grid():
    for y in range(rows):
        for x in range(cols):
            pygame.draw.rect(screen,(50,50,90),
                (x*BLOCK,y*BLOCK,BLOCK,BLOCK),1)

def draw_piece(piece):
    for y,row in enumerate(piece["shape"]):
        for x,val in enumerate(row):
            if val:
                pygame.draw.rect(screen,piece["color"],
                    ((piece["x"]+x)*BLOCK,
                     (piece["y"]+y)*BLOCK,
                     BLOCK,BLOCK))

def draw_locked():
    for y in range(rows):
        for x in range(cols):
            if grid[y][x]!=(0,0,0):
                pygame.draw.rect(screen,grid[y][x],
                    (x*BLOCK,y*BLOCK,BLOCK,BLOCK))

current = new_piece()
next_piece = new_piece()

score = 0

speed = 500
last = pygame.time.get_ticks()

running=True

while running:

    screen.fill((25,25,60))

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.KEYDOWN:

            if event.key==pygame.K_LEFT:
                current["x"]-=1
                if not valid(current):
                    current["x"]+=1

            if event.key==pygame.K_RIGHT:
                current["x"]+=1
                if not valid(current):
                    current["x"]-=1

            if event.key==pygame.K_UP:
                old=current["shape"]
                current["shape"]=rotate(current["shape"])
                if not valid(current):
                    current["shape"]=old
                else:
                    rotate_sound.play()

            if event.key==pygame.K_DOWN:
                speed=50

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_DOWN:
                speed=500

    now=pygame.time.get_ticks()

    if now-last>speed:
        current["y"]+=1

        if not valid(current):
            current["y"]-=1
            merge(current)
            clear_lines()
            big_font = pygame.font.SysFont("arial",60)
            current=next_piece
            next_piece=new_piece()

            if not valid(current):

                text = big_font.render("GAME OVER",True,(255,50,50))
                screen.blit(text,(80,250))
                pygame.display.update()

                pygame.time.delay(3000)

                running=False


        last=now

    draw_locked()
    draw_piece(current)
    draw_grid()

    pygame.draw.rect(screen,(70,70,150),(320,200,150,150))

    for y,row in enumerate(next_piece["shape"]):
        for x,val in enumerate(row):
            if val:
                pygame.draw.rect(screen,next_piece["color"],
                    (350+x*BLOCK,230+y*BLOCK,BLOCK,BLOCK))

    score_text = font.render("Score",True,(255,255,255))
    score_num = font.render(str(score),True,(255,255,255))

    screen.blit(score_text,(350,60))
    screen.blit(score_num,(360,100))

    next_text = font.render("Next",True,(255,255,255))
    screen.blit(next_text,(360,160))

    pygame.display.update()
    clock.tick(60)

pygame.quit()