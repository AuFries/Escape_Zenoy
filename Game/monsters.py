import csv
import random

class monster: #the overarching monster attributes

    monster_dict = {} #dictionary contains monster objects {"C": cransk object}
    nearby_monsters = [] #the lists of monsters that can see the player

    def __init__(self,attribute_list):
        self.name = attribute_list[0]
        self.letter = attribute_list[1]
        self.attack = attribute_list[2]
        self.defense = attribute_list[3]
        self.dexterity = attribute_list[4]
        self.luck = attribute_list[5]
        self.balance = attribute_list[6]
        self.attack_name = attribute_list[7]
        self.movement_style = attribute_list[8]
        self.flee_chance = attribute_list[9]
        self.sight = attribute_list[10] #sight is a sight*sight square in which the monster will hunt you
        self.aggression = attribute_list[11]
        self.positions = {} #consists of [r,c,d] row,column,and movement direction


    def attack_player(self):
        pass

    def find_index_of_tile_to_move(self,nearby_tiles,player_position): ####################################################################FIX THIS SO MONSTER CANT GO THROUGH WALLS
        distance_list = [] #a list containing the distances away from the player
        Pr, Pc = player_position

        for i in range(len(nearby_tiles)): #(xf-xi)^2 + (yf-yi)^2
            distance_list.append((Pr-nearby_tiles[i][0])**2 + (Pc-nearby_tiles[i][1])**2)

        return distance_list.index(min(distance_list))

    def move_towards_player(self,monster,maze_name,maze,position_index,player_position):
        Mr, Mc, _ = monster.positions[maze_name][position_index]
        nearby_tiles = []

        for i in range(-1,2): #tiles immediately surrounding monster
            for j in range(-1,2):
                nearby_tiles.append([Mr+i,Mc+j])
        nearby_tiles.remove([Mr,Mc])

        tile_index = self.find_index_of_tile_to_move(nearby_tiles,player_position) #grab the tile index for which to move the monster

        monster.positions[maze_name][position_index][0] = nearby_tiles[tile_index][0] #updates the monster's position
        monster.positions[maze_name][position_index][1] = nearby_tiles[tile_index][1]


    def check_nearby_player(self,monster,maze_name,position_index,player_position): #if player within sight, move towards the player (the last index in positions will change to -1)
        sight = int(monster.sight)
        Mr, Mc, d = monster.positions[maze_name][position_index]

        if d == 0:
            Mc -= 1
        else:
            Mc += 1

        sight_list = [] #the tiles the monster can 'see' if they player is wihtin this, they attack
        for i in range(-1*sight,sight+1):
            for j in range(-1*sight,sight+1):
                    sight_list.append([Mr+i,Mc+j])

        if player_position in sight_list:
            monster.positions[maze_name][position_index][-1] = -1
            print("I see you")
        print(player_position)


    def move_based_on_style(self,monster,maze_name,maze,position_index): #moves each monster and updates their respective positions
        r,c,d = monster.positions[maze_name][position_index]

        if monster.movement_style == "straight_horizontal":
            if d == 0:
                if [r,c-1] not in maze.wall_tiles:
                    monster.positions[maze_name][position_index] = [r,c-1,0]
                else:
                    monster.positions[maze_name][position_index][-1] = 1
            elif d == 1:
                 if [r,c+1] not in maze.wall_tiles:
                     monster.positions[maze_name][position_index] = [r,c+1,1]
                 else:
                    monster.positions[maze_name][position_index][-1] = 0


    def move_monsters(self,maze_name,maze,player_position): #initiates call for movement
        for monster in self.monster_dict:
            if len(self.monster_dict[monster].positions[maze_name]) != 0: #if there is a position in the maze, move the monster
                for i, position in enumerate(self.monster_dict[monster].positions[maze_name]):
                    self.check_nearby_player(self.monster_dict[monster],maze_name,i,player_position)
                    if position[-1] == -1:
                        self.move_towards_player(self.monster_dict[monster],maze_name,maze,i,player_position)
                    else:
                        self.move_based_on_style(self.monster_dict[monster],maze_name,maze,i) #passes type of movement to function and the position index of that instance


    def initialize_positions(self,maze_name,maze_list): #loops through monster list and attributes monster positions to each individual maze ex {"maze1":}
        for monster in self.monster_dict:
            self.monster_dict[monster].positions[maze_name] = []  #These 2 lines create a key within the positions dictionary for each maze name passed in

        for r, line in enumerate(maze_list): #This appends the instances of the monsters in each of their respective mazes
            for c in range(len(line)):
                if maze_list[r][c].isupper(): #uppercase letters are monsters
                    self.monster_dict[maze_list[r][c]].positions[maze_name].append([r,c,random.randint(0,1)]) #the randint initializes direction for monsters that use it

    def print_positions(self,monster=""): #Debugging function, prints each monster's positions in each maze
        if monster != "":
            m = self.monster_dict[monster]
            print(monster,":",m.positions)
            return

        for monster in self.monster_dict:
            print(monster,":",self.monster_dict.positions)

    def print_attributes(self,monster=""): #Debugging function, prints the attributes of each monster, optional to pass in specific monster to print
        if monster != "":
            m = self.monster_dict[monster]
            print(f'{m.name}:{m.letter}, Attack:{m.attack}, Defense:{m.defense}, Dexterity:{m.dexterity}, Luck:{m.luck}, Balance:{m.balance}, Attack name:{m.attack_name}, Movement style:{m.movement_style}, Flee chance:{m.flee_chance}')
            return

        for monster in self.monster_dict:
            m = self.monster_dict[monster] #grabs the object
            print(f'{m.name}:{m.letter}, Attack:{m.attack}, Defense:{m.defense}, Dexterity:{m.dexterity}, Luck:{m.luck}, Balance:{m.balance}, Attack name:{m.attack_name}, Movement style:{m.movement_style}, Flee chance:{m.flee_chance}')


class monster_controls(monster):
    def __init__(self):
        pass

def initialize_monsters(monsters_csv): #Creates monster objects with the values within the csv file
    with open(monsters_csv) as csvfile:
        monster_reader = csv.reader(csvfile, delimiter=',')
        for lst in monster_reader:
            monster.monster_dict[lst[1]] = monster(lst)
        del monster.monster_dict["Letter"] #Removes first element, which is just a line for description of attributes
