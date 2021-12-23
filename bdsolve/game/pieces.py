import numpy as np
from random import choice
from bdsolve.game.utils import hashset_ndarray

_pieces = [
    # Dot
    [
        [1]
    ],
    # Square
    [
        [1,1],
        [1,1]
    ],
    # Corner 2
    [
        [1,1],
        [0,1]
    ],
    # Corner 3
    [
        [1,1,1],
        [0,0,1],
        [0,0,1]
    ],
    # Diagonal 2
    [
        [1,0],
        [0,1]
    ],
    # Diagonal 3
    [
        [1,0,0],
        [0,1,0],
        [0,0,1]
    ],
    # Plus
    [
        [0,1,0],
        [1,1,1],
        [0,1,0]
    ],
    # Line 2
    [
        [1,1]
    ],
    # Line 3
    [
        [1,1,1]
    ],
    # Line 4
    [
        [1,1,1,1]
    ],
    # Line 5
    [
        [1,1,1,1,1]
    ],
    # T 2
    [
        [1,1,1],
        [0,1,0]
    ],
    # T 3
    [
        [1,1,1],
        [0,1,0],
        [0,1,0]
    ],
    # U
    [
        [1,1,1],
        [1,0,1]
    ],
    # S Left
    [
        [0,1,1],
        [1,1,0]
    ],
    # S Right
    [
        [1,1,0],
        [0,1,1]
    ],
    # L Left
    [
        [1,1,1],
        [1,0,0]
    ],
    # L Right
    [
        [1,1,1],
        [0,0,1]
    ]
]

all_pieces = hashset_ndarray([
    np.rot90(np.array(p, dtype=np.int8), i)
    for i in range(4)
    for p in _pieces
])

def get_occupation(p):
    '''
    Ratio of piece element count and the area of its shape.
    '''
    return np.round(np.count_nonzero(p) / np.product(p.shape), 2)

def get_random3():
    '''
    Pick 3 random pieces.
    '''
    return list(choice(all_pieces) for _ in range(3))
