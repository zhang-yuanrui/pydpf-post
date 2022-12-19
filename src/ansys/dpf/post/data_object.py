"""Module containing the ``DataObject`` class."""
from ansys.dpf.core.fields_container import FieldsContainer
import numpy as np  # Make sure that numpy is in the requirements

from ansys.dpf.post.errors import PandasImportError


class DataObject(FieldsContainer):
    """Exposes the fields container generated by a result provider."""

    def __init__(
        self, fields_container=None, server=None, mesh_scoping=None, columns=None
    ):
        """Wrap a FieldsContainer within a DataObject.

        Parameters
        ----------
        fields_container:
            :class:`ansys.dpf.core.fields_container.FieldsContainer`to wrap.
        server:
            DPF server to use.
        mesh_scoping:
            Scoping to use.
        columns:
            Columns to use.
        """
        self._fc = fields_container
        if columns:
            self._columns = columns

        if mesh_scoping:
            self._mesh_scoping = mesh_scoping

        super().__init__(fields_container._internal_obj, server)

    def __min__(self, **kwargs):
        """Return the minimum of the data."""
        return self.as_array().min()

    def __max__(self, **kwargs):
        """Return the maximum of the data."""
        return self.as_array().max()

    def max(self, **kwargs):
        """Return the maximum of the data."""
        return float(self.as_array().max())

    def min(self, **kwargs):
        """Return the minimum of the data."""
        return float(self.as_array().min())

    def as_data_frame(self, columns=None, **kwargs):
        """Returns the data from the field container as a Pandas data_frame.

        Parameters
        ----------
        columns :
            Columns description.

        Returns
        -------
        class:`pandas.core.frame.DataFrame`

        Examples
        --------
        >>> import pandas as pd
        >>> from ansys.dpf import post
        >>> from ansys.dpf.post import examples
        >>> solution = post.load_solution(examples.multishells_rst, legacy=False)
        >>> #stress = solution.stress()
        >>> #stress.xx.plot_contour(show_edges=False)

        >>> #data = stress.xx.get_data_at_field(0)
        >>> #data_frame = pd.DataFrame(data)

        >>> #data2 = [[0,1,2], [3,4,5], [6,7,8], [9,10,11]]
        >>> #columns = ['x', 'y', 'z']
        >>> #df = pd.DataFrame(data2, columns)
        >>> #df = df.transpose()
        """
        try:
            import pandas as pd
        except ModuleNotFoundError:
            raise PandasImportError
        # columns = None
        # for arg in args:
        #     columns.appends(arg)

        # #load data into a DataFrame object:
        # data_frame = pd.DataFrame(self.field(0), columns)
        # transposed = data_frame.transpose()
        if not columns:
            columns = self._columns
        return pd.DataFrame(
            self.as_array(), columns=columns, index=self._mesh_scoping.ids
        )

    def as_array(self):
        """Return the DataObject as a NumPy array."""
        return np.array(self._fc[-1].data)

    def plot(self, **kwargs):
        """Plot the result."""
        self._fc[-1].plot(**kwargs)

    def animate(self, **kwargs):
        """Animate the result.

        Returns
        -------
            The interactive plotter object used for animation.
        """
        return self._fc.animate(**kwargs)
