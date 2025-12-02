# TODO: ADD decorators

class Ship:
    """ Impletes the ship class for the battleships game. """
    def __init__(self, size: int):
        if type(size) is not int:
            raise Exception("ERROR: size must be an integer")

        self.__size = size
        self.__is_destroyed = False

    def get_size(self) -> int:
        return self.__size

    def is_destroyed(self) -> bool:
        return self.__is_destroyed

    def hit(self):
        if self.__size == 0:
            return

        self.__size -= 1

        if self.__size == 0:
            self.__destroy()

    def __destroy(self):
        self.__is_destroyed = True

