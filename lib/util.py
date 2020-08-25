def list_dictionary(arg=None, *args, **kwargs):
    for key, value in kwargs.items():
        try:
            for v in list_dictionary(key, **value):
                yield key,v
        except :
            yield key, str(value)
