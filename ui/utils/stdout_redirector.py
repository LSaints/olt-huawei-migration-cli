from textual.widgets import Log

class StdoutRedirector:
    def __init__(self, log_widget: Log):
        self.log_widget = log_widget
        
    def write(self, message: str):
        self.log_widget.write_line(message)
            
    def flush(self):
        pass