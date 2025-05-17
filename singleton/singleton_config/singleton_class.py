class Singleton:
    _instance = None

    def __new__(cls, **kwargs):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        if not hasattr(self, 'configuration'):
            self.configuration = {}
        self.configuration.update(kwargs)

# Usage
a = Singleton(dj=42, daniel=42)
print(a.configuration)
b = Singleton(dj=14)

print(a is b)  # True
print(a.configuration)