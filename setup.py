from ui import TerminalInterface
from core.utils import Logger


class Setup:
    def __init__(self):
        self.__setup_logger()
        self.__setup_terminal_ui()
        
    def __setup_logger(self):
        Logger()
    
    def __setup_terminal_ui(self):
        ui = TerminalInterface()
        ui.run()