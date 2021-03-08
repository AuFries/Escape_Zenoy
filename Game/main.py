import csv
import os
import time

#User defined classes
import maze as m
import monsters as mon
import player as p
import items as i
import menu as men
import events as e

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

def main():
    parent = os.path.dirname(os.getcwd()) #The parent path (Escape_Zenoy)

    menu = men.menu() #used to command menu
    menu.maximize_console() #changes screensize to fullscreen

    #initializes all the maze objects
    title_maze = m.initialize_maze("maze1",parent+"/Mazes/title_image.txt",parent+"/CSV_data/title_tiles.csv")
    maze1 = m.initialize_maze("maze1",parent+"/Mazes/maze1.txt",parent+"/CSV_data/maze1_tiles.csv")
    # maze1 = m.initialize_maze("maze2",parent+"/Mazes/maze2.txt",parent+"/CSV_data/maze2_tiles.csv")
    # maze1 = m.initialize_maze("maze3",parent+"/Mazes/maze3.txt",parent+"/CSV_data/maze3_tiles.csv")

    #initializes all monster objects
    mon.initialize_monsters(parent+"/CSV_data/monsters.csv")

    #creates controller for monster functions
    monster_controller = mon.monster_controls()

    #initializes monster positions for each maze
    monster_controller.initialize_positions("maze1",maze1.maze_list) #this also calls a function to initialize the direction that the monsters will initially move

    # monster_controller.initialize_positions("maze2",maze2.maze_list)
    # monster_controller.initialize_positions("maze3",maze3.maze_list)
    # monster_controller.initialize_positions("title_image",title_maze.maze_list)

    # monster_controller.print_positions()
    # monster_controller.print_attributes("X")

    player = p.player(maze1.get_initial_player_position())

    menu.start_menu(title_maze)
    menu.clear()

    maze1.print_full_maze()
    # maze1.print_visible_maze(player.get_visible())

    #creates event controller to check and initiate events
    event_controller = e.events()
    event_controller.initialize_events(parent+"/CSV_data/tile_events.csv")

    #creates the item manager to control item related events
    item_manager = i.items(maze1,parent+"/CSV_data/items.csv")

    while True:
        time.sleep(0.2)
        player.move_player(maze1)
        menu.clear()
        maze1.update_player_position(player.position)
        monster_controller.move_monsters("maze1",maze1,player.position)
        maze1.update_monster_positions(monster_controller)
        # maze1.print_visible_maze(player.get_visible())
        event_controller.check_events(maze1,player,item_manager,monster_controller)
        # print(player.visibility_level)
        maze1.print_full_maze()
        player.print_stats()
        # print(item_manager.item_dict)


if __name__ == "__main__":
    main()
