#!/usr/bin/env python
import pdb
from c45 import C45

# Run both continuous and discrete examples
print("[Weather data]")
c1 = C45("../data/weather/weather.data", "../data/weather/weather.names")
c1.fetchData()
c1.preprocessData()
c1.generateTree()
c1.printTree()

print("\n[Iris data]")
c1 = C45("../data/iris/iris.data", "../data/iris/iris.names")
c1.fetchData()
c1.preprocessData()
c1.generateTree()
c1.printTree()
