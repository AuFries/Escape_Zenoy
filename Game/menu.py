import os
import ctypes
import msvcrt
import subprocess
import colors
import keyboard as k

from ctypes import wintypes
from os import system, name

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

class menu:

    def __init__(self):
        pass

    def print_spacer(self):
        print('-'*212)

    def print_imagery(self,title_maze):
        self.clear()
        title_maze.print_full_maze()
        self.print_spacer()
        print("Welcome to Zenoy.".center(212))
        print("Choose a number to begin.".center(212))
        self.print_spacer()

    def print_menu(self,title_maze,choice_index):
        choice_list = ["1 Play", "2 Rules", "3 Probabilties and Statistics", "4 Credits"]

        self.print_imagery(title_maze)

        if choice_index == None:
            for choice in choice_list:
                print(" "*80,end='')
                print(choice)
            return

        for choice in choice_list:
            print(" "*80,end='')
            if choice_index == choice_list.index(choice):
                print(colors.colors.bg.green,choice[0],colors.colors.bg.black,choice[1:])
            else:
                print(choice)

        self.print_spacer()
        print(f"Click {choice_index+1} again to confirm.".center(212))

    def start_menu(self,title_maze):

        listener = k.keyboard(['1','2','3','4'])

        choice_index = None
        confirmed = False
        while not confirmed:

            self.print_menu(title_maze,choice_index)
            choice1 = listener.get_key()
            choice_index = int(choice1)-1
            self.print_menu(title_maze,choice_index)

            choice2 = listener.get_key()
            choice_index = int(choice2)-1
            self.print_menu(title_maze,choice_index)

            if choice1 == choice2:
                confirmed = True


    def maximize_console(self,lines=None):
        fd = os.open('CONOUT$', os.O_RDWR)
        try:
            hCon = msvcrt.get_osfhandle(fd)
            max_size = kernel32.GetLargestConsoleWindowSize(hCon)
            if max_size.X == 0 and max_size.Y == 0:
                raise ctypes.WinError(ctypes.get_last_error())
        finally:
            os.close(fd)
        cols = max_size.X
        hWnd = kernel32.GetConsoleWindow()
        if cols and hWnd:
            if lines is None:
                lines = max_size.Y
            else:
                lines = max(min(lines, 9999), max_size.Y)
            subprocess.check_call('mode.com con cols={} lines={}'.format(
                                    cols, lines))
            user32.ShowWindow(hWnd, SW_MAXIMIZE)

    def clear(self):
        # for windows
        if name == 'nt':
            _ = system('cls')
