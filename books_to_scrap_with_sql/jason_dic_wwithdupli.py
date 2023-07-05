import json
python_obj = '{"a":  1, "a":  2, "a":  3, "a": 4, "b": 1, "b": 2}'

def p(n):
    print(n)
    r = {}
    for k, value in n:
        if k in r:
            if isinstance(r[k], list):
                r[k].append(value)
            else:
                r[k] = [r[k], value]
        else:
            r[k] = value
    return r
print(json.loads(python_obj, object_pairs_hook=p))
print(type(json.loads(python_obj, object_pairs_hook=p)))
