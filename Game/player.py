import keyboard as k
import items as i

class player:

    def __init__(self,position):
        self.name = None
        self.position = position
        self.direction = None
        self.visibility_level = None #depends on the item
        self.inventory = [] #what items player has
        self.inventory_size = 2 #starts with size of 2
        self.HP = 100 #start will full HP
        self.gold = 0
        self.luck = 1

    def print_stats(self):
        print('-'*212)
        print(f'{self.name}|HP: {self.HP}|Facing: {self.direction}|Gold: {self.gold:.2f}|Luck: {self.luck:.2f}|Visibility: {self.visibility_level}'.center(212))

    def move_player(self,maze):

        listener = k.keyboard(['w','a','s','d'])
        dir = listener.get_key()
        r,c = self.position

        if dir == 'w' and [r-1,c] not in maze.wall_tiles:
            self.position[0] -= 1
            self.direction = "↑"
        elif dir == 'a' and [r,c-1] not in maze.wall_tiles:
            self.position[1] -= 1
            self.direction = "←"
        elif dir == 's' and [r+1,c] not in maze.wall_tiles:
            self.position[0] += 1
            self.direction = "↓"
        elif dir == 'd' and [r,c+1] not in maze.wall_tiles:
            self.position[1] += 1
            self.direction = "→"
        else:
            print("thats a wall")

    def get_visible(self): #returns tiles nearby that are visible to the player
        r,c = self.position
        visible_list = []

        if self.visibility_level == None:
            return [self.position]
        elif self.visibility_level == "match":
            if self.direction == "↑":
                return [self.position,[r-1,c]]
            elif self.direction == "←":
                return [self.position,[r,c-1]]
            elif self.direction == "↓":
                return [self.position,[r+1,c]]
            else:
                return [self.position,[r,c+1]]

    def update_visibility(self,item): #torch,candle,etc
        self.visibility_level = item
        print(self.visibility_level)

    def update_gold(self,amount):
        self.gold += amount

    def update_luck(self,amount):
        self.luck += amount
