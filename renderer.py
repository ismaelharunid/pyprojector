



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


def points_isometric_transform(points):
    npa0 = np.matmul(points, TRANSFORM_Z45_MATRIX)
    return np.matmul(npa0, TRANSFORM_X45_MATRIX)


def points_sides_depth_sorted_sides(points, sides):
    return ( s[1] 
            for s in sorted( ((min(points[i,2] for i in side), side) 
            for side in sides),
            key=lambda pair: pair[0], reverse=True ) )


def drawer_points_sides_orthographic(drawer, points, sides,
        outline=None, weight=1.0, fill=None,
        offset3d=(0,0,0), offset2d=(0,0)):
    #npa0 = np.matmul(TRANSFORM_X_MATRIX, points.T)
    #npa1 = np.matmul(TRANSFORM_Y_MATRIX, npa0)
    #npa1 = np.matmul(TRANSFORM_Y_MATRIX, points.T)
    # npa0 = np.matmul(TRANSFORM_Z45_MATRIX, points.T)
    # npa1 = np.matmul(TRANSFORM_X45_MATRIX, npa0)
    # npa2 = npa1.T + offset3d
    #npa0 = np.matmul(points, TRANSFORM_Z45_MATRIX)
    #npa1 = np.matmul(npa0, TRANSFORM_X45_MATRIX)
    #npa2 = npa1 + offset3d
    npa2 = points_isometric_transform(points) + offset3d
    changed = False
    for side in points_sides_depth_sorted_sides(npa2, sides):
        xy = sum((tuple(npa2[i,(0,1)] + offset2d) for i in side), ())
        changed = drawer.draw_polygon(xy, outline, weight, fill) or changed
    return changed

