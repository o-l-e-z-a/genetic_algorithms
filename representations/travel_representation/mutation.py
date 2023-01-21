from base_mutation import BaseMutation
from service import get_random_indices


class MutationExchange(BaseMutation):
    """ Мутация обменом """

    def get_indices(self, indices):
        self._index_1, self._index_2 = indices if indices else get_random_indices(end=len(self.individual) - 1)

    def mutation(self):
        self.individual[self._index_1], self.individual[self._index_2] = \
            self.individual[self._index_2], self.individual[self._index_1]
