import pygame
import os
import sys
from .map import *
from settings import *
from player import *
from villager import *
from Buildings import buildings
from .utils import draw_text
from projectPython.game.camera import Camera

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        # map
        self.map = Map(75,75, self.width, self.height)

        # camera
        self.camera = Camera(self.width,self.height)

        # Writing style
        myfont = pygame.font.SysFont("monospace", 20)

        #  INIT FOR RESSOURCES DISPLAY
        self.display_stone = myfont.render(str(playerOne.ressources[0]), True, (10, 10, 10))
        self.display_gold = myfont.render(str(playerOne.ressources[1]), True, (10, 10, 10))
        self.display_lumber = myfont.render(str(playerOne.ressources[2]), True, (10, 10, 10))
        self.display_food = myfont.render(str(playerOne.ressources[3]), True, (10, 10, 10))

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(120)
            self.events()
            self.update()
            self.draw()



    def events(self):

        for event in pygame.event.get():

            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # USER PRESSED A KEY
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    # Quit to menu screen instead maybe
                    pygame.quit()
                    sys.exit()

                # Enable - Disable health bars
                if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    global ENABLE_HEALTH_BARS
                    if ENABLE_HEALTH_BARS == False:
                        ENABLE_HEALTH_BARS = True
                    else:
                        ENABLE_HEALTH_BARS = False


            # USER PRESSED A MOUSEBUTTON
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:  #  LEFT CLICK
                    # we check the clicks for every building
                    for b in buildings:
                        b.select()
                        # we print the position of the mouse on the map if the mouse is on the map
                        print(b.pos_mouse() if 1 <= b.pos_mouse()[0] <= 10 and 1 <= b.pos_mouse()[
                            1] <= 10 else "not on map")

                elif event.button == 3:  # RIGHT CLICK
                    if testUnit1.is_alive:
                        testUnit2.attack(testUnit1)


    def update(self):
        self.camera.update()

    # GAME DISPLAY
    def draw(self):

        # BLACK BACKGROUND
        self.screen.fill((0,0,0))
        # Rendering "block", as Surface grass_tiles is in the same dimension of screen so just add (0,0)
        self.screen.blit(self.map.grass_tiles, (self.camera.scroll.x,self.camera.scroll.y))

        # FOR THE MAP
        for x in range(self.map.grid_length_x):
            for y in range(self.map.grid_length_y):
                # square = self.map.map[x][y]["drect"]
                # rect = pygame.Rect(square[0][0], square[0][1], TILE_SIZE,TILE_SIZE)
                #pygame.draw.rect(self.screen, (0,255,255),rect,1)
                #pygame.draw.rect(surface, color, rect, width...)

                render_pos = self.map.map[x][y]["render_pos"]
                #moving rendering part of "block" to map.py to increase fps
                #self.screen.blit(self.map.tiles["block"], (render_pos[0] + self.width/2, render_pos[1]+self.height/4 ))

                # Rendering tile, if it is not a tree or rock then render nothing as we already had block with green grass
                tile = self.map.map[x][y]["tile"]
                if tile != "":
                    self.screen.blit(self.map.tiles[tile],
                                     (render_pos[0] + self.map.grass_tiles.get_width()/2 + self.camera.scroll.x,
                                      render_pos[1] - (self.map.tiles[tile].get_height() -TILE_SIZE) + self.camera.scroll.y))


                # p = self.map.map[x][y]["iso_poly"]
                # p = [(x+self.width/2, y + self.height/4) for x, y in p]
                #pygame.draw.polygon(self.screen, (255,255,255), p, 1)

        # ressources display
        self.screen.blit(top_menu, (180, 95))
        self.screen.blit(self.display_stone, (300, 130))
        self.screen.blit(self.display_gold, (500, 130))
        self.screen.blit(self.display_lumber, (700, 130))
        self.screen.blit(self.display_food, (900, 130))

        # units display
        for a_unit in units_group:
            if a_unit.is_alive:
                a_unit.display(self.screen)

                #health bar display
                if ENABLE_HEALTH_BARS:
                    a_unit.display_life(self.screen)



        # buildings display
        for b in buildings:
            if b.is_alive:
                b.display(self.screen)

                if ENABLE_HEALTH_BARS:
                    b.display_life(self.screen)



        # MOUSE CURSOR - we disable the default one and create a new one at the current position of the mouse
        # MUST BE LAST TO SEE IT AND NOT BE HIDDEN BEHIND OTHER THINGS
        pygame.mouse.set_visible(False)
        standard_cursor_rect = standard_cursor.get_rect()
        standard_cursor_rect.center = pygame.mouse.get_pos()  # update position
        self.screen.blit(standard_cursor, standard_cursor_rect)  # draw the cursor

        # to refresh the screen and display things properly
#Draw FPS, must be the last to shown -> put it right on top of the display.flip
        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            (255,0,0),
            (10,10)
        )

        pygame.display.flip()

