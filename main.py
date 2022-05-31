import os
#os.environ["KIVY_AUDIO"] = "android"

from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
import random

########################################################################################################################
#############################################------TO DO-----###########################################################
########################################################################################################################
# make the buttons look more clickable, a little transparent, something like this
# push to github...
########################################################################################################################
########################################################################################################################

#Window.fullscreen = 'auto'
#Window.size = (710,1420)
#Window.size = (715,1430)
Window.size = (300,600)

#windows_sizes = Window.size

#print(Window.size)

# if windows_sizes[1] != 2 * windows_sizes[0]:
#     #print("not double")
#     Window.size = (windows_sizes[0],2*windows_sizes[0])
#else:
    #print("exactly double!")

#print(Window.size)

Builder.load_file('design.kv')

class MultiAudio:

    _next = 0

    def __init__(self, filename, count):
        self.buf = [SoundLoader.load(filename)
                    for _ in range(count)]

    def play(self, *args):
        self.buf[self._next].play()
        self._next = (self._next + 1) % len(self.buf)

    def stop(self,*args):
        self.buf[self._next].stop()
        #self._next = (self._next + 1) % len(self.buf)

class LBit(Widget):
    pass

class OBit(Widget):
    pass

class IBit(Widget):
    pass

class TBit(Widget):
    pass

class SBit(Widget):
    pass

class ZBit(Widget):
    pass

class JBit(Widget):
    pass

class Box(Widget):
    pass

class Wall(Widget):
    pass

class GameScreen(Screen):

    def on_pre_enter(self, *args):
        self.ids.my_game.ids.score_label.text = 'SCORE: 0'

class SecondScreen(Screen):

    highest_score_achieved = 0

    sound_bump_long_over = SoundLoader.load(filename='long_over_2.mp3')

    def on_pre_enter(self, *args):

        self.ids.my_label.text = f'HIGH SCORE:{self.highest_score_achieved}'

    def game_restart(self,*args):
        game_screen = self.manager.get_screen('game')
        my_game = game_screen.children[0]
        print(my_game.score)
        my_game.restart()
        self.parent.current = 'game'

    def on_enter(self, *args):
        self.sound_bump_long_over.play()
        self.sound_bump_long_over.loop = True
        pass

    def on_leave(self, *args):
        pass
        self.sound_bump_long_over.stop()

class Game(Widget):

    score = 0
    how_many_lines = 0
    ONE_LINE_CLEAR = 40
    TWO_LINE_CLEARS = 120
    THREE_LINE_CLEARS = 300
    FOUR_LINE_CLEARS = 1200

    NUMBER_OF_ROWS = 20
    NUMBER_OF_COLUMNS = 10

    SPACING = Window.size[0] / NUMBER_OF_COLUMNS
    BOX_WIDTH = (SPACING * 7)/2
    BOX_HEIGHT = (SPACING * 4)/2

    BOX_X = (Window.size[0]/2)-(BOX_WIDTH/2)
    BOX_Y = Window.size[1]*0.05 + SPACING

    LEFT_WALL_X = SPACING
    RIGHT_WALL_X = Window.size[0]-SPACING


    speed_fast = False

    next_shape_array = []
    NEXT_SHAPE_SCALING_FACTOR = 2
    SPEED_FACTOR_ARRAY = [1,1/10]
    speed_vertical = Window.size[1] /NUMBER_OF_ROWS
    SPEED_HORIZONTAL = Window.size[0]/NUMBER_OF_COLUMNS

    STARTING_X = Window.size[0]/2

    CUT_OFF_HEIGHT = (Window.size[0]/NUMBER_OF_COLUMNS)*4
    AFTER_WINNING_LINE_MOVE_TO = CUT_OFF_HEIGHT + SPACING
    Y_BOTTOM = AFTER_WINNING_LINE_MOVE_TO
    BLOCK_DROP_START_HEIGHT = Window.size[1] * 1
    #BLOCK_DROP_START_HEIGHT = AFTER_WINNING_LINE_MOVE_TO + 2 * SPACING

    active_array = []

    dead_array = []

    dead_array_top = []

    shapes_list = ['T','L','I','O','S','Z','J']
    #shapes_list = ['L']
    current_active_shape = random.choice(shapes_list)
    index = 0
    orientations = ['up','left','down','right']
    current_orientation = orientations[index]
    next_shape = []

    sound_bump_move = MultiAudio('rotate_4.mp3', 6)
    sound_bump_rotate = MultiAudio('rotate_4.mp3', 4)
    sound_bump_clear = MultiAudio('clear_3.mp3', 5)

    def create_left_wall(self,*args):
        self.left_wall = Wall()
        self.left_wall.size = Window.size[0]/self.NUMBER_OF_COLUMNS,Window.size[1]
        self.left_wall.pos = (0,self.CUT_OFF_HEIGHT)
        self.add_widget(self.left_wall)

    def create_bottom_wall(self, *args):
        self.bottom_wall = Wall()
        self.bottom_wall.size = Window.size[0], Window.size[0]/self.NUMBER_OF_COLUMNS
        self.bottom_wall.pos = (0, self.CUT_OFF_HEIGHT)
        self.add_widget(self.bottom_wall)

    def create_right_wall(self, *args):
        self.right_wall = Wall()
        self.right_wall.size = Window.size[0]/self.NUMBER_OF_COLUMNS, Window.size[1]
        self.right_wall.pos = (Window.size[0]-self.SPACING, self.CUT_OFF_HEIGHT)
        self.add_widget(self.right_wall)

    def create_BOX(self,*args):
        self.BOX = Box()
        self.BOX.size = (self.BOX_WIDTH,self.BOX_HEIGHT)
        self.BOX.pos = (self.BOX_X,self.BOX_Y)
        self.add_widget(self.BOX)

    def check_for_shape_release(self,*args):

        if self.active_array == []:

            if self.next_shape != []:

                choice = self.next_shape[0]

                if choice == 'L':
                    self.current_active_shape = 'L'
                    self.create_L_shape()

                elif choice == 'O':
                    self.current_active_shape = 'O'
                    self.create_O_shape()

                elif choice == 'I':
                    self.current_active_shape = 'I'
                    self.create_I_shape()

                elif choice == 'T':
                    self.current_active_shape = 'T'
                    self.create_T_shape()

                elif choice == 'S':
                    self.current_active_shape = 'S'
                    self.create_S_shape()

                elif choice == 'Z':
                    self.current_active_shape = 'Z'
                    self.create_Z_shape()

                elif choice == 'J':
                    self.current_active_shape = 'J'
                    self.create_J_shape()

                self.next_shape = []
                for bit in self.next_shape_array:
                    self.remove_widget(bit)

            else:

                if self.current_active_shape == 'L':
                    self.create_L_shape()

                elif self.current_active_shape == 'O':
                    self.create_O_shape()

                elif self.current_active_shape == 'I':
                    self.create_I_shape()

                elif self.current_active_shape == 'T':
                    self.create_T_shape()

                elif self.current_active_shape == 'S':
                    self.create_S_shape()

                elif self.current_active_shape == 'Z':
                    self.create_Z_shape()

                elif self.current_active_shape == 'J':
                    self.create_J_shape()

        else:

            if self.next_shape == []:
                self.next_shape.append(random.choice(self.shapes_list))


