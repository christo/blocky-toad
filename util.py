
def seq(n, thing) -> list:
    """
    return a list of n things or if things is a list, a list of an n times repeating pattern of them
    :param n: number of repeats
    :param thing: a list or single value
    :return: a flat list of n repeated
    """
    try:
        for x in thing:
            break
        return thing*n
    except TypeError:
        return [thing]*n
