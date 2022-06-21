import pygame as pg

WIDTH = 550
background_color = (251,247,245)
original_grid_element_color = (52, 31, 151)
buffer = 5

w = 9
h = 9
grid = [[0 for x in range(w)] for y in range(h)]

#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pg.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pg.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


def insert(win, position):
    i,j = position[1], position[0]
    myfont = pg.font.SysFont('Comic Sans MS', 35)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if(event.key == 48): #checking with 0
                    grid[i-1][j-1] = event.key - 48
                    pg.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50 + buffer,50 -2*buffer , 50 - 2*buffer))
                    pg.display.update()
                    return
                if(0 < event.key - 48 <10):  #checking for valid input
                    pg.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50 + buffer,50 -2*buffer , 50 - 2*buffer))
                    value = myfont.render(str(event.key-48), True, (0,0,0))
                    win.blit(value, (position[0]*50 +15, position[1]*50+15))
                    grid[i-1][j-1] = event.key - 48
                    pg.display.update()
                    return
                return
        
def isEmpty(num):
    if num == 0:
        return True
    return False

def isValid(position, num):
     #Check for Column, row and sub-grid
    
    #Checking row
    for i in range(0, len(grid[0])):
        if(grid[position[0]][i] == num):
            return False
    
    #Checking column
    for i in range(0, len(grid[0])):
        if(grid[i][position[1]] == num):
            return False
    
    #Check sub-grid  
    x = position[0]//3*3
    y = position[1]//3*3
    #Gives us the box number
    
    for i in range(0,3):
        for j in range(0,3):
            if(grid[x+i][y+j]== num):
                return False
    return True


solved = 0
def sudoku_solver(win):
    myfont = pg.font.SysFont('Comic Sans MS', 35)
    for i in range(0,len(grid[0])):
        for j in range(0, len(grid[0])):
            if(isEmpty(grid[i][j])): 
                for k in range(1,10):
                    if isValid((i,j), k):                   
                        grid[i][j] = k
                        pg.draw.rect(win, background_color, ((j+1)*50 + buffer, (i+1)*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                        value = myfont.render(str(k), True, (255,0,0))
                        win.blit(value, ((j+1)*50 +15,(i+1)*50+15))
                        pg.display.update()
                        pg.time.delay(25)
                        
                        sudoku_solver(win)
                        
                        #Exit condition
                        global solved
                        if(solved == 1):
                            return
                        
                        #if sudoku_solver returns, there's a mismatch
                        grid[i][j] = 0
                        pg.draw.rect(win, background_color, ((j+1)*50 + buffer, (i+1)*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                        pg.display.update()
                        #pg.time.delay(50)
                return               
    solved = 1

def main():    
    pg.init()
    win = pg.display.set_mode((WIDTH, WIDTH+75))
    pg.display.set_caption("Sudoku")
    win.fill(background_color)
    myfont = pg.font.SysFont('Comic Sans MS', 35)
    
    
    for i in range(0,10):
        if(i%3 == 0):
            pg.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i ,500 ), 4 )
            pg.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 4 )

        pg.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i ,500 ), 2 )
        pg.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2 )
    pg.display.update()
    
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if(0<grid[i][j]<10):
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j+1)*50 + 15, (i+1)*50 + 15))
    pg.display.update()
        
    #load button images
    solve_img = pg.image.load('solving.png').convert_alpha()

    #create button instances
    solve_button = Button(225,525, solve_img, 0.08)
    
    
    while True: 
        
        if solve_button.draw(win):
               sudoku_solver(win)
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                pos = pg.mouse.get_pos()
                insert(win, (pos[0]//50, pos[1]//50))
            if event.type == pg.QUIT:
                pg.quit()
                return
   
main()