########################################################################################################################
########################################################################################################################
# SHAPE CREATIONS
########################################################################################################################
########################################################################################################################

    def show_next_shape(self,*args):

        #DO THIS FOR I later

        if self.next_shape != []:

            if self.next_shape[0] == 'L':

                start_x = (self.BOX_X + self.BOX_WIDTH / 2)-(self.SPACING/4)
                start_y = (self.BOX_Y + self.BOX_HEIGHT / 2)-(self.SPACING/2)

                factor = Window.size[0] / self.NUMBER_OF_COLUMNS/self.NEXT_SHAPE_SCALING_FACTOR

                # AXIS BIT, bit 0
                new_bit = LBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

                # bit_1, vertical
                new_bit = LBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x-factor,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)


                # bit 2, vertical
                new_bit = LBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x+factor,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)


                # bit 3 , horizontal
                new_bit = LBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x+factor,start_y+factor)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)


            elif self.next_shape[0] == 'O':

                start_x = (self.BOX_X + self.BOX_WIDTH/2)-self.SPACING/2
                start_y = (self.BOX_Y + self.BOX_HEIGHT/2)-self.SPACING/2

                factor = Window.size[0] / self.NUMBER_OF_COLUMNS/self.NEXT_SHAPE_SCALING_FACTOR

                # AXIS BIT, bit 0
                new_bit = OBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

                # bit_1, vertical
                new_bit = OBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x+factor,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)


                # bit 2, vertical
                new_bit = OBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x,start_y+factor)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)


                # bit 3 , horizontal
                new_bit = OBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x+factor,start_y+factor)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

            elif self.next_shape[0] == 'I':

                start_x = (self.BOX_X + self.BOX_WIDTH/2)-self.SPACING/2
                start_y = (self.BOX_Y + self.BOX_HEIGHT/2)-self.SPACING/4

                factor = Window.size[0] / self.NUMBER_OF_COLUMNS/self.NEXT_SHAPE_SCALING_FACTOR

                # AXIS BIT, bit 0
                new_bit = IBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

                # bit_1, vertical
                new_bit = IBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x-factor,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)


                # bit 2, vertical
                new_bit = IBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x+factor,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)


                # bit 3 , horizontal
                new_bit = IBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x+2*factor,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

            elif self.next_shape[0] == 'T':

                start_x = (self.BOX_X + self.BOX_WIDTH / 2)-(self.SPACING/4)
                start_y = (self.BOX_Y + self.BOX_HEIGHT / 2) -self.SPACING/2

                factor = Window.size[0] / self.NUMBER_OF_COLUMNS/self.NEXT_SHAPE_SCALING_FACTOR

                # AXIS BIT, bit 0
                new_bit = TBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

                # bit_1, vertical
                new_bit = TBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x-factor,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)


                # bit 2, vertical
                new_bit = TBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x+factor,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)


                # bit 3 , horizontal
                new_bit = TBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x,start_y+factor)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

            elif self.next_shape[0] == 'S':

                start_x = (self.BOX_X + self.BOX_WIDTH / 2)-(self.SPACING/4)
                start_y = (self.BOX_Y + self.BOX_HEIGHT / 2) -self.SPACING/2

                factor = Window.size[0] / self.NUMBER_OF_COLUMNS/self.NEXT_SHAPE_SCALING_FACTOR

                # AXIS BIT, bit 0
                new_bit = SBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

                # bit_1, vertical
                new_bit = SBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x-factor,start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)


                # bit 2, vertical
                new_bit = SBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x,start_y+factor)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)


                # bit 3 , horizontal
                new_bit = SBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x+factor,start_y+factor)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

            elif self.next_shape[0] == 'Z':
                start_x = (self.BOX_X + self.BOX_WIDTH / 2) - (self.SPACING / 4)
                start_y = (self.BOX_Y + self.BOX_HEIGHT / 2) - self.SPACING / 2

                factor = Window.size[0] / self.NUMBER_OF_COLUMNS / self.NEXT_SHAPE_SCALING_FACTOR

                # AXIS BIT, bit 0
                new_bit = ZBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x, start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

                # bit_1, vertical
                new_bit = ZBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x + factor, start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

                # bit 2, vertical
                new_bit = ZBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x, start_y + factor)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

                # bit 3 , horizontal
                new_bit = ZBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x - factor, start_y + factor)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

            elif self.next_shape[0] == 'J':
                start_x = (self.BOX_X + self.BOX_WIDTH / 2) - (self.SPACING / 4)
                start_y = (self.BOX_Y + self.BOX_HEIGHT / 2) - self.SPACING / 2

                factor = Window.size[0] / self.NUMBER_OF_COLUMNS / self.NEXT_SHAPE_SCALING_FACTOR

                # AXIS BIT, bit 0
                new_bit = JBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x, start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

                # bit_1, vertical
                new_bit = JBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x + factor, start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

                # bit 2, vertical
                new_bit = JBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x -factor, start_y)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

                # bit 3 , horizontal
                new_bit = JBit()
                new_bit.size = factor, factor
                new_bit.pos = (start_x - factor, start_y + factor)
                self.add_widget(new_bit)
                self.next_shape_array.append(new_bit)

    def create_L_shape(self,*args):

        y_starting_coordinate = self.BLOCK_DROP_START_HEIGHT
        x_starting_coordinate = self.STARTING_X
        starting_coordinates = (x_starting_coordinate, y_starting_coordinate)

        bit_array = []

        SPACING = Window.size[0] / self.NUMBER_OF_COLUMNS

        #AXIS BIT, bit 0
        new_bit = LBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0], starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        #bit_1, vertical
        new_bit = LBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0]-SPACING, starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        #bit 2, vertical
        new_bit = LBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0]+SPACING, starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 3 , horizontal
        new_bit = LBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0] + SPACING, starting_coordinates[1]+SPACING)
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        self.active_array.append(bit_array)

        self.index = (self.index + 1) % 4
        self.current_orientation = self.orientations[self.index]

    def create_O_shape(self,*args):

        y_starting_coordinate = self.BLOCK_DROP_START_HEIGHT
        x_starting_coordinate = self.STARTING_X
        starting_coordinates = (x_starting_coordinate, y_starting_coordinate)

        bit_array = []

        SPACING = Window.size[0] / self.NUMBER_OF_COLUMNS

        # bit_0
        new_bit = OBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0], starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 1
        new_bit = OBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0]+ 1 * SPACING, starting_coordinates[1] )
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 2
        new_bit = OBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0], starting_coordinates[1] + 1 * SPACING)
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 3
        new_bit = OBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0] + 1 * SPACING, starting_coordinates[1]+ 1 * SPACING)
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        self.active_array.append(bit_array)

        self.index = (self.index + 1) % 4
        self.current_orientation = self.orientations[self.index]


    def create_I_shape(self,*args):

        y_starting_coordinate = self.BLOCK_DROP_START_HEIGHT
        x_starting_coordinate = self.STARTING_X
        starting_coordinates = (x_starting_coordinate, y_starting_coordinate)

        bit_array = []

        SPACING = Window.size[0] / self.NUMBER_OF_COLUMNS

        # bit_0
        new_bit = IBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0], starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 1
        new_bit = IBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0]- 1 * SPACING, starting_coordinates[1] )
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 2
        new_bit = IBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0]+ 1 * SPACING, starting_coordinates[1] )
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 3
        new_bit = IBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0] + 2 * SPACING, starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        self.active_array.append(bit_array)

        self.index = (self.index + 1) % 4
        self.current_orientation = self.orientations[self.index]



    def create_T_shape(self,*args):

        y_starting_coordinate = self.BLOCK_DROP_START_HEIGHT
        x_starting_coordinate = self.STARTING_X
        starting_coordinates = (x_starting_coordinate, y_starting_coordinate)

        bit_array = []

        SPACING = Window.size[0] / self.NUMBER_OF_COLUMNS

        # bit_0
        new_bit = TBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0], starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 1
        new_bit = TBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0]- 1 * SPACING, starting_coordinates[1] )
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 2
        new_bit = TBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0]+ 1 * SPACING, starting_coordinates[1] )
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 3
        new_bit = TBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0], starting_coordinates[1]+SPACING)
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        self.active_array.append(bit_array)

        self.index = (self.index + 1) % 4
        self.current_orientation = self.orientations[self.index]


    def create_S_shape(self,*args):

        y_starting_coordinate = self.BLOCK_DROP_START_HEIGHT
        x_starting_coordinate = self.STARTING_X
        starting_coordinates = (x_starting_coordinate, y_starting_coordinate)

        bit_array = []

        SPACING = Window.size[0] / self.NUMBER_OF_COLUMNS

        #AXIS BIT, bit 0
        new_bit = SBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0], starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        #bit_1, vertical
        new_bit = SBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0]-SPACING, starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        #bit 2, vertical
        new_bit = SBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0], starting_coordinates[1] + SPACING)
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 3 , horizontal
        new_bit = SBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0] + 1 * SPACING, starting_coordinates[1]+SPACING)
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        self.active_array.append(bit_array)

        self.index = (self.index + 1) % 4
        self.current_orientation = self.orientations[self.index]

    def create_Z_shape(self,*args):

        y_starting_coordinate = self.BLOCK_DROP_START_HEIGHT
        x_starting_coordinate = self.STARTING_X
        starting_coordinates = (x_starting_coordinate, y_starting_coordinate)

        bit_array = []

        SPACING = Window.size[0] / self.NUMBER_OF_COLUMNS

        #AXIS BIT, bit 0
        new_bit = ZBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0], starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        #bit_1, vertical
        new_bit = ZBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0]+SPACING, starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        #bit 2, vertical
        new_bit = ZBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0], starting_coordinates[1] + SPACING)
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 3 , horizontal
        new_bit = ZBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0] - 1 * SPACING, starting_coordinates[1]+SPACING)
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        self.active_array.append(bit_array)

        self.index = (self.index + 1) % 4
        self.current_orientation = self.orientations[self.index]

    def create_J_shape(self,*args):

        y_starting_coordinate = self.BLOCK_DROP_START_HEIGHT
        x_starting_coordinate = self.STARTING_X
        starting_coordinates = (x_starting_coordinate, y_starting_coordinate)

        bit_array = []

        SPACING = Window.size[0] / self.NUMBER_OF_COLUMNS

        #AXIS BIT, bit 0
        new_bit = JBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0], starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        #bit_1, vertical
        new_bit = JBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0]+SPACING, starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        #bit 2, vertical
        new_bit = JBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0]-SPACING, starting_coordinates[1])
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        # bit 3 , horizontal
        new_bit = JBit()
        new_bit.size = Window.size[0] / self.NUMBER_OF_COLUMNS, Window.size[0] / self.NUMBER_OF_COLUMNS
        new_bit.pos = (starting_coordinates[0] - 1 * SPACING, starting_coordinates[1]+SPACING)
        self.add_widget(new_bit)
        bit_array.append(new_bit)

        self.active_array.append(bit_array)

        self.index = (self.index + 1) % 4
        self.current_orientation = self.orientations[self.index]

