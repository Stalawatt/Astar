import pygame as pg, Astar_algorithm as ASTAR 
import sys, math


pg.init()
pg.font.init()


squares_per_row :int = 10

SIZE :int = 500

WIN = pg.display.set_mode((SIZE + squares_per_row  + 100,SIZE + squares_per_row + 100)) # 100 extra pixels for the start button

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)


# WHITE IS FOR A FREE NODE
# BLACK IS FOR A WALL
# GREEN IS FOR THE START NODE
# RED IS FOR THE END NODE


class Grid:

    squares_per_row :int = squares_per_row
    square_size :int = (SIZE) / squares_per_row # a multiple of SIZE so that it fits on screen

    GRIDLIST = [] # goes in (y,x) coordinates
    GRIDLIST_colour = []

    def draw():
        for i in range(len(Grid.GRIDLIST)):
            for each in Grid.GRIDLIST[i]:
             pg.draw.rect(WIN, Grid.square_colour(Grid.GRIDLIST[i].index(each),i-1), each )

    def square_colour(x,y):
        #print(Grid.GRIDLIST_colour[y][x])
        if Grid.GRIDLIST_colour[y][x] == 0:
          colour = BLACK
        if Grid.GRIDLIST_colour[y][x] == 1:
          colour = WHITE
        if Grid.GRIDLIST_colour[y][x] == 2: 
          colour = GREEN
        if Grid.GRIDLIST_colour[y][x] == 3:
          colour = RED
          
        
        return (colour)

    def load_grid():

        for i in range(Grid.squares_per_row):
            Grid.GRIDLIST.append([])
         
        # loads each pg.rect object into a list so that 
        for i in range (Grid.squares_per_row):
            for j in range(Grid.squares_per_row):
                Grid.GRIDLIST[i].append(pg.Rect(((Grid.square_size+1) * j), ((Grid.square_size+1) * i), Grid.square_size, Grid.square_size))

        for i in range(Grid.squares_per_row):
          Grid.GRIDLIST_colour.append([])

        for i in range(Grid.squares_per_row):
          for j in range(Grid.squares_per_row):
            Grid.GRIDLIST_colour[i].append(1)

    def reset():
       Grid.GRIDLIST_colour = []
       Algorithm.path = []

       for i in range(Grid.squares_per_row):
          Grid.GRIDLIST_colour.append([])

       for i in range(Grid.squares_per_row):
         for j in range(Grid.squares_per_row):
           Grid.GRIDLIST_colour[i].append(1)

class Font :

   font = pg.font.SysFont("comicsansms)",15)


class Algorithm :

   path = []
   start = []
   end = []
  
   def run():
      
      print("START " + str(Algorithm.start))
      print("END " +str(Algorithm.end))
      maze = Grid.GRIDLIST_colour
      Algorithm.path = ASTAR.main(maze= maze, start= Algorithm.start, end= Algorithm.end)
      #print(Algorithm.path)
      Algorithm.path.remove((Algorithm.start[1],Algorithm.start[0]))
      Algorithm.path.remove((Algorithm.end[1],Algorithm.end[0]))

   



   def draw_path():
      for i in Algorithm.path:
         box = Grid.GRIDLIST[i[0]][i[1]]
         pg.draw.rect(WIN, BLUE, box)
            
    
         
   


class Reset  :
   width = 75
   height = 75
   x_Pos = SIZE + 10 + squares_per_row
   y_Pos = 10
   text = "Reset"
   label = Font.font.render(text, True, WHITE )
   button_background = pg.Rect(x_Pos, y_Pos, width, height)

   Colour = (25,25,25)
   def draw():
      
      pg.draw.rect(WIN, Reset.Colour, Reset.button_background)
      WIN.blit(Reset.label, (Reset.x_Pos + Reset.width/4, Reset.y_Pos + Reset.height/2 - Reset.label.get_height()))
      


class Click:

    boxClickedX :int = 0
    boxClickedY :int = 0

    clickMode = True

    # Change colours of squares

    def change_colour_black():
        if Grid.GRIDLIST_colour[Click.boxClickedY-1][Click.boxClickedX] != 0:
          Grid.GRIDLIST_colour[Click.boxClickedY-1][Click.boxClickedX] = 0
        else:
          Grid.GRIDLIST_colour[Click.boxClickedY-1][Click.boxClickedX] = 1
        return
          
    def change_colour_green():
        if Grid.GRIDLIST_colour[Click.boxClickedY-1][Click.boxClickedX] == 2:
          Grid.GRIDLIST_colour[Click.boxClickedY-1][Click.boxClickedX] = 1
        else:
          Grid.GRIDLIST_colour[Click.boxClickedY-1][Click.boxClickedX] = 2
        return
    
    def change_colour_red():
        if Grid.GRIDLIST_colour[Click.boxClickedY-1][Click.boxClickedX] == 3:
          Grid.GRIDLIST_colour[Click.boxClickedY-1][Click.boxClickedX] = 1
        else:
          Grid.GRIDLIST_colour[Click.boxClickedY-1][Click.boxClickedX] = 3
        return
    

    # Verify it is the ONLY start or end

    def verify_only_start():
       for i in Grid.GRIDLIST_colour:
        if 2 in i:
           i[i.index(2)] = 1
              
              
              
            
    def verify_only_end():
       for i in Grid.GRIDLIST_colour:
        if 3 in i:
           i[i.index(3)] = 1
              
          
      

    def handleClick(button):

        #button shows which button clicked, 1 for leftclick, 2 for middleclick, 3 for rightclick etc
        mousePosX, mousePosY = pg.mouse.get_pos()  #gets mouse position
        Click.boxClickedX = math.floor(mousePosX / (Grid.square_size+1))
        Click.boxClickedY = math.floor(mousePosY / (Grid.square_size+1))
        if button.button == 1: 
            if Click.boxClickedX > squares_per_row-1: # A WALL 
              Grid.reset()

            elif  Click.boxClickedY > squares_per_row-1 :
              Algorithm.run()

            else:
              
              Click.change_colour_black()
        

        elif button.button == 2 :
            if Click.boxClickedX > squares_per_row-1 or Click.boxClickedY > squares_per_row-1: # START POINT
              pass
            else:
              Click.verify_only_start()
              Algorithm.start = [Click.boxClickedX, Click.boxClickedY]
              Click.change_colour_green()

        elif button.button == 3:

            if Click.boxClickedX > squares_per_row-1 or Click.boxClickedY > squares_per_row-1: # END POINT
              pass
            else:
              Click.verify_only_end()
              Algorithm.end = [Click.boxClickedX, Click.boxClickedY]
              Click.change_colour_red()

        #print(Grid.GRIDLIST_colour)
        


def main() :
    
    clock = pg.time.Clock()
    Grid.load_grid()
    while True :
        clock.tick(120) # 60 FPS
        update()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                Click.handleClick(event)
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)


def update():
    WIN.fill((50,50,50))
    Grid.draw()
    Reset.draw()
    Algorithm.draw_path()
    pg.display.update()