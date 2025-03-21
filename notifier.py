from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod 
    def send_message(self, message): 
        pass
    
    def format_message(self, title, link): 
        return self.format.format(title=title, link=link)

    @abstractmethod
    def is_ready(self): 
        pass


