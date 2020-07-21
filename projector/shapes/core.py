

from math import pi, asin, acos, atan, atan2, cos, sin, tan, degrees, radians
quarterpi .25 * pi
sixthpi = pi / 6
halfpi = .5 * pi
thirdpi = pi / 3
twopi = 2 * pi
lerp = lambda a, b, t=0.5: a + (b-a) * t
lerpit = lambda it0, it1, t=0.5: type(a)(a + (b-a) * t \
        for (a, b) in zip(it0, it1))
dists = lambda s: np.sum(na ** 2)
distit = lambda it: np.sum(sum(c**2 for c in it))


import numpy as np
epsilon64 = np.finfo(np.float64).resolution

sphere_area = lambda R=1.0: 4 * pi * R ** 2

lat_dist = lambda lat, R=1.0: R*(1-sin(lat))

#A = 2*pi*R^2(1-sin(lat))
def sphere_latarea(lat, R=1.0):
    if -halfpi > lat or lat > halfpi:
        raise ValueError("lat must be between -halfpi and halfpi")
    return 2 * pi * R ** 2 * (1-sin(lat))

sphere_lonarea = lambda lon, R=1.0: \
        4 * pi * R ** 2 * lon / twopi

#A = 2*pi*R^2 |sin(lat1)-sin(lat2)| |lon1-lon2|/360
#    = (pi/180)R^2 |sin(lat1)-sin(lat2)| |lon1-lon2|
sphere_rectarea = lambda lat0, lat1, lon0, lon1, R=1.0: \
        (sphere_latarea(lat0, R)-sphere_latarea(lat1, R)) * (lon1-lon0) / twopi


def new_pcache():
    return np.ndarray( (0,3), dtype=np.float64 )


def pcache_point_indexof(pcache, point, default=None):
    n_pcache = len(pcache)
    for i in range(n_pcache):
        if all(abs(point - pcache[i]) <= epsilon64):
            #print("found", i, point)
            return i
    i = default(None, pcache, point) if callable(default) else default
    #print("new", i, point)
    return i


def pcache_points_indexes(pcache, points, default=None):
    return (pcache_point_indexof(pcache, p, default) for p in points)


def pcache_points_extend(pcache, points):
    n_pcache = len(pcache)
    new_points = []
    def reindexer(i, pcache, point):
        new_index = n_pcache + len(new_points)
        new_points.append( point )
        return new_index
    indexes = tuple(pcache_points_indexes(pcache, points, reindexer))
    new_points.insert(0, pcache)
    return np.vstack( new_points ), indexes


def pcache_points_face_extend(pcache, points, face):
    return pcache_points_extend(pcache, (points[i] for i in face))


def pcache_points_faces_extend(pcache, points, faces):
    accum = []
    for face in faces:
        pcache, face = pcache_points_face_extend(pcache, points, face)
        accum.append( face )
    return pcache, tuple(accum)


def create_x_transform_matrix( ca, sa ):
    return np.array( ( (  1,  0,  0), 
                       (  0, ca,-sa), 
                       (  0, sa, ca) ), 
                    dtype=np.float64 )

def create_y_transform_matrix( ca, sa ):
    return np.array( ( ( ca,  0, sa), 
                       (  0,  1,  0), 
                       (-sa,  0, ca) ), 
                    dtype=np.float64 )

def create_z_transform_matrix( ca, sa ):
    return np.array( ( ( ca,-sa,  0), 
                       ( sa, ca,  0), 
                       (  0,  0,  1) ), 
                    dtype=np.float64 )

c45, s45 = cos(radians(45)), sin(radians(45))
TRANSFORM_X45_MATRIX = create_x_transform_matrix( c45, s45 )
TRANSFORM_Y45_MATRIX = create_y_transform_matrix( c45, s45 )
TRANSFORM_Z45_MATRIX = create_z_transform_matrix( c45, s45 )


def points_sides_depth_sorted_sides(points, sides):
    return ( s[1] 
            for s in sorted( ((min(points[i,2] for i in side), side) 
            for side in sides),
            key=lambda pair: pair[0], reverse=True ) )


