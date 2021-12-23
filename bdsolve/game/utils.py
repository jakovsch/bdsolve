import numpy as np

def hashset_ndarray(ls):
    '''
    Deduplicate a list of ndarray objects.
    '''
    return list({
        (arr.shape, arr.data.tobytes()): arr
        for arr in ls
    }.values())

def runs1d(arr, val=0):
    '''
    Find bounded runs of 'val' in a 1D array.
    Returns a list of run sizes.
    '''
    runs = np.where(np.abs(np.diff(
        np.concatenate(
            ([0], np.equal(arr, val).view(np.int8), [0])
        )
    )) == 1)[0].reshape(-1, 2)
    return runs[:, 1] - runs[:, 0]

def runs2d(arr, val=0, diagonal=False):
    '''
    Find bounded runs/regions of 'val' in a 2D array.
    Optionally merge runs sharing a vertex but not an edge.
    Returns a list of run sizes.

    Note: ~quadratic time complexity.
    '''
    runs = []
    tr = np.zeros(arr.shape)
    i, j = 0, 0
    for j in range(arr.shape[0]):
        for i in range(arr.shape[1]):
            if tr.all(): return runs
            if tr[i, j] or arr[i, j] != val:
                continue
            res, st = 0, []
            st.append((i, j))
            while st:
                i, j = st.pop()
                if not tr[i, j]:
                    tr[i, j] = 1
                    if arr[i, j] == val:
                        res += 1
                        li = i < arr.shape[0]-1
                        lj = j < arr.shape[1]-1
                        if li: st.append((i+1, j))
                        if lj: st.append((i, j+1))
                        if diagonal and li and lj:
                            st.append((i+1, j+1))
            if res: runs.append(res)
    return runs
