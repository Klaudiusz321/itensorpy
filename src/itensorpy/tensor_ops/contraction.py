from sympy.tensor.array import tensorcontraction


class ContractionMixin:

    def contract(self, *pairs):
        contracted = tensorcontraction(self.data, pairs)
        return self.__class__(contracted)
