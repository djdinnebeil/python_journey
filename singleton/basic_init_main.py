from basic_init_singleton import Singleton
from basic_init_crud import make_singleton

singleton = Singleton()
if hasattr(singleton, 'config'):
    print(singleton.config)
else:
    print('does not have attribute')

make_singleton()
if hasattr(singleton, 'config'):
    print(singleton.config)
else:
    print('does not have attribute')