########################################################################################################################
########################################################################################################################
# END SHAPE CREATIONS
########################################################################################################################
########################################################################################################################








########################################################################################################################
########################################################################################################################
# SHAPE TRANSLATIONS:DOWN, LEFT, RIGHT
########################################################################################################################
########################################################################################################################

    def move_shape_right(self, *args):

        self.sound_bump_move.play()

        keep_moving_all_bits = True

        even_one_collision = False

        for shape in self.active_array:
            shape = sorted(shape, key=lambda x: x.pos[0],reverse=True)

            for bit in shape:
                for dead_bit in self.dead_array:
                    if (bit.pos[1] == dead_bit.pos[1]) and (bit.pos[0] + self.SPACING == dead_bit.pos[0]):
                        keep_moving_all_bits = False

            if keep_moving_all_bits:
                for bit in shape:
                    if not even_one_collision:
                        if bit.collide_widget(self.right_wall) == False:

                            bit.pos[0] += self.SPEED_HORIZONTAL
                        else:
                            even_one_collision = True


    def move_shape_left(self, *args):

        self.sound_bump_move.play()

        keep_moving_all_bits = True

        even_one_collision = False

        for shape in self.active_array:
            shape = sorted(shape, key=lambda x: x.pos[0])

            for bit in shape:
                for dead_bit in self.dead_array:
                    if (bit.pos[1] == dead_bit.pos[1]) and (bit.pos[0] - self.SPACING == dead_bit.pos[0]):
                        keep_moving_all_bits = False

            if keep_moving_all_bits:
                for bit in shape:
                    if not even_one_collision:
                        if bit.collide_widget(self.left_wall) == False:

                            bit.pos[0] -= self.SPEED_HORIZONTAL
                        else:
                            even_one_collision = True


    def change_speed(self,*args):

        if self.ids.accelerate_button.state == 'down':
            self.speed_fast = True
        else:
            self.speed_fast = False

        if self.speed_fast:
            Clock.unschedule(self.move_shape_down)
            Clock.schedule_interval(self.move_shape_down, self.SPEED_FACTOR_ARRAY[1])

        else:
            Clock.unschedule(self.move_shape_down)
            Clock.schedule_interval(self.move_shape_down, self.SPEED_FACTOR_ARRAY[0])


    def move_shape_down(self, *args):

        #sound_bump_hit = MultiAudio('hit_1.mp3',1)

        self.change_speed()

        check_bottom_wall = True
        keep_moving_all_bits = True


        for shape in self.active_array:
            shape = sorted(shape, key=lambda x: x.pos[1])

            for bit in shape:
                for dead_bit in self.dead_array:
                    if (bit.pos[0] == dead_bit.pos[0]) and (bit.pos[1]-self.SPACING==dead_bit.pos[1]):
                        keep_moving_all_bits = False
                        check_bottom_wall = False

            if keep_moving_all_bits:
                for bit in shape:
                    bit.pos[1] -= self.speed_vertical
            else:
                for bit in shape:
                    self.dead_array.append(bit)
                #sound_bump_hit.play()
                self.active_array = []
                self.index = 0
                self.current_orientation = self.orientations[self.index]

        if check_bottom_wall:

            even_one_collision = False

            for shape in self.active_array:

                shape = sorted(shape,key=lambda x:x.pos[1])

                for bit in shape:
                    if not even_one_collision:
                        if bit.collide_widget(self.bottom_wall) == True:
                            even_one_collision = True

                if even_one_collision:
                    #sound_bump_hit.play()
                    self.active_array = []
                    self.index = 0
                    self.current_orientation = self.orientations[self.index]
                    for bit in shape:
                        self.dead_array.append(bit)

    def move_dead_bits_down(self,*args):

        self.dead_array_top = sorted(self.dead_array_top,key=lambda x:x.pos[1])

        all_x_positions = []

        for bit in self.dead_array:
            all_x_positions.append(bit.pos[0])

        all_x_positions = list(set(all_x_positions))
        all_x_positions = sorted(all_x_positions)

        columns_of_x = [[] for _ in range(len(all_x_positions))]

        for i in range(len(all_x_positions)):
            for bit in self.dead_array:
                if bit.pos[0] == all_x_positions[i]:
                    columns_of_x[i].append(bit)

        highest_y = []

        for i in range(len(columns_of_x)):
            max_y = 0
            for bit in columns_of_x[i]:
                if bit.pos[1] > max_y:
                    max_y = bit.pos[1]
            highest_y.append(max_y)

        uppermost_dead_bits = []
        for i in range(len(columns_of_x)):
            for bit in columns_of_x[i]:
                if bit.pos[1] == highest_y[i]:
                    uppermost_dead_bits.append(bit)


        lowest_y = 1000000
        for bit in self.dead_array_top:
            if bit.pos[1] < lowest_y:
                lowest_y = bit.pos[1]

        where_to_move_to = []

        for bit in self.dead_array_top:
            move_to_bottom = True
            for upper_bit in uppermost_dead_bits:
                if bit.pos[0] == upper_bit.pos[0]:
                    move_to_bottom = False
                    move_to = upper_bit.pos[1]+\
                                       (bit.pos[1]-lowest_y)+self.SPACING
                    where_to_move_to.append(upper_bit.pos[1]+\
                                       (bit.pos[1]-lowest_y)+self.SPACING)
                    bit.pos[1] = move_to

            if move_to_bottom:
                move_to = self.AFTER_WINNING_LINE_MOVE_TO + (bit.pos[1]-lowest_y)
                where_to_move_to.append(self.AFTER_WINNING_LINE_MOVE_TO +(bit.pos[1]-lowest_y))
                bit.pos[1] = move_to


        for top_bit in self.dead_array_top:
            self.dead_array.append(top_bit)

        self.dead_array_top = []


