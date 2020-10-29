

def list_dictionary(arg=None, *args, **kwargs):
    for key, value in kwargs.items():
        try:
            for v in list_dictionary(key, **value):
                yield key,v
        except :
            yield key, str(value)

def remove_exponent(num):
    try:
        return num.to_integral() if num == num.to_integral() else num.normalize()
    except AttributeError:
        return num

def to_str(num):
    try:
        return str(num.to_integral()) if num == num.to_integral() else str(num.normalize())
    except AttributeError:
        return str(num)