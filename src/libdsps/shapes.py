# noqa: D100

import solid2 as sp

XX = 2

def rect_frame(width: float, length: float, height: float, frame_size: float) -> sp.OpenSCADObjectPlus:
    """
    Generate a rectangular frame.

    :param float width: Size in the X axis
    :param float length: Size in the Y axis
    :param float height: Size in the Z axis
    :param float frame_size: Size of each frame side
    :return sp.OpenSCADObject: Generated grid, centered in X and Y, rests on Z=0
    """
    frame = sp.cube([width, length, height], center=True)
    mask = sp.cube([width - frame_size*2, height - frame_size*2, height+XX], center=True)
    frame = frame - mask
    frame = sp.up(height/2)(frame)
    return frame  # noqa: RET504
