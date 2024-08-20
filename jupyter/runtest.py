import os
import sys
p = os.path.abspath("")
print(p)
sys.path.insert(0, p)
p = os.path.abspath(os.path.join(p, os.path.relpath('libs')))
sys.path.insert(0, p)

print('-' * 100)
print(os.path.abspath(sys.argv[0]))
print(os.path.abspath(""))
print(sys.path)
from datetime import datetime
from libs.paydown import *
