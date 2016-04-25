def lerp(v0, v1, t):
    return (1-t)*v0 + t*v1

def intlerp(v0, v1, t):
    return int(lerp(v0, v1, t))