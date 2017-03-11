#!/usr/bin/env python
import pdb
from c45 import C45

c1 = C45("../data/iris/iris.data", "../data/iris/iris.names")
c1.fetchData()
c1.preprocessData()
c1.generateTree()
c1.printTree()
