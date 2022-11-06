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
        return None

class BinaryTree:
    """
    This is the first tree of the k-ary trees, basically just 
    to get a hang of things. Once generalized, then this class
    will probably be deprecated.

    Attributes:
        levels (int): number of levels on the tree.
        minimum_height (float): value of the minima on the tree. Zero by default.
        pointnodes (list of PointNodes): all the PointNodes on the tree.
    """
    def __init__(self, levels, minimum_height = 0.0) -> None:
        """
        Constructor for the BinaryTree.

        Parameters:
            levels (int): number of levels on the tree.
            minimum_height (float): value of the y-coordinate for all the minima. Zero by default.
        """
        self.levels = levels
        self.minimum_height = minimum_height
        self.create_pointnodes()
        return None
    
    def create_pointnodes(self) -> None:
        
        return None

    def export_pointnodes(self) -> tuple:
        """
        Returns the x and y values of all the point nodes as separate lists.
        """
        
        # Collect the tuples
        tup_values = []
        for pn in self.pointnodes:
            tup_values.append( pn.position )
        
        # Sort them based on the xvalues
        tup_values.sort( key = lambda idx: tup_values.index(idx[0]) )
        
        # Export the x and y values separately as lists
        xvalues = []
        yvalues = []
        for tup in tup_values:
            xvalues.append(tup[0])
            yvalues.append(tup[1])
        
        return (xvalues, yvalues)