########################################################################################################################
########################################################################################################################
# END SHAPE TRANSLATIONS
########################################################################################################################
########################################################################################################################

    def rotate_piece(self, *args):

        self.sound_bump_rotate.play()

        for shape in self.active_array:

            if self.current_active_shape == 'L':

                self.rotate_L(shape)

            elif self.current_active_shape == 'O':


                self.rotate_O(shape)

            elif self.current_active_shape == 'I':


                self.rotate_I(shape)

            elif self.current_active_shape == 'T':


                self.rotate_T(shape)

            elif self.current_active_shape == 'S':


                self.rotate_S(shape)

            elif self.current_active_shape == 'Z':


                self.rotate_Z(shape)

            elif self.current_active_shape == 'J':


                self.rotate_J(shape)



########################################################################################################################
########################################################################################################################
# ROTATIONS
########################################################################################################################
########################################################################################################################
    def rotate_L(self, shape):

        axis_bit = shape[0]

        array_of_danger_zones = [['left', self.AFTER_WINNING_LINE_MOVE_TO + self.SPACING]]

        factor = self.SPACING

        new_axis_x_OG = [axis_bit.pos[0] - factor, axis_bit.pos[0] + factor]

        if self.current_orientation == 'up':

            bit_1_x = axis_bit.pos[0] - factor
            bit_1_y = axis_bit.pos[1]

            bit_2_x = axis_bit.pos[0] + factor
            bit_2_y = axis_bit.pos[1]

            bit_3_x = axis_bit.pos[0] + factor
            bit_3_y = axis_bit.pos[1] + factor

            modify_x_1 = -factor
            modify_y_1 = 0

            modify_x_2 = factor
            modify_y_2 = 0

            modify_x_3 = factor
            modify_y_3 = factor

            #print("PREVIOUS RIGHT -----> CURRENT UP!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y,shape,modify_x_1,modify_y_1,
                                 modify_x_2,modify_y_2,modify_x_3,modify_y_3,array_of_danger_zones,new_axis_x_OG)
######################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        elif self.current_orientation == 'left':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] + factor


            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] - factor


            bit_3_x = axis_bit.pos[0] + factor
            bit_3_y = axis_bit.pos[1] - factor


            modify_x_1 = 0
            modify_y_1 = factor

            modify_x_2 = 0
            modify_y_2 = -factor

            modify_x_3 = factor
            modify_y_3 = -factor

            #print("PREVIOUS UP ------> CURRENT LEFT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                 modify_x_2, modify_y_2, modify_x_3, modify_y_3,array_of_danger_zones,new_axis_x_OG)
