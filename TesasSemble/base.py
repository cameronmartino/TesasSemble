from abc import abstractmethod


class _BaseRedBlueFastq(object):

    """Base class for fastg to redbluegraphs
    Warning: This class should not be used directly.
    Use derived classes instead.
    """

    @abstractmethod
    def fit(self):
        """ Placeholder for fit this
        should be implemetned by sub-method"""

    def condition_graph(self, cond):
        """ get each condition after fitting"""

        if cond not in self.cond_graphs.keys():
            raise ValueError('Condition is not in input ',
                             'conditions: must be one of '
                             + ' '.join(self.conditions))

        return self.cond_graphs[cond]

    def leftout_rest_graph(self, cond):
        """ return a RedBlueDiGraph
        """
        return self.rest_leftout[cond]

    def node_map(self):
        """ return a node labels in fatsa
            type format
        """
        return {y: x for x, y in self.nodes.items()}
