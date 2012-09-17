import math

def magnitude_3d_euclid(v):
    '''Calculate 3d euclidian magnitude of the vector v
    arg v: indexable of length 3
    '''
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def distance_3d_euclid(v1, v2):
    '''Calculate 3d euclidian distance between vectors v1 and v2'''
    return magnitude_3d_euclid(tuple(v2[i] - v1[i] for i in range(3)))

