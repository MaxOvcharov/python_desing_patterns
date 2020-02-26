# coding: utf-8
"""
EXAMPLE - from book "Learning Python Design Patterns"
"""
import abc
import os


class Command(metaclass=abc.ABCMeta):
    """The Command interface."""

    def __init__(self, receiver):
        self.receiver = receiver

    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def undo(self):
        pass


class TouchCommand(Command):
    """Create and delete file like Unix - touch."""

    def execute(self):
        self.receiver.create_file()

    def undo(self):
        self.receiver.delete_file()


class TouchReceiver:
    """Do all work of creating and deleting file."""

    def __init__(self, file_name):
        self.file_name = file_name

    def create_file(self):
        """Actual implementation of Unix touch command."""
        with open(self.file_name, 'a'):
            os.utime(self.file_name, None)

    def delete_file(self):
        """Undo Unix touch command."""
        os.remove(self.file_name)


class Invoker:
    """Ask the command to carry out the request."""

    def __init__(self, create_file_commands=None, delete_file_commands=None):
        self.create_file_commands = create_file_commands or []
        self.delete_file_commands = delete_file_commands or []
        self.history = []

    def create_file(self):

        print('Creating file...')

        for command in self.create_file_commands:
            command.execute()
            self.history.append(command)

        print('File created.\n')

    def delete_file(self):

        print('Deleting file...')

        for command in self.delete_file_commands:
            command.execute()
            self.history.append(command)

        print('File deleted.\n')

    def undo_all(self):
        print('Undo all...')
        for command in self.history:
            command.undo()

        print('Undo all finished...')


def main():
    # Client
    touch_receiver = TouchReceiver('file_name')
    touch_command = TouchCommand(touch_receiver)

    # Command
    create_commands = [touch_command, ]

    # Invoker
    invoker = Invoker(create_commands)
    invoker.create_file()
    invoker.undo_all()


if __name__ == "__main__":
    main()
