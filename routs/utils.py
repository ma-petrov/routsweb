class Bunch(dict):
    """
    Convert dict to object to use object.key instead of object['key']
    """

    __getattr__, __setattr__ = dict.get, dict.__setitem__