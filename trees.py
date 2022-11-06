"""
Source code for generating points on a k-ary tree.

All trees are drawn in a 2D representation. That is,
their nodes are only defined spatially by 2 coordinates.
"""

class PointNode:
    """
    This is a class that defines the nodes on a 2D k-ary tree.

    Attributes:
        ismax (bool): Whether the PointNode is a local maximum or local minimum.
        position (Tuple): The (x, y) position of the node.
    """
    def __init__(self, ismax, xposition, yposition) -> None:
        """
        The constructor for the PointNode class.

        Parameters:
            ismax (bool): sets the ismax attribute
            xposition (number): sets the position[0] attribute
            yposition (number): sets the position[1] attribute
        """
        if not type(ismax) is bool:
            raise TypeError("ismax argument must be a boolean.")
        self.ismax = ismax
        self.position = (xposition, yposition)