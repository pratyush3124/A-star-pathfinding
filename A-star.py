import pygame

pygame.init()

white = (255, 255, 255)  # empty
blue = (100, 120, 255)  # covered
black = (0, 0, 0)     # block
red = (230, 10, 10)   # end
green = (50, 230, 50)  # start
yellow = (255, 255, 10)  # nah
grey = (180, 180, 180)  # path

WIDTH = 600
ROWS = 100

screen = pygame.display.set_mode((WIDTH, WIDTH))
screen.fill(white)


class node:
    color = white
    parent = None
    h = 0
    g = 0
    f = g+h

    def __init__(self, x, y):
        self.pos = (x, y)

nodes = {}
end = ()
start = ()

def creat_rect(x, y, color):
    t = WIDTH/ROWS
    pygame.draw.rect(screen, color, (x*t, y*t, t, t))


def generate_path(node):
    a = node
    while a != 'Start':
        creat_rect(a.pos[0], a.pos[1], green)
        pygame.display.update()
        a = a.parent

def Astar(mode):
    openlist = []
    closedlist = []
    openlist.append(nodes[start])
    while openlist != []:

        # smallest element
        a = openlist[0]
        for i in openlist:
            if i.f < a.f:
                a = i
        current = a
        openlist.remove(a)


        # finding neighbours
        neighbours = []
        for i in range(3):
            for j in range(3):
                if mode == 'euclidean':
                    if i!=1 or j!=1:
                        neighbours.append((i,j))
                if mode == 'manhatten':
                    if (i+j) % 2 != 0:
                        neighbours.append((i,j))
                if mode == 'diagonal':
                    if i!=1 or j!=1:
                        neighbours.append((i,j))
        
        # checkiing neighbours
        for neighbour in neighbours:

            successor = nodes[(current.pos[0]-1+neighbour[0], current.pos[1]-1+neighbour[1])]
            a,b = successor.pos[0], successor.pos[1]

            if successor.color == red:
                generate_path(current)
                return
            elif successor.color == green:
                continue
            elif successor.color == black:
                continue
            elif successor.color == white:

                # initializing successor
                successor.parent = current

                if mode == 'euclidean':
                    successor.h = ((end[0]-a)**2 + (end[1]-b)**2)**(1/2)*10//1
                    successor.g = current.g+14 if (neighbour[0]+neighbour[1])%2==0 else current.g+10
                if mode == 'manhatten':
                    successor.h = abs(end[0]-a)*10 + abs(end[1]-b)*10
                    successor.g = current.g + 10
                if mode == 'diagonal':
                    successor.h = max(abs(end[0]-a), abs(end[1]-b))*10
                    successor.g = current.g + 10

                successor.f = successor.g + successor.h
            
            if successor.color == yellow:
                for t in closedlist:
                    if t.pos == successor.pos:
                        if t.g < successor.g:
                            continue
                        else:
                            closedlist.remove(t)
            else:
                successor.color = yellow
                openlist.append(successor)
                creat_rect(a, b, yellow)
                pygame.display.update()

        closedlist.append(current)
        creat_rect(current.pos[0], current.pos[1], blue)
        pygame.display.update()


def click(pos):
    global end, start
    t = WIDTH//ROWS
    x, y = pos[0]//t, pos[1]//t

    if start_pressed == 1:
        color = green
        start = (x, y)
        nodes[start].color = color
        nodes[start].parent = 'Start'
    elif end_pressed == 1:
        color = red
        end = (x, y)
        nodes[end].color = color
    else:
        color = black
        nodes[(x, y)].color = color
    creat_rect(x, y, color)


def refresh():
    global nodes, start, end
    nodes = {}
    start = ()
    end = ()

    for i in range(ROWS):
        for j in range(ROWS):
            creat_rect(i, j, white)
            nodes[(i, j)] = node(i, j)

    # border
    for i in range(ROWS):
        nodes[(0, i)].color = black
        creat_rect(0, i, black)
        nodes[(ROWS-1), i].color = black
        creat_rect(ROWS-1, i, black)
        if i != 0 and i != ROWS-1:
            nodes[(i, 0)].color = black
            creat_rect(i, 0, black)
            nodes[i, (ROWS-1)].color = black
            creat_rect(i, ROWS-1, black)


start_pressed = 0
end_pressed = 0
mode = 'euclidean'

refresh()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == 115: # s
                start_pressed = 1
            if event.key == 101: # e
                end_pressed = 1
            if event.key == 32: # Spacebar
                Astar(mode)
            if event.key == 8: # Backspace
                refresh()
            if event.key == 49: # 1
                mode = 'euclidean'
            if event.key == 50: # 2
                mode = 'manhatten'
            if event.key == 51: # 3
                mode = 'diagonal'
        
        if event.type == pygame.KEYUP:
            if event.key == 115:
                start_pressed = 0
            if event.key == 101:
                end_pressed = 0
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            click(event.pos)
            break
        
        if event.type == pygame.MOUSEMOTION:
            if event.buttons == (1, 0, 0):
                click(event.pos)
                break
    try:
        pygame.display.update()
    except:
        break
