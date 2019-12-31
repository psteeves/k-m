import numpy as np
import abc


class BaseSimilarity:
    @abc.abstractmethod
    def compare(self, x, y):
        pass

    def __call__(self, x, y):
        return self.compare(x, y)


class EuclidianSimilarity(BaseSimilarity):
    def compare(self, x, y):
        return np.linalg.norm(x - y)