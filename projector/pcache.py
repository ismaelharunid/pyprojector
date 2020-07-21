

import numpy as np
import numpy_indexed as npi
from .common import POINT_DTYPE, POINT_NCOLUMNS, Sequence, Iterator
from .pointarray import PointArray


CAPACITY = 1000


class PCache(PointArray):
    
    def __new__(cls, capacity=CAPACITY, 
            n_columns=POINT_NCOLUMNS, 
            dtype=POINT_DTYPE):
        self = super(PCache, cls).__new__(cls, capacity
                , n_columns=n_columns, dtype=dtype)
        self._length = 0
        return self
    
    def __array_finalize__(self, obj):
        pass

    _length = 0

    @property
    def n_points(self):
        return self[self._length]
    
    @property
    def capacity(self):
        return self._ndarray.shape[0]

    def __init__(self, *args, **kwargs):
        pass
    
    def __len__(self):
        return self._length
    
    def __str__(self):
        return np.ndarray.__str__(self[:self._length])
    
    def __repr__(self):
        return np.ndarray.__repr__(self[:self._length])
    
    def index(self, point):
        if self._length > 0:
            return npi.indices(self[:self._length], [point], 0)[0]
        raise KeyError('Not all keys in `that` are present in `this`')

    def push(self, point):
        if self._length >= self.shape[0]:
            raise OverflowError("Attempted to overrun PCache @ {:}".format(i))
        self[self._length] = point
        index, self._length = (self._length, self._length + 1)
        return index
    
    def put(self, point):
        try:
            return self.index(point)
        except KeyError as ke:
            pass
        return self.push(point)

    def indices(self, points):
        return npi.indices(self, points, 0)

    def put_points(self, points, asiter=False):
        it = ((self.push(p) if i < 0 else i) for (p, i) in 
                zip(points, npi.indices(self[:self._length], points, 0, -1)))
        return it if asiter else list(it)

