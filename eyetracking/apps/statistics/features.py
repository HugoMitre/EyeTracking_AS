

def point_inside_polygon(x, y, poly):
    n = len(poly)

    if n==0:
        return False

    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


def get_data_shapes(shapes):

    data_shapes = []

    for shape in shapes:
        data = {}
        data['id'] = shape.id
        data['name'] = shape.name
        data['points'] = get_points(shape.top, shape.left, shape.width, shape.height)
        data['type'] = shape.type
        data['visit_count'] = 0
        data_shapes.append(data)

    return data_shapes


def get_points(top, left, width, height):

    points = []

    p1x = left
    p2x = left + width

    p1y = top
    p2y = top + height

    points.append((p1x, p1y))
    points.append((p1x, p2y))
    points.append((p2x, p1y))
    points.append((p2x, p2y))

    return points

