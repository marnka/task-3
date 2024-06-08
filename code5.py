from abc import ABC, abstractmethod

class EventManager:
    
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)

    def notify(self, event_type, data):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener.update(data)

class EventListener(ABC):
    @abstractmethod
    def update(self, data):
        pass

class Editor:
    def __init__(self):
        self.events = EventManager()
        self.file = None

    def open_file(self, path):
        self.file = path
        self.events.notify("open", self.file)

    def save_file(self):
        if self.file:
            self.events.notify("save", self.file)

class LoggingListener(EventListener):
    def __init__(self, log_filename, message):
        self.log_filename = log_filename
        self.message = message

    def update(self, filename):
        with open(self.log_filename, 'a') as log_file:
            log_file.write(self.message % filename + '\n')

class EmailAlertsListener(EventListener):
    def __init__(self, email, message):
        self.email = email
        self.message = message

    def update(self, filename):
        print(f"Email sent to {self.email}: {self.message % filename}")

if __name__ == "__main__":
    editor = Editor()

    logger = LoggingListener("/path/to/log.txt", "Someone has opened file: %s")
    editor.events.subscribe("open", logger)

    email_alerts = EmailAlertsListener("admin@example.com", "Someone has changed the file: %s")
    editor.events.subscribe("save", email_alerts)

    # Симулюємо дії користувача
    editor.open_file("example.txt")
    editor.save_file()
