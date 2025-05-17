def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Config:
    def __init__(self):
        self.setting = 'default'

# Usage
cfg1 = Config()
cfg2 = Config()
print(cfg1 is cfg2)  # True