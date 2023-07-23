def check_probability(probability: int) -> int:
    if probability > 100 or probability < 0:
        raise ValueError('Probability mast have value in range(0, 101)')
    return probability


def check_for_positive_int(number: int) -> int:
    if number < 1:
        raise ValueError('Value must be greater than zero')
    return number
