"""Provides tools for placing geometrical shapes of blocks."""


from typing import Optional, Union, List, Iterable

from glm import ivec2, ivec3

from .vector_tools import Rect, Box, cylinder, fittingCylinder, line3D, lineSequence3D, rotateSizeXZ
from .block import Block
from .interface import Editor


def placeCuboid(editor: Editor, first: ivec3, last: ivec3, block: Block, replace: Optional[Union[str, List[str]]] = None):
    """Places a box of [block] blocks from [first] to [last] (inclusive)."""
    # Transform only the key points instead of all points
    first = editor.transform * first
    last = editor.transform * last
    block = block.transformed(editor.transform.rotation, editor.transform.flip)
    editor.placeBlockGlobal(Box.between(first, last).inner, block, replace)


def placeCuboidHollow(editor: Editor, first: ivec3, last: ivec3, block: Block, replace: Optional[Union[str, List[str]]] = None):
    """Places a hollow box of [block] blocks from [first] to [last] (inclusive)."""
    # Transform only the key points instead of all points
    first = editor.transform * first
    last = editor.transform * last
    block = block.transformed(editor.transform.rotation, editor.transform.flip)
    editor.placeBlockGlobal(Box.between(first, last).shell, block, replace)


def placeCuboidWireframe(editor: Editor, first: ivec3, last: ivec3, block: Block, replace: Optional[Union[str, List[str]]] = None):
    """Places a wireframe of [block] blocks from [first] to [last] (inclusive)."""
    # Transform only the key points instead of all points
    first = editor.transform * first
    last = editor.transform * last
    block = block.transformed(editor.transform.rotation, editor.transform.flip)
    editor.placeBlockGlobal(Box.between(first, last).wireframe, block, replace)


def placeBox(editor: Editor, box: Box, block: Block, replace: Optional[Union[str, List[str]]] = None):
    """Places a box of [block] blocks."""
    if (box.size.x == 0 or box.size.y == 0 or box.size.z == 0): return
    placeCuboid(editor, box.begin, box.end - 1, block, replace)


def placeBoxHollow(editor: Editor, box: Box, block: Block, replace: Optional[Union[str, List[str]]] = None):
    """Places a hollow box of [block] blocks."""
    if (box.size.x == 0 or box.size.y == 0 or box.size.z == 0): return
    placeCuboidHollow(editor, box.begin, box.end - 1, block, replace)


def placeBoxWireframe(editor: Editor, box: Box, block: Block, replace: Optional[Union[str, List[str]]] = None):
    """Places a wireframe of [block] blocks."""
    if (box.size.x == 0 or box.size.y == 0 or box.size.z == 0): return
    placeCuboidWireframe(editor, box.begin, box.end - 1, block, replace)


def placeRect(editor: Editor, rect: Rect, y: int, block: Block, replace: Optional[Union[str, List[str]]] = None):
    """Places a rectangle of blocks in the XY-plane, at height [y]"""
    placeBox(editor, rect.toBox(y, 1), block, replace)


def placeRectOutline(editor: Editor, rect: Rect, y: int, block: Block, replace: Optional[Union[str, List[str]]] = None):
    """Places the outline of a rectangle of blocks in the XY-plane, at height [y]"""
    placeBoxWireframe(editor, rect.toBox(y, 1), block, replace)


def placeCheckeredCuboid(editor: Editor, first: ivec3, last: ivec3, block1: Block, block2: Block = Block(""), replace: Optional[Union[str, List[str]]] = None):
    """Places a checker pattern of [block1] and [block2] in the box between [first] and [last] (inclusive)"""
    placeCheckeredBox(editor, Box.between(first, last), block1, block2, replace)


def placeCheckeredBox(editor: Editor, box: Box, block1: Block, block2: Block = Block(""), replace: Optional[Union[str, List[str]]] = None):
    """Places a checker pattern of [block1] and [block2] in [box]"""
    # We loop through [box]-local positions so that the pattern start is independent of [box].offset
    for pos in Box(size=box.size).inner:
        editor.placeBlock(box.offset + pos, block1 if sum(pos) % 2 == 0 else block2, replace)


def placeStripedCuboid(editor: Editor, first: ivec3, last: ivec3, stripeAxis: int, block1: Block, block2: Block = Block(""), replace: Optional[Union[str, List[str]]] = None):
    """Places a stripe pattern of [block1] and [block2] along [stripeAxis] (0, 1 or 2) in the box
    between [first] and [last] (inclusive)"""
    placeStripedBox(editor, Box.between(first, last), stripeAxis, block1, block2, replace)


def placeStripedBox(editor: Editor, box: Box, stripeAxis: int, block1: Block, block2: Block = Block(""), replace: Optional[Union[str, List[str]]] = None):
    """Places a stripe pattern of [block1] and [block2] along [stripeAxis] (0, 1 or 2) in [box]"""
    # We loop through [box]-local positions so that the pattern start is independent of [box].offset
    for pos in Box(size=box.size).inner:
        editor.placeBlock(box.offset + pos, block1 if pos[stripeAxis] % 2 == 0 else block2, replace)


def placeLine(editor: Editor, first: ivec3, last: ivec3, block: Block, width=1, replace: Optional[Union[str, List[str]]] = None):
    """Places a line of [block] blocks from [first] to [last] (inclusive).\n
    When placing axis-aligned lines, placeCuboid and placeBox are more efficient."""
    # Transform only the key points instead of all points
    first = editor.transform * first
    last = editor.transform * last
    block = block.transformed(editor.transform.rotation, editor.transform.flip)
    editor.placeBlockGlobal(line3D(first, last, width), block, replace)


def placeLineSequence(editor: Editor, points: Iterable[ivec3], block: Block, closed=False, replace: Optional[Union[str, List[str]]] = None):
    """Place lines that run from point to point."""
    editor.placeBlock(lineSequence3D(points, closed=closed), block, replace)


def placeCylinder(
    editor: Editor,
    baseCenter: ivec3, diameters: Union[ivec2, int], length: int,
    block: Block,
    axis=1, tube=False, hollow=False,
    replace: Optional[Union[str, List[str]]] = None
):
    """Place a cylindric shape centered on xyz with height and radius."""
    editor.placeBlock(cylinder(baseCenter, diameters, length, axis, tube, hollow), block, replace)


def placeFittingCylinder(
    editor: Editor,
    corner1: ivec3, corner2: ivec3,
    block: Block,
    axis=1, tube=False, hollow=False,
    replace: Optional[Union[str, List[str]]] = None
):
    """Place a cylindric shape that fills the entire region."""
    # Transform only the key points instead of all points
    corner1 = editor.transform * corner1
    corner2 = editor.transform * corner2
    block = block.transformed(editor.transform.rotation, editor.transform.flip)
    editor.placeBlockGlobal(fittingCylinder(corner1, corner2, axis, tube, hollow), block, replace)