#############################################################################################################################
#############################################################################################################################

        elif self.current_orientation == 'down':

            bit_1_x = axis_bit.pos[0] + factor
            bit_1_y = axis_bit.pos[1]


            bit_2_x = axis_bit.pos[0] - factor
            bit_2_y = axis_bit.pos[1]


            bit_3_x = axis_bit.pos[0] - factor
            bit_3_y = axis_bit.pos[1] - factor

            modify_x_1 = factor
            modify_y_1 = 0

            modify_x_2 = -factor
            modify_y_2 = 0

            modify_x_3 = -factor
            modify_y_3 = -factor

            #print("PREVIOUS LEFT -----> CURRENT DOWN!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                 modify_x_2, modify_y_2, modify_x_3, modify_y_3,array_of_danger_zones,new_axis_x_OG)

#############################################################################################################################
#############################################################################################################################

        elif self.current_orientation == 'right':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] - factor


            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] + factor


            bit_3_x = axis_bit.pos[0] - factor
            bit_3_y = axis_bit.pos[1] + factor

            modify_x_1 = 0
            modify_y_1 = -factor

            modify_x_2 = 0
            modify_y_2 = factor

            modify_x_3 = -factor
            modify_y_3 = factor

            #print("PREVIOUS DOWN -------> CURRENT RIGHT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                 modify_x_2, modify_y_2, modify_x_3, modify_y_3,array_of_danger_zones,new_axis_x_OG)

#############################################################################################################################
#############################################################################################################################


    def repititive_code_L(self,bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y,shape,modify_x_1,modify_y_1,
                                 modify_x_2,modify_y_2,modify_x_3,modify_y_3,array_of_danger_zones,new_axis_x_OG):

        ok_rotation_to_future_state = True

        axis_bit = shape[0]
        bit_1 = shape[1]
        bit_2 = shape[2]
        bit_3 = shape[3]

        # print(f"current axis coordinates:{axis_bit.pos}")
        # print(f"current shape orientation:{self.current_orientation}")
        # print(f"my array of danger zones: {array_of_danger_zones}")

        for array in array_of_danger_zones:
            if self.current_orientation == array[0] and axis_bit.pos[1]==array[1]:
                #print("DANGER ZONE!!!")
                axis_bit.pos[1] += self.SPACING
                #bit_1_x =
                bit_1_y += self.SPACING
                #bit_2_x =
                bit_2_y = self.SPACING
                #bit_3_x =
                bit_3_y = self.SPACING

        bit_1_future = [bit_1_x, bit_1_y]
        bit_2_future = [bit_2_x, bit_2_y]
        bit_3_future = [bit_3_x, bit_3_y]

        future_array = [bit_1_future, bit_2_future, bit_3_future]

        factor = self.SPACING

        # +self.SPACING
        #FOR THAT STRANGE CASE... LATER...

        for future_bit in future_array:

            if (future_bit[0] < self.LEFT_WALL_X or future_bit[0] >= self.RIGHT_WALL_X) or \
                    (future_bit[1] < self.Y_BOTTOM):
                ok_rotation_to_future_state = False
                break

            for dead_bit in self.dead_array:
                if future_bit[0] == dead_bit.pos[0] and future_bit[1] == dead_bit.pos[1]:
                    ok_rotation_to_future_state = False
                    break

        if ok_rotation_to_future_state:
            bit_1.pos[0] = bit_1_x
            bit_1.pos[1] = bit_1_y

            bit_2.pos[0] = bit_2_x
            bit_2.pos[1] = bit_2_y

            bit_3.pos[0] = bit_3_x
            bit_3.pos[1] = bit_3_y

            self.index = (self.index + 1) % 4
            self.current_orientation = self.orientations[self.index]

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        else:

            #print("rotation barred!")

            #
            new_axis_x = new_axis_x_OG

            new_axis_x_position = 0

            #already_found_suitable_position = False
            for new_x in new_axis_x:

                entered_1 = False
                entered_2 = False

                #print("entered")
                #print(f"axis currently being tested = {new_x,axis_bit.pos[1]}")

                bit_1_x = new_x + modify_x_1
                bit_1_y = axis_bit.pos[1] + modify_y_1
                bit_1_future = [bit_1_x, bit_1_y]

                bit_2_x = new_x + modify_x_2
                bit_2_y = axis_bit.pos[1] + modify_y_2
                bit_2_future = [bit_2_x, bit_2_y]

                bit_3_x = new_x + modify_x_3
                bit_3_y = axis_bit.pos[1] + modify_y_3
                bit_3_future = [bit_3_x, bit_3_y]

                future_array = [bit_1_future, bit_2_future, bit_3_future]

                # +self.SPACING
                for future_bit in future_array:

                    #print(f"future bit location:{future_bit[0], future_bit[1]}")
                    if (future_bit[0] < self.LEFT_WALL_X or future_bit[0] >= self.RIGHT_WALL_X) or \
                            (future_bit[1] < self.Y_BOTTOM):
                        #print("entered first stage")
                        entered_1 = True

                    if self.dead_array != []:
                        #print("checking dead array")
                        for dead_bit in self.dead_array:
                            #print(f'dead bit:{dead_bit.pos}',end=',')
                            #print()

                            if new_x == dead_bit.pos[0] and axis_bit.pos[1] == dead_bit.pos[1]:
                                #print("entered 2nd stage for axis bit!")
                                entered_2 = True
                            if (future_bit[0] == dead_bit.pos[0]) and (future_bit[1] == dead_bit.pos[1]):
                                #print("entered 2nd stage for bit 1,2 or 3")
                                entered_2 = True

                if entered_1 == False and entered_2 == False:
                    new_axis_x_position = new_x
                    #already_found_suitable_position = True
                    #print("found suitable position!")
                    break

            #if already_found_suitable_position:
            if new_axis_x_position != 0:
                axis_bit.pos[0] = new_axis_x_position
                #print(axis_bit.pos[0])

                bit_1.pos[0] = axis_bit.pos[0] + modify_x_1
                bit_1.pos[1] = axis_bit.pos[1] + modify_y_1

                bit_2.pos[0] = axis_bit.pos[0] + modify_x_2
                bit_2.pos[1] = axis_bit.pos[1] + modify_y_2

                bit_3.pos[0] = axis_bit.pos[0] + modify_x_3
                bit_3.pos[1] = axis_bit.pos[1] + modify_y_3

                #print(f"new bits at: {axis_bit.pos,bit_1.pos,bit_2.pos,bit_3.pos}")

                self.index = (self.index + 1) % 4
                self.current_orientation = self.orientations[self.index]









