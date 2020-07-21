

from math import *
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

from math import pi, asin, sin, degrees
halfpi, twopi = .5 * pi, 2 * pi
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


def create_plane_sides(shape, axes=2, offset=(0,0,0)):
    x, y = shape
    points = np.roll( ((0, -0.5 * x, -0.5 * y),
                       (0,  0.5 * x, -0.5 * y),
                       (0, -0.5 * x,  0.5 * y),
                       (0,  0.5 * x,  0.5 * y))
                       , axes, axis=1 ).astype( dtype=np.float64 ) + offset
    return points, ( (0,1,3,2), )


def create_polygon_sides(points2d, axes=2, offset=(0,0,0)):
    points = np.roll( np.insert(points2d, 0, 0, axis=1), axes, axis=1 ) \
            .astype( dtype=np.float64 ) + offset
    return points, (tuple( range(len(points2d)) ),)


def create_extruded_polygon_sides(points2d, delta, axes=2, offset=(0,0,0)):
    if points2d[-1] != points2d[0]:
        points2d = np.vstack( (points2d, points2d[:1]) ) # close it
    n_points = len(points2d)
    points = np.vstack( (
            np.roll( np.insert(points2d, 0, .5 * delta, axis=1), axes, axis=1 ) \
                    .astype( dtype=np.float64 ), 
            np.roll( np.insert(points2d, 0, -.5 * delta, axis=1), axes, axis=1 ) \
                    .astype( dtype=np.float64 ) ) ) + offset
    faces = ( tuple( range(n_points) ), tuple( range(n_points, 2*n_points, 1) ) ) \
            + tuple( (i, i+1, i+1+n_points, i+n_points) for i in range(n_points-1) )
    return points, faces


def create_box_sides(shape, offset=(0,0,0)):
    shape = np.reshape ( shape, (1, 3) ).astype( dtype=np.float64 )
    points = np.vstack( tuple ( shape * ( x, y, z )
            for z in ( -.5, .5 ) 
            for y in ( -.5, .5 ) 
            for x in ( -.5, .5 ) ) ) + offset
    return points, ( (0,1,3,2),
                     (0,1,5,4),
                     (1,3,7,5),
                     (3,2,6,7),
                     (2,0,4,6),
                     (4,5,7,6) )


def create_globe_sides(radius, n_lats, n_lons=None, offset=(0,0,0)):
    if n_lons is None: n_lons = n_lats
    n_pieces = n_lats * n_lons
    assert type(n_lats) is int and n_lats >= 3 \
            , 'n_lats must be an int of at least 3, but is {:}'.format( n_lats )
    assert type(n_lons) is int and n_lons >= 3 \
            , 'n_lons must be an int of at least 3, but is {:}'.format( n_lons )
    points = np.array( tuple((radius * cos(lon) * cos(lat),
                         radius * sin(lat),
                         radius * sin(lon) * cos(lat))
                         for lat in (asin(2. * i / n_lats - 1) 
                                for i in range(n_lats+1))
                         for lon in (twopi * i / n_lons 
                                for i in range(n_lons))),
                      dtype=np.float64 ) + offset
    faces = tuple( (i+j, (i+1)%n_lons+j, (i+1)%n_lons+j+n_lons, i+j+n_lons) \
            for j in range(0,n_lons*n_lats,n_lons) for i in range(n_lons) )
    return points, faces

