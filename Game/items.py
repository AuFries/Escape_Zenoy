import player as p
import csv
import random

class items:

    item_dict = {} #contains dictionary of item tiles and their locations

    def __init__(self,maze,items_file):
        self.initialize_items(maze,items_file)

    def initialize_items(self,maze,items_file): #takes in item character and the respective class, then initializes item objects and their locations
        with open(items_file) as csvfile:
            item_reader = csv.reader(csvfile, delimiter=',')
            for line in item_reader:
                self.item_dict[line[0]] = eval(line[1])

        for item in self.item_dict:
            self.item_dict[item].initialize_pos(maze)

class sight(items): #match, small candle, regular candle, torch, large torch

    sight_dict = {0: None, 1:"match",2:"small candle",3:"regular candle",4:"torch",5:"large torch"}
    sight_positions = []

    def __init__(self):
        self.sight_level = 0

    def initialize_pos(self,maze): #initialize positions of sight related tiles
        for r, line in enumerate(maze.maze_list):
            for c in range(len(line)):
                if maze.maze_list[r][c] == 'l':
                    self.sight_positions.append([r,c])
        print("sight initialized")

    def update_visibility(self,player):
        self.sight_level += 1
        player.update_visibility(self.sight_dict[self.sight_level])


class weapons(items):
    pass

class potions(items):
    pass

class upgrades(items):

    def __init__(self):
        self.charm_positions = []

    def initialize_pos(self,maze):
        for r, line in enumerate(maze.maze_list):
            for c in range(len(line)):
                if maze.maze_list[r][c] == 'c':
                    self.charm_positions.append([r,c])
        print("charm initialized")

    def increase_luck(self,player):
        amount = random.uniform(0.01,0.2)
        player.update_luck(amount)


class currency(items):

    gold_positions = []

    def __init__(self):
        self.gold = 0

    def initialize_pos(self,maze):
        for r, line in enumerate(maze.maze_list):
            for c in range(len(line)):
                if maze.maze_list[r][c] == '.':
                    self.gold_positions.append([r,c])
        print("gold initialized")

    def give_gold(self,player):
        amount = random.randint(1,9)
        amount *= player.luck
        player.update_gold(amount)
