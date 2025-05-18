# curl.py

from sympy import diff, Matrix

class CurlMixin:
    """
    Mix-in providing curl calculation for 3D vector fields.
    """

    def curl(self):
        """
        Calculate the curl ∇×F for a 3D vector field F.
        Returns a sympy Matrix (3×1) representing the curl vector.
        """
        coords = self.coords
        F = self.f

        # sprawdź 3 wymiary
        if len(coords) != 3:
            raise ValueError(f"curl: requires exactly 3 coordinates, got {len(coords)}")

        # spróbujmy zamienić na listę trzech komponentów
        try:
            components = list(F)
        except TypeError:
            raise TypeError("curl: f must be an iterable of 3 sympy Expr")

        if len(components) != 3:
            raise ValueError(f"curl: requires exactly 3 field components, got {len(components)}")

        x, y, z = coords
        Fx, Fy, Fz = components

        return Matrix([
            diff(Fz, y) - diff(Fy, z),
            diff(Fx, z) - diff(Fz, x),
            diff(Fy, x) - diff(Fx, y),
        ])
