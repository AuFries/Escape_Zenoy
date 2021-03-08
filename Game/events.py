import player as p
import csv

class events: #handles game events (such as landing on a tile)

    event_dict = {} #holds the tile and the event that is triggered when it's stepped on

    def __init__(self):
        pass

    def initialize_events(self,events_file): #initializes event_dict depending on tile_events.csv
        with open(events_file) as csvfile:
            event_reader = csv.reader(csvfile, delimiter=',')
            for line in event_reader:
                self.event_dict[line[0]] = line[1]

    def check_events(self,maze,player,item_manager,monster_controller): #checks if the player triggered an event and then calls that event

        if player.position in item_manager.item_dict['l'].sight_positions:
            item_manager.item_dict['l'].sight_positions.remove(player.position)
            print("Executed")
            exec(self.event_dict["l"])

        if player.position in item_manager.item_dict['.'].gold_positions:
            item_manager.item_dict['.'].gold_positions.remove(player.position)
            print("got gold")
            exec(self.event_dict["."])

        if player.position in item_manager.item_dict['c'].charm_positions:
            item_manager.item_dict['c'].charm_positions.remove(player.position)
            print("got charm")
            exec(self.event_dict["c"])
