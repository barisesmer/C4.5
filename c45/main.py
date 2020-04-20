#!/usr/bin/env python
from c45 import C45
import pandas as pd

data = pd.read_csv("../data/iris/iris.data", header = None)
c1 = C45(data, [False, False, False, False])

c1.generate_tree()
