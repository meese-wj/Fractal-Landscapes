"""
Source code for generating points on a k-ary tree.

All trees are drawn in a 2D representation. That is,
their nodes are only defined spatially by 2 coordinates.

One should essentially only use the TreeLandscape class 
to interface with this code. I see no reason to use the 
other classes directly at this point...
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

    def __str__(self) -> str:
        """
        Print representation string for the PointNode class.
        """
        maxstr = "max"
        if not self.ismax:
            maxstr = "min"
        return "PointNode (" + maxstr + ") at (" + str(self.position[0]) + ", " + str(self.position[1]) + ")"

class BinaryTree:
    """
    This is the first tree of the k-ary trees, basically just 
    to get a hang of things. Once generalized, then this class
    will probably be deprecated.

    Attributes:
        base (int): the k of the k-ary. For this tree is is always 2.
        levels (int): number of levels on the tree.
        minimum_height (float): value of the minima on the tree. Zero by default.
        level_height (float): step value to separate levels on the tree. 1 by default.
        pointnodes (list of PointNodes): all the PointNodes on the tree.
    """
    def __init__(self, levels, minimum_height = 0.0, level_height = 1.0) -> None:
        """
        Constructor for the BinaryTree.

        Parameters:
            levels (int): number of levels on the tree.
            minimum_height (float): value of the y-coordinate for all the minima. Zero by default.
            level_height (float): constant vertical shift between levels. 1.0 by default.
        """
        if (not type(levels) is int) or levels <= 0:
            raise ValueError("The number of levels must be a positive integer.")

        self.base = 2
        self.levels = levels
        self.minimum_height = minimum_height
        self.level_height = level_height
        self.create_pointnodes()
        return None

    def total_height(self) -> float:
        print(self.levels, self.level_height)
        return (self.levels + 1) * self.level_height

    def total_width(self) -> float:
        return self.base**(self.levels)

    def nodes_per_level(self, level):
        return self.base**level
    
    def create_pointnodes(self) -> None:
        self.pointnodes = [ PointNode(True, 0.0, self.total_height()) ]
        
        # Start at the bottom and build up
        current_level = self.levels
        # Collect a list of lists for the PointNodes
        # on each level.
        level_nodes = []
        while current_level > 0:
            current_nodes = []
            if current_level == self.levels:
                # The minimum levels have positions that 
                # can most easily be established, so we
                # start here.
                half_nodes = self.nodes_per_level(current_level) // self.base
                for ndx in range(0, self.nodes_per_level(current_level)):
                    xpos = -0.5 * self.total_width() + ndx
                    if ndx >= half_nodes:
                        # Switch up the spacing around x = 0.0 to provide padding and
                        # inversion symmetry along x.
                        xpos = ndx % half_nodes + 1.0
                    ypos = self.minimum_height
                    current_nodes.append( PointNode(True, xpos, ypos) )
            else:
                # Now for each level above the minimum, we can find the
                # x positions from the averages of the daughter nodes
                daughter_nodes = level_nodes[self.levels - (current_level + 1)]
                num_daughters = len(daughter_nodes)
                for ndx in range(0, self.nodes_per_level(current_level)):
                    # Map the current ndx index to the daughter indices
                    left_index = self.base * ndx
                    right_index = left_index + 1
                    # Average the daughter x positions
                    xpos = ( daughter_nodes[left_index].position[0] + daughter_nodes[right_index].position[1] ) / self.base
                    # Add the level_height to the daughter y position
                    ypos = daughter_nodes[left_index].position[0] + self.level_height
                    current_nodes.append( PointNode(False, xpos, ypos) )

            level_nodes.append(current_nodes)
            current_level -= 1

        # Add all nodes from the level_nodes to the position nodes
        # Note that they *will be* out of x-order!
        for lvl in level_nodes:
            for pn in lvl:
                self.pointnodes.append(pn)
         
        return None

    def export_pointnode_coordinates(self) -> list:
        """
        Return a sorted tuple of the PointNode coordinates from the
        binary tree. The sort is performed such that the x coordinates
        are ordered.
        """
        # Collect the tuples
        tup_values = []
        for pn in self.pointnodes:
            tup_values.append( pn.position )
        
        # Sort them based on the xvalues
        tup_values.sort( key = lambda tup: tup[0] )
        
        return tup_values
        

class TreeLandscape:
    """
    Class that converts a k-ary tree structure into a well-defined energy landscape.

    Attributes:
        boundary_factor (float): the factor by which the boundary points (which are global maxima) are greater than tree's total height
        tree (k-ary tree): the k-ary tree that defines a set of PointNodes.
            * A k-ary tree must have the following attributes: levels, minimum_height, level_height
            * A k-ary tree must have the following members: total_height(), export_pointnode_coordinates()
    """
    def __init__(self, treeclass = BinaryTree, levels = 3, minimum_height = 0.0, level_height = 1.0, boundary_factor = 2.0) -> None:
        """
        Constructor for the TreeLandscape class

        Parameters:
            treeclass (class): Type of tree that should be used to build the landscape. Defaults to BinaryTree.
            levels (int): Number of levels to give the treeclass. Defaults to 3.
            minimum_height (float): Value of the y-coordinate for all the minima. Defaults to 0.0.
            level_height (float): Constant vertical shift between levels. Defaults to 1.0.
            boundary_factor (float): Numerical factor by which the boundary global maxima are greater than the tree's maximum. Defaults to 2.0.
        """
        if boundary_factor <= 1.0:
            raise ValueError("The boundary_factor must be greater than 1.0 for a well-defined energy landscape.")

        self.boundary_factor = boundary_factor
        self.tree = treeclass(levels, minimum_height, level_height)
        return None
        
    def export_landscape(self) -> tuple:
        """
        Returns the x and y values of all the point nodes as separate lists.

        This function also attaches the global maximizing endpoints to make
        the energy-landscape well-defined.

        One should use this function to quickly generate the landscape.
        """
        tup_values = self.tree.export_pointnode_coordinates()

        # Insert the global maxima with the same x-distance as defined by the BinaryTree part
        left_xpos = tup_values[0][0] - (tup_values[1][0] - tup_values[0][0])
        right_xpos = tup_values[-1][0] + (tup_values[-1][0] - tup_values[-2][0])
        global_max = self.boundary_factor * (self.tree.minimum_height + self.tree.total_height())
        tup_values.insert(0, (left_xpos, global_max))
        tup_values.append( (right_xpos, global_max) )

        # Export the x and y values separately as lists
        xvalues = []
        yvalues = []
        for tup in tup_values:
            xvalues.append(tup[0])
            yvalues.append(tup[1])
        
        return (xvalues, yvalues)
        