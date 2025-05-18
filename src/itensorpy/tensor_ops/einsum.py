# src/itensorpy/tensor_ops/einsum.py

from collections import defaultdict
from sympy.tensor.array import tensorproduct, tensorcontraction
import numpy as np
import sympy as sp


def parse_einsum_pairs(input_notations, output_notation):
    
    # 1) obliczamy offsety, czyli od jakiego numeru zaczyna się każda tablica
    offsets = []
    off = 0
    for labels in input_notations:
        offsets.append(off)
        off += len(labels)

    # 2) zliczamy wszystkie wystąpienia każdej litery
    occ = defaultdict(list)  # letter -> [ (tensor_idx, pos_in_tensor), ... ]
    for tensor_idx, labels in enumerate(input_notations):
        for pos, letter in enumerate(labels):
            occ[letter].append((tensor_idx, pos))

    # 3) każdy letter, który występuje dokładnie dwa razy i nie jest w output, kontraktujemy
    pairs = []
    for letter, locs in occ.items():
        if len(locs) == 2 and letter not in output_notation:
            (t1, p1), (t2, p2) = locs
            axis1 = offsets[t1] + p1
            axis2 = offsets[t2] + p2
            pairs.append((axis1, axis2))

    return pairs


class EinsumMixin:
    
    def einsum_product(self, subscripts, *operands):
        """
        Perform an Einstein summation operation between this tensor and others.
        
        Args:
            subscripts: A string with the subscripts for summation (like "ij,jk->ik")
            *operands: Other TensorND objects to contract with
            
        Returns:
            TensorND: Result of the einsum operation
        """
        # Convert all inputs to numpy arrays for the einsum operation
        np_arrays = [self.to_numpy()]
        for op in operands:
            if not hasattr(op, 'to_numpy'):
                raise TypeError("All operands must be TensorND instances")
            np_arrays.append(op.to_numpy())
            
        # Perform the einsum operation
        result_np = np.einsum(subscripts, *np_arrays)
        
        # Convert back to a TensorND
        return self.__class__(result_np)
    
    def einsum_reduce(self, subscripts):
        """
        Perform an Einstein summation reduction operation on this tensor alone.
        
        Args:
            subscripts: A string with the subscripts for reduction (like "ii->")
            
        Returns:
            TensorND or scalar: Result of the einsum operation
        """
        result_np = np.einsum(subscripts, self.to_numpy())
        
        # If the result is a scalar, return it directly
        if isinstance(result_np, (int, float, complex, np.number)):
            return result_np
            
        # Otherwise, convert back to a TensorND
        return self.__class__(result_np)

    def einsum(self, notation, *others):
        # 1) rozbijamy notację wejście/wyjście
        try:
            lhs, rhs = notation.split('->')
        except ValueError:
            raise ValueError("Notacja musi zawierać '->', np. 'ij,jk->ik'")
        input_notations = lhs.split(',')
        output_notation = rhs.strip()

        # 2) zbieramy dane wszystkich tensorów
        arrays = [self.data] + [o.data for o in others]

        # 3) tworzymy produkt tensora
        prod = arrays[0]
        for arr in arrays[1:]:
            prod = tensorproduct(prod, arr)

        # 4) wyznaczamy pary osi do skwantowania, teraz z output
        pairs = parse_einsum_pairs(input_notations, output_notation)

        # 5) wykonujemy kontrakcję, rozpakowując listę par
        result = tensorcontraction(prod, *pairs)

        # 6) zwracamy nowy TensorND tej samej klasy
        return self.__class__(result)
