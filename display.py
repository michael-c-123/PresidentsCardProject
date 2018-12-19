import pygame

class Button:
    """A button for clicking"""
    def __init__(self, msg, dimension, color):
        self.msg = msg
        self.dimension = dimension
        self.color = color
        self.orig_color = color
        self.on = True
        self.click = None
        self.action = None

    #change status of button depending on user actions
    def update(self, gameDisplay, event=None):
        if event != None and self.on and \
            (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP):
            
            cursor = pygame.mouse.get_pos()
            click_status = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = cursor

            if contains_point(cursor,self.dimension):
                if click_status[0] == 1 and contains_point(self.click, self.dimension):
                    self.color = change_shade(self.orig_color,-100) #darken
                else:
                    self.color = change_shade(self.orig_color, 100) #brighten
                if event.type == pygame.MOUSEBUTTONUP:
                    if contains_point(self.click, self.dimension) and self.action != None:
                        self.action()
                    self.click = None
            else:
                self.color = self.orig_color
              
    def draw(self, gameDisplay):
        #draw rectangle
        if not self.on:
            pygame.draw.rect(gameDisplay, change_shade(self.orig_color, -125), self.dimension)
        else:
            pygame.draw.rect(gameDisplay, self.color, self.dimension)
        #draw text
        draw_text(gameDisplay, self.msg, self.dimension)

def draw_text(gameDisplay, msg, dimension, color=(0,0,0), size = 20):
    textSurface, textRect = get_font(msg, color, size)
    textRect.center = dimension[2] / 2 + dimension[0], dimension[3] / 2 + dimension[1]
    gameDisplay.blit(textSurface, textRect)

class ImageButton:
    enabled = True
    """An image that can be clicked"""
    def __init__(self, img, point):
        self.img = img
        self.dimension = (point[0], point[1], img.get_size()[0], img.get_size()[1])
        self.clicked = False
        self.actions = []
        self.bumped = False
    #change status of button depending on user actions
    def update(self, gameDisplay, event=None):
        if event != None and (ImageButton.enabled or self.clicked) and \
            (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP):
            
            cursor = pygame.mouse.get_pos()
            if contains_point(cursor, self.dimension) and event.type == pygame.MOUSEBUTTONDOWN:
                ImageButton.enabled = False
                self.clicked = True

            if event.type == pygame.MOUSEBUTTONUP:
                ImageButton.enabled = True
                if contains_point(cursor, self.dimension):
                    if self.clicked:
                        for action in self.actions:
                            action()    
                self.clicked = False
              
    def draw(self, gameDisplay):
        gameDisplay.blit(self.img, (self.dimension[0], self.dimension[1]))

def contains_point(point,dimension):
    px = point[0] #point location
    py = point[1]
    x = dimension[0]
    y = dimension[1]
    w = dimension[2]
    h = dimension[3]
    return px >= x and px < x + w and py >= y and py < y + h

#darken or brighten color
def change_shade(color,val=100):
    color_list = []
    for rgb in color:
        rgb+=val
        if rgb > 255:
            rgb = 255
        elif rgb < 0:
            rgb = 0
        color_list.append(rgb)
    return tuple(color_list)

#retrieve desired font thing and rectangle
def get_font(text,color,size):
    font = pygame.font.SysFont("arial", size)    
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class Moveable:
    """Image that can be moved by mouse"""
    enabled = True
    def __init__(self, img, point):
        self.img = img
        self.point = point
        self.click = None
        self.orig_point = None #point at which image was before moving
        self.action = None
        self.grabbed = False
    def update(self, gameDisplay, event):
        #move image with user input
        if event != None and (Moveable.enabled or self.grabbed) and \
            (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP):
            
            cursor = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if contains_point(
                    cursor, (self.point[0], self.point[1], self.img.get_size()[0], self.img.get_size()[1])):
                    self.click = cursor
                    self.orig_point = self.point[0], self.point[1]
                    self.grabbed = True
                    Moveable.enabled = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.click = None
                self.grabbed = False
                Moveable.enabled = True
                if self.orig_point!=None:
                    self.point = self.orig_point[0], self.orig_point[1]
                if self.action != None:
                    self.action()

            if self.click!=None:
                dx = cursor[0]-self.click[0]
                dy = cursor[1]-self.click[1]
                self.point = (self.orig_point[0]+dx, self.orig_point[1]+dy)

    def draw(self, gameDisplay):
        gameDisplay.blit(self.img, self.point)

class Image:
    """Simple image"""
    def __init__(self, img, point):
        self.img = img
        self.point = point
    def get_dimension(self):
        return (self.point[0],self.point[1], self.img.get_size()[0], self.img.get_size()[1])
    def update(self, gameDisplay, event):
        pass
    def draw(self, gameDisplay):
        gameDisplay.blit(self.img, self.point)

class Text:
    """Simple screen text"""
    def __init__(self, msg, dimension, color=(0,0,0), size = 20):
        self.msg = msg
        self.dimension = dimension
        self.color = color
        self.size = size
    def update(self, gameDisplay, event):
        pass
    def draw(self, gameDisplay):
        draw_text(gameDisplay, self.msg, self.dimension, self.color, self.size)
