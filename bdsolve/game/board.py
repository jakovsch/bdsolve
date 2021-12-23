import numpy as np
from bdsolve.game.utils import runs1d, runs2d

class Board:
    '''
    The game board, a square matrix of size 's'.

    The board is further divided into subsets:
    rows, columns and blocks (square sub-matrices of size 'bs')
    Individual elements of the board are either empty or occupied
    by a piece, though placing a piece over another is allowed.
    Completely occupied subsets can be reduced (emptied), giving a score.

    TODO: globally cache pairs of (board state, statistical property)
          to reduce unnecessary computation of the same values.
    '''

    def __init__(self, s=9, bs=3):
        self.s = s
        self.bs = bs
        self.bw = s//bs
        self.board = np.zeros(shape=(s, s), dtype=np.int8)

    def reset(self):
        '''
        Set all elements to zero.
        '''
        self.board *= 0

    def copy(self):
        '''
        Return a new board object with identical state.
        '''
        b = Board(self.s, self.bs)
        b.board = self.board.copy()
        return b

    def place(self, piece, pos):
        '''
        Place a piece onto the board at position (y, x).
        Returns count of piece elements placed (score).
        '''
        y, x = piece.shape
        i, j = pos
        self.board[i:i+y, j:j+x] += piece
        return np.count_nonzero(piece)

    def reduce_subsets(self):
        '''
        Empty occupied subsets, if any.
        Returns count of zeroed elements * 2 per subset (score).
        Overlapping subsets are scored independently.
        '''
        count = 0
        for i in range(self.s):
            r = self.row(i).copy()
            c = self.col(i).copy()
            b = self.block(i).copy()
            if r.all():
                br = self.row(i)
                br *= 0
                count += self.s*2
            if c.all():
                bc = self.col(i)
                bc *= 0
                count += self.s*2
            if b.all():
                bb = self.block(i)
                bb *= 0
                count += (self.bs**2)*2
        return count

    def row(self, i):
        '''
        The i-th row. (reference, not a copy)
        '''
        return self.board[i, :]

    def col(self, i):
        '''
        The i-th column. (reference, not a copy)
        '''
        return self.board[:, i]

    def block(self, i):
        '''
        The i-th block. (reference, not a copy)
        '''
        bs, bw = self.bs, self.bw
        y, x = divmod(i, bw)
        return self.board[y*bs:(y+1)*bs, x*bs:(x+1)*bs]

    @property
    def occupation(self):
        '''
        Ratio of all occupied elements and board area.
        '''
        return np.round(np.count_nonzero(self.board) / (self.s**2), 2)

    @property
    def subset_occupation(self):
        '''
        Ratio of occupied subsets and num. of subsets.
        '''
        res = 0
        for i in range(self.s):
            res += self.row(i).all()
            res += self.col(i).all()
            res += self.block(i).all()
        return np.round(res / (3 * self.s), 2)

    @property
    def row_integrity(self):
        '''
        Statistic measuring the integrity of all rows,
        taking into account the sizes of free regions.
        '''
        s = self.s
        val = 0
        res = np.zeros(s+1)
        for i in range(s):
            res[runs1d(self.row(i))] += 1
        for i in range(1, res.size):
            val += (s+1-i) * res[i]
        return np.round(val / (45 * s), 2)

    @property
    def col_integrity(self):
        '''
        Statistic measuring the integrity of all columns,
        taking into account the sizes of free regions.
        '''
        s = self.s
        val = 0
        res = np.zeros(s+1)
        for i in range(s):
            res[runs1d(self.col(i))] += 1
        for i in range(1, res.size):
            val += (s+1-i) * res[i]
        return np.round(val / (45 * s), 2)

    @property
    def block_integrity(self):
        '''
        Statistic measuring the integrity of all blocks,
        taking into account the sizes of free regions.
        '''
        s = self.s
        val = 0
        res = np.zeros(s+1)
        for i in range(s):
            res[runs2d(self.block(i))] += 1
        for i in range(1, res.size):
            val += (s+1-i) * res[i]
        return np.round(val / (45 * s), 2)

    @property
    def integrity(self):
        '''
        Statistic measuring overall board integrity,
        taking into account the sizes of free regions.
        Similar to 'block_integrity' but considers boundaries
        between blocks and diagonally separated regions.
        '''
        s = self.s
        val = 0
        res = np.zeros(s**2+1)
        res[runs2d(self.board, diagonal=True)] += 1
        for i in range(1, res.size):
            val += ((s**2+1)-i) * res[i]
        return np.round(val / (45 * (s**2)), 2)
