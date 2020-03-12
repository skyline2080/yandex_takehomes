from collections import ChainMap

# implementing in a functional style leaving the initial tables intact

NULL = "NULL"

def left_update(t1, t2):
    return {k: (t1[k], NULL) for k in (t1.keys() - t2.keys())}

def right_update(t1, t2):
    return {k: (NULL, t2[k]) for k in (t2.keys() - t1.keys())}

def common_update(t1, t2):
    return {k: (t1[k], t2[k]) for k in (t1.keys() & t2.keys())}

def FULL(t1, t2):
    return dict(
        ChainMap(
            left_update(t1, t2),
            right_update(t1, t2),
            common_update(t1, t2)
        )
    )

def INNER(t1, t2):
    return common_update(t1, t2)

def LEFT_OUTER(t1, t2):
    return dict(
        ChainMap(
            left_update(t1, t2),
            common_update(t1, t2)
        )
    )