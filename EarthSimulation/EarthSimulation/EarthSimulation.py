from Earth import Earth
from Graphics import Graphics
import matplotlib.pyplot as plt
import numpy as np
import random


e = Earth()
e.generateEarth()
g = Graphics(e.ROWS,e.COLUMNS, 500, e)


