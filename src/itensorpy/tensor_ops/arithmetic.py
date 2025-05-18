# src/itensorpy/tensor_ops/arithmetic.py

from sympy.tensor.array import tensorproduct

class ArithmeticMixin:
    """
    Mix-in: element-wise add/sub/mul/div dla tensorów tego samego kształtu,
    oraz tensorprodukt @.
    """

    def _check_shape_match(self, other):
        if self.shape != other.shape:
            raise ValueError(
                f"Shape mismatch: {self.shape} vs {other.shape}"
            )

    def __add__(self, other):
        self._check_shape_match(other)
        return self.__class__(self.data + other.data)

    def __sub__(self, other):
        self._check_shape_match(other)
        return self.__class__(self.data - other.data)

    def __mul__(self, other):
        # tensor * tensor (elementwise) albo tensor * skalar
        if hasattr(other, 'data'):
            self._check_shape_match(other)
            return self.__class__(self.data * other.data)
        else:
            return self.__class__(self.data * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        # tensor / tensor (elementwise) albo tensor / skalar
        if hasattr(other, 'data'):
            self._check_shape_match(other)
            return self.__class__(self.data / other.data)
        else:
            return self.__class__(self.data / other)

    def __matmul__(self, other):
        # zawsze tensorprodukt, wspiera dowolne wymiary
        return self.__class__(tensorproduct(self.data, other.data))
