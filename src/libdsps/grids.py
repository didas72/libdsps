# noqa: D100

from math import ceil, cos, floor, radians, sin, sqrt

import solid as sp
import solid.utils as su


def _inner_hex(radius: float, height: float, fill_ratio: float) -> sp.OpenSCADObject:
    points = []
    for a in range(6):
        angle = radians(a * 60)
        x = cos(angle)
        y = sin(angle)
        points.append((x, y))

    hex_poly = su.polygon(points)
    outer = sp.scale((radius, radius, 1))(hex_poly)
    inner = sp.scale((1-fill_ratio, 1-fill_ratio, 1))(outer)
    hexagon = outer - inner
    return su.linear_extrude(height)(hexagon)


def hex_grid(width: float, length: float, height: float, stride: float, fill_ratio: float) -> sp.OpenSCADObject:
    """
    Generate a partially filled grid of hexagons.

    :param float width: Size in the X axis
    :param float length: Size in the Y axis
    :param float height: Size in the Z axis
    :param float stride: Size of hexagons
    :param float fill_ratio: Relative size of hexagon walls
    :return sp.OpenSCADObject: Generated grid, centered in X and Y, rests on Z=0
    """
    hex_radius = stride/2
    hex_sizex = hex_radius*3/2
    hex_sizey = hex_radius * sqrt(3)
    x_count = ceil(width / hex_sizex)
    y_count = ceil(length / hex_sizey)
    x_floor = floor(width / hex_sizex)
    y_floor = floor(length / hex_sizey)
    x_partial = width - x_floor * hex_sizex
    y_partial = length - y_floor * hex_sizey
    x_base = -width/2 + hex_sizex/2 + x_partial/2
    y_base = -length/2 + hex_sizey/2 + y_partial/2

    hexagon = _inner_hex(hex_radius, height, fill_ratio)
    hexs = []
    for x_i in range(-1, x_count):
        x = x_base + x_i * hex_sizex
        for y_i in range(-1, y_count):
            y = y_base + y_i * hex_sizey
            y += hex_sizey/2 if x_i % 2 == 0 else 0
            cur_hex = hexagon
            cur_hex = su.right(x)(cur_hex)
            cur_hex = su.forward(y)(cur_hex)
            cur_hex = su.color(((x_i+1) / (x_count+1), (y_i+1) / (y_count+1), 0))(cur_hex)
            hexs.append(cur_hex)

    grid = su.union()(*hexs)
    bounds = su.cube([width, length, height], center=True)
    bounds = su.up(height/2)(bounds)
    grid = grid * bounds
    return grid  # noqa: RET504



