def bresenham(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    x_sign = 1 if dx > 0 else -1
    y_sign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = x_sign, 0, 0, y_sign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, y_sign, x_sign, 0

    D = 2*dy - dx
    y = 0

    tab = []
    for x in range(dx + 1):
        tab.append([x0 + x*xx + y*yx, y0 + x*xy + y*yy])
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy
    
    return tab

