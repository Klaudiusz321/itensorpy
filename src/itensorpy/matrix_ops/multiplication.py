# multiplication.py

from sympy import MatrixError

class MultiplicationMixin:
   

    def matmul(self, other):
        
        if not hasattr(other, 'mat'):
            raise TypeError("other must be MatrixOps")
        return self.__class__(self.mat * other.mat)

    def inverse(self):
        
        try:
            inv = self.mat.inv()
        except MatrixError as e:
            raise ValueError(f"inverse: matrix is singular ({e})")
        return self.__class__(inv)
