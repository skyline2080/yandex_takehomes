import itertools
import copy
from pprint import pprint

# beware changing the source json dict in-place
# mk defensive cpy like in test below 

def _is_empty_list(v):
    return isinstance(v, list) and not(v)

def _is_empty_dict(v):
    return isinstance(v, dict) and not(v)

def _is_dict(v):
    return isinstance(v, dict)

def _is_list(v):
    return isinstance(v, list)

def gen_empty_entities_dict(d):
    for k, v in d.items():
        if _is_empty_list(v) or _is_empty_dict(v):
            yield d, k 
        if _is_dict(v): # assuming dict is non-empty at this point
            yield from gen_empty_entities_dict(v)
        if _is_list(v): # assuming list is non-empty at this point
            yield from gen_empty_entities_list(v)

def gen_empty_entities_list(ls):
    for i, v in enumerate(ls):
        if _is_empty_list(v) or _is_empty_dict(v):
            yield ls, i 
        if _is_dict(v): # assuming dict is non-empty at this point
            yield from gen_empty_entities_dict(v)
        if _is_list(v): # assuming list is non-empty at this point
            yield from gen_empty_entities_list(v)

def procces_empty_entities(gen, action):
    for container, element in gen:
        action(container, element)

def report(container, element):
    print(f"element {element} is empty >> parent container {container}")

def delete(container, element):
    del container[element]

def test():
    dict_cpy = copy.deepcopy(test_d)
    gen = gen_empty_entities_dict(dict_cpy)
    gen1, gen2 = itertools.tee(gen)

    procces_empty_entities(gen1, report)
    procces_empty_entities(gen2, delete)

    print("initial json")
    pprint(test_d)
    print("revised one")
    pprint(dict_cpy)


test_d = {
    "a": 1,
    "b": [],
    "c": [1,2,3],
    "d":{
        "a1": {},
        "b1": [1, []],
        "c1": 1,
        "d1": [{}, {"d2": 2}]
    }
}