########################################################################################################################

    def rotate_I(self, shape):

        axis_bit = shape[0]

        array_of_danger_zones = [['left',self.AFTER_WINNING_LINE_MOVE_TO+2*self.SPACING],
                                 ['right',self.AFTER_WINNING_LINE_MOVE_TO+self.SPACING]]

        factor = self.SPACING

        new_axis_x_OG = [axis_bit.pos[0] - factor, axis_bit.pos[0] + factor, axis_bit.pos[0]+2*factor,axis_bit.pos[0]-2*factor]

        if self.current_orientation == 'up':

            bit_1_x = axis_bit.pos[0] - factor
            bit_1_y = axis_bit.pos[1]

            bit_2_x = axis_bit.pos[0] + factor
            bit_2_y = axis_bit.pos[1]

            bit_3_x = axis_bit.pos[0] + 2 * factor
            bit_3_y = axis_bit.pos[1]

            modify_x_1 = -factor
            modify_y_1 = 0

            modify_x_2 = factor
            modify_y_2 = 0

            modify_x_3 = 2 * factor
            modify_y_3 = 0

            #print("PREVIOUS RIGHT -----> CURRENT UP!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3,array_of_danger_zones,new_axis_x_OG)
        ######################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        elif self.current_orientation == 'left':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] + factor

            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] - factor

            bit_3_x = axis_bit.pos[0]
            bit_3_y = axis_bit.pos[1] - 2 * factor

            modify_x_1 = 0
            modify_y_1 = factor

            modify_x_2 = 0
            modify_y_2 = -factor

            modify_x_3 = 0
            modify_y_3 = -2*factor

            #print("PREVIOUS UP ------> CURRENT LEFT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3,array_of_danger_zones,new_axis_x_OG)
        #############################################################################################################################
        #############################################################################################################################

        elif self.current_orientation == 'down':

            bit_1_x = axis_bit.pos[0] + factor
            bit_1_y = axis_bit.pos[1]

            bit_2_x = axis_bit.pos[0] - factor
            bit_2_y = axis_bit.pos[1]

            bit_3_x = axis_bit.pos[0] -2 * factor
            bit_3_y = axis_bit.pos[1]

            modify_x_1 = factor
            modify_y_1 = 0

            modify_x_2 = -factor
            modify_y_2 = 0

            modify_x_3 = -2*factor
            modify_y_3 = 0

            #print("PREVIOUS LEFT -----> CURRENT DOWN!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3,array_of_danger_zones,new_axis_x_OG)

        #############################################################################################################################
        #############################################################################################################################

        elif self.current_orientation == 'right':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] - factor

            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] + factor

            bit_3_x = axis_bit.pos[0]
            bit_3_y = axis_bit.pos[1] + 2 * factor

            modify_x_1 = 0
            modify_y_1 = -factor

            modify_x_2 = 0
            modify_y_2 = factor

            modify_x_3 = 0
            modify_y_3 = 2*factor

            #print("PREVIOUS DOWN -------> CURRENT RIGHT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3,array_of_danger_zones,new_axis_x_OG)

    def rotate_T(self, shape):

        axis_bit = shape[0]


        #array_of_danger_zones = []
        array_of_danger_zones = [['left',self.AFTER_WINNING_LINE_MOVE_TO + self.SPACING]]

        factor = self.SPACING

        new_axis_x_OG = [axis_bit.pos[0] - factor, axis_bit.pos[0] + factor]

        if self.current_orientation == 'up':

            bit_1_x = axis_bit.pos[0] - factor
            bit_1_y = axis_bit.pos[1]

            bit_2_x = axis_bit.pos[0] + factor
            bit_2_y = axis_bit.pos[1]

            bit_3_x = axis_bit.pos[0]
            bit_3_y = axis_bit.pos[1] + factor

            modify_x_1 = -factor
            modify_y_1 = 0

            modify_x_2 = factor
            modify_y_2 = 0

            modify_x_3 = 0
            modify_y_3 = factor

            #print("PREVIOUS RIGHT -----> CURRENT UP!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)
        ######################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        elif self.current_orientation == 'left':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] + factor

            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] - factor

            bit_3_x = axis_bit.pos[0] + factor
            bit_3_y = axis_bit.pos[1]

            modify_x_1 = 0
            modify_y_1 = factor

            modify_x_2 = 0
            modify_y_2 = -factor

            modify_x_3 = factor
            modify_y_3 = 0

            #print("PREVIOUS UP ------> CURRENT LEFT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)
        #############################################################################################################################
        #############################################################################################################################

        elif self.current_orientation == 'down':

            bit_1_x = axis_bit.pos[0] + factor
            bit_1_y = axis_bit.pos[1]

            bit_2_x = axis_bit.pos[0] - factor
            bit_2_y = axis_bit.pos[1]

            bit_3_x = axis_bit.pos[0]
            bit_3_y = axis_bit.pos[1] - factor

            modify_x_1 = factor
            modify_y_1 = 0

            modify_x_2 = -factor
            modify_y_2 = 0

            modify_x_3 = 0
            modify_y_3 = -factor

            #print("PREVIOUS LEFT -----> CURRENT DOWN!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)

        #############################################################################################################################
        #############################################################################################################################

        elif self.current_orientation == 'right':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] - factor

            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] + factor

            bit_3_x = axis_bit.pos[0] - factor
            bit_3_y = axis_bit.pos[1]

            modify_x_1 = 0
            modify_y_1 = -factor

            modify_x_2 = 0
            modify_y_2 = factor

            modify_x_3 = -factor
            modify_y_3 = 0

            #print("PREVIOUS DOWN -------> CURRENT RIGHT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)


    def rotate_O(self, shape):
        pass

    def rotate_S(self, shape):

        axis_bit = shape[0]

        #array_of_danger_zones = []
        array_of_danger_zones = [['left', self.AFTER_WINNING_LINE_MOVE_TO + self.SPACING]]

        factor = self.SPACING

        new_axis_x_OG = [axis_bit.pos[0] - factor, axis_bit.pos[0] + factor]

        if self.current_orientation == 'up':

            bit_1_x = axis_bit.pos[0] - factor
            bit_1_y = axis_bit.pos[1]

            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] + factor

            bit_3_x = axis_bit.pos[0] + factor
            bit_3_y = axis_bit.pos[1] + factor

            modify_x_1 = -factor
            modify_y_1 = 0

            modify_x_2 = 0
            modify_y_2 = factor

            modify_x_3 = factor
            modify_y_3 = factor

            #print("PREVIOUS RIGHT -----> CURRENT UP!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)
        ######################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        elif self.current_orientation == 'left':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] + factor

            bit_2_x = axis_bit.pos[0] + factor
            bit_2_y = axis_bit.pos[1]

            bit_3_x = axis_bit.pos[0] + factor
            bit_3_y = axis_bit.pos[1] - factor

            modify_x_1 = 0
            modify_y_1 = factor

            modify_x_2 = factor
            modify_y_2 = 0

            modify_x_3 = factor
            modify_y_3 = -factor

            #print("PREVIOUS UP ------> CURRENT LEFT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)
        #############################################################################################################################
        #############################################################################################################################

        elif self.current_orientation == 'down':

            bit_1_x = axis_bit.pos[0] + factor
            bit_1_y = axis_bit.pos[1]

            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] - factor

            bit_3_x = axis_bit.pos[0] - factor
            bit_3_y = axis_bit.pos[1] - factor

            modify_x_1 = factor
            modify_y_1 = 0

            modify_x_2 = 0
            modify_y_2 = -factor

            modify_x_3 = -factor
            modify_y_3 = -factor

            #print("PREVIOUS LEFT -----> CURRENT DOWN!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)

        #############################################################################################################################
        #############################################################################################################################

        elif self.current_orientation == 'right':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] - factor

            bit_2_x = axis_bit.pos[0] - factor
            bit_2_y = axis_bit.pos[1]

            bit_3_x = axis_bit.pos[0] - factor
            bit_3_y = axis_bit.pos[1] + factor

            modify_x_1 = 0
            modify_y_1 = -factor

            modify_x_2 = -factor
            modify_y_2 = 0

            modify_x_3 = -factor
            modify_y_3 = factor

            #print("PREVIOUS DOWN -------> CURRENT RIGHT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)


    def rotate_Z(self, shape):

        axis_bit = shape[0]

        #array_of_danger_zones = []
        array_of_danger_zones = [['left', self.AFTER_WINNING_LINE_MOVE_TO + self.SPACING]]

        factor = self.SPACING

        new_axis_x_OG = [axis_bit.pos[0] - factor, axis_bit.pos[0] + factor]

        if self.current_orientation == 'up':

            bit_1_x = axis_bit.pos[0] + factor
            bit_1_y = axis_bit.pos[1]

            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] + factor

            bit_3_x = axis_bit.pos[0] - factor
            bit_3_y = axis_bit.pos[1] + factor

            modify_x_1 = factor
            modify_y_1 = 0

            modify_x_2 = 0
            modify_y_2 = factor

            modify_x_3 = -factor
            modify_y_3 = factor

            #print("PREVIOUS RIGHT -----> CURRENT UP!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)
        ######################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        elif self.current_orientation == 'left':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] - factor

            bit_2_x = axis_bit.pos[0] + factor
            bit_2_y = axis_bit.pos[1]

            bit_3_x = axis_bit.pos[0] + factor
            bit_3_y = axis_bit.pos[1] + factor

            modify_x_1 = 0
            modify_y_1 = -factor

            modify_x_2 = factor
            modify_y_2 = 0

            modify_x_3 = factor
            modify_y_3 = factor

            #print("PREVIOUS UP ------> CURRENT LEFT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)
        #############################################################################################################################
        #############################################################################################################################

        elif self.current_orientation == 'down':

            bit_1_x = axis_bit.pos[0] - factor
            bit_1_y = axis_bit.pos[1]

            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] - factor

            bit_3_x = axis_bit.pos[0] + factor
            bit_3_y = axis_bit.pos[1] - factor

            modify_x_1 = -factor
            modify_y_1 = 0

            modify_x_2 = 0
            modify_y_2 = -factor

            modify_x_3 = factor
            modify_y_3 = -factor

            #print("PREVIOUS LEFT -----> CURRENT DOWN!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)

        #############################################################################################################################
        #############################################################################################################################

        elif self.current_orientation == 'right':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] + factor

            bit_2_x = axis_bit.pos[0] - factor
            bit_2_y = axis_bit.pos[1]

            bit_3_x = axis_bit.pos[0] - factor
            bit_3_y = axis_bit.pos[1] - factor

            modify_x_1 = 0
            modify_y_1 = factor

            modify_x_2 = -factor
            modify_y_2 = 0

            modify_x_3 = -factor
            modify_y_3 = -factor

            #print("PREVIOUS DOWN -------> CURRENT RIGHT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)
