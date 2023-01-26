def check_probability(probability: int) -> Exception | None:
    if probability > 100 or probability < 0:
        return ValueError('Probability mast have value in range(0, 101)')


def check_for_positive_int(number: int) -> Exception | None:
    if number < 1:
        return ValueError('Value must be greater than zero')
