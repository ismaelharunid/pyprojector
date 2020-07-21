

import numpy as np
from .common import Sequence, Iterator, Number, POINT_DTYPE, POINT_NCOLUMNS


class PointArray(np.ndarray):

    def __new__(cls, initializer,
            n_columns=POINT_NCOLUMNS, dtype=POINT_DTYPE):
        n_points = 0
        if isinstance(initializer, Sequence) and initializer:
            if isinstance(initializer[0], Sequence):
                if any(len(i) != n_columns for i in initializer):
                    raise ValueError("bad initializer shape")
                n_points = len(initializer)
            elif isinstance(initializer[0], Number):
                n_points = len(initializer) // n_columns
                if n_points * n_columns != len(initializer):
                    raise ValueError("bad initializer shape")
            self = super(PointArray, cls).__new__(cls,
                    shape=(n_points, n_columns)
                    , dtype=dtype)
            self[:] = np.reshape( initializer, (n_points, n_columns) )
        elif isinstance(initializer, np.ndarray):
            n_points = len(initializer)
            self = super(PointArray, cls).__new__(cls,
                    shape=(n_points, n_columns)
                    , dtype=dtype)
            self[:] = initializer
        elif type(initializer) is int:
            n_points = initializer
            self = super(PointArray, cls).__new__(cls,
                    shape=(n_points, n_columns)
                    , dtype=dtype)
        else:
            raise ValueError("bad initializer, expected a size, Sequence or ndarray")
        return self

    def __array_finalize__(self, obj):
        pass

    @property
    def n_points(self):
        return self.shape[0]

    @property
    def n_columns(self):
        return self.shape[1]

    def __init__(self, *args, **kwargs):
        pass
    
