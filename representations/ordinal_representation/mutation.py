from base_mutation import BaseMutation
from service import get_random_index


class SinglePointOrdinalMutation(BaseMutation):
    """ Одноточечная мутация для порядкового представления """

    def get_indices(self, indices):
        if indices:
            self._index, self._random_value = indices
        else:
            self._index = get_random_index(end=len(self.individual) - 1)
            self._random_value = get_random_index(end=len(self.individual) - self._index - 1)

    def mutation(self):
        self.individual[self._index] = self._random_value
