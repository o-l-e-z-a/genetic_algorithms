import abc
import random
from typing import MutableSequence, Any

from form_genes_with_greedy_heuristics import FormStartGenes


class BaseIndividual(abc.ABC):
    """ Базовое представление особи"""

    def __init__(self, genes: MutableSequence[Any] | None = None, genes_length: int = 0):
        self._genes = list(genes) if genes else [0 for i in range(genes_length)]

    def __repr__(self):
        return f'{self._genes}'

    def __getitem__(self, key):
        return self._genes[key]

    def __setitem__(self, key, value):
        self._genes[key] = value

    def __len__(self):
        return len(self._genes)

    def __eq__(self, other):
        return self._genes == list(other)

    @property
    def genes(self):
        return self._genes

    def set_genes(self, genes):
        # Задать новые гены
        self._genes = list(genes)

    @abc.abstractmethod
    def set_initial_genes(self):
        """ Задать начальные гены"""


class IndividualWithRandomInitialGenes(BaseIndividual):
    """ Особь со случайными начальными генами"""

    def set_initial_genes(self):
        random_list = list(range(len(self)))
        random.shuffle(random_list)
        self._genes = random_list


class IndividualWithFormedInitialGenes(BaseIndividual):
    """ Особь с начальными генами, сформированными с помощью жадных эвристик"""

    def __init__(self, matrix, key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.matrix = matrix
        self.key = key

    def set_initial_genes(self):
        form_start_genes = FormStartGenes(self.key, self.matrix, self)
        self._genes = form_start_genes.get_formed_initial_genes()
