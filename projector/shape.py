


import numpy as np
import numpy_indexed as npi
from .common import POINT_DTYPE, POINT_NCOLUMNS, Sequence, Iterator


class Shape(np.ndarray):
    
    def __new__(cls, *args, **kwargs):
        return super(Shape, cls).__new__(cls, *args, **kwargs)

    def __array_finalize__(self, obj):
        print('In array_finalize:')
        print('   self type is %s' % type(self))
        print('   obj type is %s' % type(obj))

