import msvcrt as m

class keyboard:

    def __init__(self,wait_for_keys): #only returns a key pressed if it is within wait_for_keys
        self.wait_for_keys = wait_for_keys

    def get_key(self):
        while True:
            while m.kbhit(): #Clears keyboard buffer
                m.getch()
            key_pressed = str(m.getch())
            key_pressed = key_pressed[2:-1]
            if key_pressed in self.wait_for_keys:
                return key_pressed
