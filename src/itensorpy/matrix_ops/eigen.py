# eigen.py

class EigenMixin:
   

    def eigen(self):
        
        vals = self.mat.eigenvals()
        vecs = self.mat.eigenvects()
        # eigenvects() zwraca listę (value, multiplicity, [vectors])
        eigenvalues = list(vals.keys())
        eigenvectors = [v for (_, _, vec_list) in vecs for v in vec_list]
        return eigenvalues, eigenvectors
