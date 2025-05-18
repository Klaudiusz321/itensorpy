# linear_solve.py

from sympy import solve_linear_system, Matrix as _M

class LinearSolveMixin:
    

    def solve(self, b):
        
        # Zamieniamy b na kolumnową macierz
        if not hasattr(b, 'rows'):
            b = _M(b)
        if b.cols != 1 or b.rows != self.mat.rows:
            raise ValueError("solve: b must be a column vector of the same size as A")
        aug = self.mat.row_join(b)
        sol = solve_linear_system(aug, *self._symbols_for_vars())
        return sol

    def _symbols_for_vars(self):
        
        from sympy import symbols
        n = self.mat.cols
        return symbols(f'x0:{n}')
