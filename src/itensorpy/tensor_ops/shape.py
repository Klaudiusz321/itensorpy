

class ShapeMixin:

    def transpose(self, axes):
        return self.__class__(self.data.transpose(axes))

    def reshape(self, new_shape):
        return self.__class__(self.data.reshape(new_shape))
