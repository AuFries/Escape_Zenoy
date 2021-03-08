import colors
import copy
import csv
import random

class maze:

    wall_tile_dict = {0:u'\u2550',1:u'\u2551',2:u'\u2554',3:u'\u2557',4:u'\u255A',5:u'\u255D',6:u'\u2560',7:u'\u2563',8:u'\u2566',9:u'\u2569',10:u'\u256C'} #Used to change associated tiles from regular to extended ascii
    #0:═ 1:║, 2:╔, 3:╗, 4:╚, 5:╝, 6:╠, 7:╣, 8:╦, 9:╩, 10:╬

    #nearby_coord in fix_walls uses index [0,1,2,3] to associate this change
    # 0
    #1@2
    # 3
    wall_index = {(0,1):5, (0,2):4, (0,3):1, (1,2):0, (1,3):3, (2,3):2, (0,1,2):9, (0,1,3):7, (0,2,3):6, (1,2,3):8, (0,1,2,3):10} #The associated position combinations for walls in wall_tile_dict

    def __init__(self,name,maze_list):
        self.name = name
        self.maze_list = maze_list #the full maze
        self.visible_tiles = []
        self.wall_tiles = []
        self.fg_tile_color_dict = {}
        self.bg_tile_color_dict = {}

    def fix_walls(self): #appends wall locations to wall_tiles, then fixes them depending on nearby wall locations
        for r, line in enumerate(self.maze_list):
            for c in range(len(line)):
                if line[c] == "w":
                    self.wall_tiles.append([r,c])

        temp = copy.deepcopy(self.maze_list)

        for r, line in enumerate(temp):
            for c in range(len(line)):
                if line[c] == "w":
                    nearby_coords = [[r-1,c],[r,c-1],[r,c+1],[r+1,c]]
                    nearby_walls = []

                    for coord in nearby_coords:
                        try:
                            if temp[coord[0]][coord[1]] == "w":
                                nearby_walls.append(nearby_coords.index(coord))
                        except:
                            pass

                    nearby_walls.sort()
                    try:
                        self.maze_list[r][c] = self.wall_tile_dict[self.wall_index[tuple(nearby_walls)]]
                    except:
                        pass

    def initialize_tiles(self,tile_file): #initializes tile events and colors depending on data from CSV file
        with open(tile_file) as csvfile: #file contains tile,fg,bg
            tile_reader = csv.reader(csvfile, delimiter=',')
            for line in tile_reader:
                tile = line[0]
                if line[1] != "NA":
                    self.fg_tile_color_dict[tile] = line[1]
                if line[2] != "NA":
                    self.bg_tile_color_dict[tile] = line[2]

    def get_initial_player_position(self): #immediately adds the nearest tiles to the visible_tiles
        for r, line in enumerate(self.maze_list):
            for c in range(len(line)):
                if line[c] == "@":
                    return [r,c]
        return [0,0] #Place player in top left if they aren't already on the map


    def print_full_maze(self):
        for r, line in enumerate(self.maze_list):
            for c in range(len(line)):
                tile = self.maze_list[r][c]

                if [r,c] in self.wall_tiles:
                    print(eval(self.fg_tile_color_dict['w'])+tile,end='')
                elif tile in self.fg_tile_color_dict:
                    print(eval(self.fg_tile_color_dict[tile])+tile,end='')
                else:
                    print(colors.colors.fg.white+tile,end='')
            print()

    def print_visible_maze(self,added_visibility): #prints the maze visible to the player, takes in the new visible tiles with near player
        fog_dict = {1:u'\u2591',2:u'\u2592',3:u'\u2593'}

        for coords in added_visibility:
            if coords not in self.visible_tiles:
                self.visible_tiles.append(coords[:])
        self.visible_tiles.sort()

        for r, line in enumerate(self.maze_list):
            for c in range(len(line)):
                if [r,c] in self.visible_tiles:
                    tile = self.maze_list[r][c]

                    if [r,c] in self.wall_tiles:
                        print(eval(self.fg_tile_color_dict['w'])+tile,end='')
                    elif tile in self.fg_tile_color_dict:
                        print(eval(self.fg_tile_color_dict[tile])+tile,end='')
                    else:
                        print(colors.colors.fg.white+tile,end='')
                else:
                    print(colors.colors.fg.white+fog_dict[random.randint(1,3)],end='')
            print()


    def update_visible(self): #updates the player visibility, adding to visible_maze and visible_tiles
        print("visible maze updated")

    def update_player_position(self,player_position): #update player
        for r, line in enumerate(self.maze_list):
            for c in range(len(line)):
                if line[c] == "@":
                    self.maze_list[r][c] = " " #replaces old @ location with new one
                if [r,c] == player_position:
                    self.maze_list[r][c] = "@"

    def update_monster_positions(self,monster_controller):
        for r, line in enumerate(self.maze_list):
            for c in range(len(line)):
                if self.maze_list[r][c].isupper(): #Wipes all monster characters from the maze
                    self.maze_list[r][c] = " "

        for monster in monster_controller.monster_dict: #adds monster characters back to maze in new repspective positions
            mon = monster_controller.monster_dict[monster]
            if len(mon.positions) != 0: #checks if there are positions to add
                for pos in mon.positions[self.name]:
                    self.maze_list[pos[0]][pos[1]] = mon.letter


def initialize_maze(name,maze_file,tile_file): #creates the maze object with the initialized maze_list
    maze_list = []
    with open(maze_file, 'r') as maze_file:
        for r, line in enumerate(maze_file):
            maze_list.append([])
            for c in range(len(line)):
                if line[c] != "\n":
                    maze_list[r].append(line[c])
    m = maze(name,maze_list)
    m.fix_walls()
    m.initialize_tiles(tile_file)
    return m