########################################################################################################################
########################################################################################################################
    def rotate_J(self, shape):

        axis_bit = shape[0]

        # array_of_danger_zones = []
        array_of_danger_zones = [['left', self.AFTER_WINNING_LINE_MOVE_TO + self.SPACING]]

        factor = self.SPACING

        new_axis_x_OG = [axis_bit.pos[0] - factor, axis_bit.pos[0] + factor]

        if self.current_orientation == 'up':

            bit_1_x = axis_bit.pos[0] + factor
            bit_1_y = axis_bit.pos[1]

            bit_2_x = axis_bit.pos[0] - factor
            bit_2_y = axis_bit.pos[1]

            bit_3_x = axis_bit.pos[0] - factor
            bit_3_y = axis_bit.pos[1] + factor

            modify_x_1 = factor
            modify_y_1 = 0

            modify_x_2 = -factor
            modify_y_2 = 0

            modify_x_3 = -factor
            modify_y_3 = factor

            #print("PREVIOUS RIGHT -----> CURRENT UP!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)
        ######################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        elif self.current_orientation == 'left':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] - factor

            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] + factor

            bit_3_x = axis_bit.pos[0] + factor
            bit_3_y = axis_bit.pos[1] + factor

            modify_x_1 = 0
            modify_y_1 = -factor

            modify_x_2 = 0
            modify_y_2 = factor

            modify_x_3 = factor
            modify_y_3 = factor

            #print("PREVIOUS UP ------> CURRENT LEFT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)
        #############################################################################################################################
        #############################################################################################################################

        elif self.current_orientation == 'down':

            bit_1_x = axis_bit.pos[0] - factor
            bit_1_y = axis_bit.pos[1]

            bit_2_x = axis_bit.pos[0] + factor
            bit_2_y = axis_bit.pos[1]

            bit_3_x = axis_bit.pos[0] + factor
            bit_3_y = axis_bit.pos[1] - factor

            modify_x_1 = -factor
            modify_y_1 = 0

            modify_x_2 = factor
            modify_y_2 = 0

            modify_x_3 = factor
            modify_y_3 = -factor

            #print("PREVIOUS LEFT -----> CURRENT DOWN!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)

        #############################################################################################################################
        #############################################################################################################################

        elif self.current_orientation == 'right':

            bit_1_x = axis_bit.pos[0]
            bit_1_y = axis_bit.pos[1] + factor

            bit_2_x = axis_bit.pos[0]
            bit_2_y = axis_bit.pos[1] - factor

            bit_3_x = axis_bit.pos[0] - factor
            bit_3_y = axis_bit.pos[1] - factor

            modify_x_1 = 0
            modify_y_1 = factor

            modify_x_2 = 0
            modify_y_2 = -factor

            modify_x_3 = -factor
            modify_y_3 = -factor

            #print("PREVIOUS DOWN -------> CURRENT RIGHT!!!")
            self.repititive_code_L(bit_1_x, bit_1_y, bit_2_x, bit_2_y, bit_3_x, bit_3_y, shape, modify_x_1, modify_y_1,
                                   modify_x_2, modify_y_2, modify_x_3, modify_y_3, array_of_danger_zones, new_axis_x_OG)


########################################################################################################################
########################################################################################################################
# END ROTATIONS
########################################################################################################################
########################################################################################################################

    def arrays_columns_dead_bits(self,*args):

        continue_on = False

        removed_row_num = 0

        #make an array that has the same number of rows as the current board state

        array_all_y = []

        for bit in self.dead_array:
            array_all_y.append(bit.pos[1])

        set_all_y = list(set(array_all_y))

        set_all_y = sorted(set_all_y)

        number_of_rows = len(set_all_y)

        self.my_sorted_array = [[] for _ in range(number_of_rows)]

        #for every bit, put it into a row according to it's y coordinate

        for bit in self.dead_array:
            bit_y = bit.pos[1]
            for y in range(number_of_rows):
                if bit_y == set_all_y[y]:
                    self.my_sorted_array[y].append(bit)


        for row in self.my_sorted_array:
            if len(row) == self.NUMBER_OF_COLUMNS-2:
                self.sound_bump_clear.play()
                self.how_many_lines += 1
                for bit in row:
                    self.remove_widget(bit)
                    self.dead_array.remove(bit)
                    #only the bits that were above will actually move
                    #store the removed row as a variable
                    continue_on = True
                    removed_row_num = self.my_sorted_array.index(row)




        if self.how_many_lines == 1:
            self.score += self.ONE_LINE_CLEAR

        elif self.how_many_lines == 2:
            self.score += self.TWO_LINE_CLEARS

        elif self.how_many_lines == 3:
            self.score += self.THREE_LINE_CLEARS

        elif self.how_many_lines == 4:
            self.score += self.FOUR_LINE_CLEARS


        self.ids.score_label.text = f"SCORE: {self.score}"

        #now do a for loop to append the top array

        if continue_on:

            for x in range(len(self.my_sorted_array)):

                if x > removed_row_num:

                    for bit in self.my_sorted_array[x]:
                        self.dead_array.remove(bit)
                        self.dead_array_top.append(bit)

        #reset how many lines
        self.how_many_lines = 0


    def check_defeat(self,*args):

        sorted_array = sorted(self.dead_array,key=lambda x:x.pos[1],reverse=True)

        if sorted_array != []:

            bit_with_highest_y_value = sorted_array[0]

            highest_y_value = bit_with_highest_y_value.pos[1]

            if highest_y_value >= Window.size[1]-self.SPACING:

                final_high_score = self.score

                self.reset()

                defeat_screen = self.parent.manager.get_screen('second')

                if final_high_score > defeat_screen.highest_score_achieved:
                    defeat_screen.highest_score_achieved = final_high_score

                self.parent.parent.current = 'second'


    def on_size(self, *args):

        self.sound_track = SoundLoader.load(filename='8bit_4.m4a')
        self.sound_track.play()
        self.sound_track.loop = True
        self.ids.score_label.text = f"SCORE: {self.score}"

        self.create_left_wall()
        self.create_bottom_wall()
        self.create_right_wall()
        self.create_BOX()

        Clock.schedule_interval(self.check_for_shape_release,1)
        Clock.schedule_interval(self.move_shape_down, self.SPEED_FACTOR_ARRAY[0])
        Clock.schedule_interval(self.move_dead_bits_down, 1)
        Clock.schedule_interval(self.show_next_shape,1)
        Clock.schedule_interval(self.arrays_columns_dead_bits, 1)
        Clock.schedule_interval(self.check_defeat,1)

    def reset(self,*args):

        self.score = 0

        self.sound_track.stop()

        for dead_bit in self.dead_array:
            self.remove_widget(dead_bit)

        for bit in self.active_array:
            self.remove_widget(bit)

        Clock.unschedule(self.check_for_shape_release)
        Clock.unschedule(self.move_shape_down)
        Clock.unschedule(self.move_dead_bits_down)
        Clock.unschedule(self.show_next_shape)
        Clock.unschedule(self.arrays_columns_dead_bits)
        Clock.unschedule(self.check_defeat)

        self.how_many_lines = 0
        self.ONE_LINE_CLEAR = 40
        self.TWO_LINE_CLEARS = 120
        self.THREE_LINE_CLEARS = 300
        self.FOUR_LINE_CLEARS = 1200

        self.NUMBER_OF_ROWS = 20
        self.NUMBER_OF_COLUMNS = 10

        self.SPACING = Window.size[0] / self.NUMBER_OF_COLUMNS
        self.BOX_WIDTH = (self.SPACING * 7) / 2
        self.BOX_HEIGHT = (self.SPACING * 4) / 2

        self.BOX_X = (Window.size[0] / 2) - (self.BOX_WIDTH / 2)
        self.BOX_Y = Window.size[1] * 0.05 + self.SPACING

        self.LEFT_WALL_X = self.SPACING
        self.RIGHT_WALL_X = Window.size[0] - self.SPACING

        self.speed_fast = False

        self.next_shape_array = []
        self.NEXT_SHAPE_SCALING_FACTOR = 2
        self.SPEED_FACTOR_ARRAY = [1, 1 / 10]
        self.speed_vertical = Window.size[1] / self.NUMBER_OF_ROWS
        self.SPEED_HORIZONTAL = Window.size[0] / self.NUMBER_OF_COLUMNS

        self.STARTING_X = Window.size[0] / 2

        self.CUT_OFF_HEIGHT = (Window.size[0] / self.NUMBER_OF_COLUMNS) * 4
        self.AFTER_WINNING_LINE_MOVE_TO = self.CUT_OFF_HEIGHT + self.SPACING
        self.Y_BOTTOM = self.AFTER_WINNING_LINE_MOVE_TO
        self.BLOCK_DROP_START_HEIGHT = Window.size[1] * 1
        # BLOCK_DROP_START_HEIGHT = AFTER_WINNING_LINE_MOVE_TO + 2 * SPACING

        self.active_array = []

        self.dead_array = []

        self.dead_array_top = []

        self.shapes_list = ['T', 'L', 'I', 'O', 'S', 'Z', 'J']
        # shapes_list = ['L']
        self.current_active_shape = random.choice(self.shapes_list)
        self.index = 0
        self.orientations = ['up', 'left', 'down', 'right']
        self.current_orientation = self.orientations[self.index]
        self.next_shape = []

    def restart(self,*args):

        self.sound_track.play()
        self.sound_track.loop = True
        #self.ids.score_label.text = f"SCORE: {self.score}"

        Clock.schedule_interval(self.check_for_shape_release, 1)
        Clock.schedule_interval(self.move_shape_down, self.SPEED_FACTOR_ARRAY[0])
        Clock.schedule_interval(self.move_dead_bits_down, 1)
        Clock.schedule_interval(self.show_next_shape, 1)
        Clock.schedule_interval(self.arrays_columns_dead_bits, 1)
        Clock.schedule_interval(self.check_defeat, 1)


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(SecondScreen(name='second'))
        return sm

MyApp().run()


