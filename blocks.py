from block import Block
from position import Position

class LBlock(Block):
    def __init__(self):
        super().__init__(id=1)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

    def clone(self):
        new_block = LBlock()
        new_block.rotation_state = self.rotation_state
        new_block.id = self.id
        new_block.cells = {rot: [Position(p.row, p.col) for p in self.cells[rot]] for rot in self.cells}
        return new_block

class JBlock(Block):
    def __init__(self):
        super().__init__(id=2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.move(0, 3)

    def clone(self):
        new_block = JBlock()
        new_block.rotation_state = self.rotation_state
        new_block.id = self.id
        new_block.cells = {rot: [Position(p.row, p.col) for p in self.cells[rot]] for rot in self.cells}
        return new_block

class IBlock(Block):
    def __init__(self):
        super().__init__(id=3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        self.move(-1, 3)

    def clone(self):
        new_block = IBlock()
        new_block.rotation_state = self.rotation_state
        new_block.id = self.id
        new_block.cells = {rot: [Position(p.row, p.col) for p in self.cells[rot]] for rot in self.cells}
        return new_block

class OBlock(Block):
    def __init__(self):
        super().__init__(id=4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
        }
        self.move(0, 4)

    def clone(self):
        new_block = OBlock()
        new_block.rotation_state = self.rotation_state
        new_block.id = self.id
        new_block.cells = {rot: [Position(p.row, p.col) for p in self.cells[rot]] for rot in self.cells}
        return new_block

class SBlock(Block):
    def __init__(self):
        super().__init__(id=5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

    def clone(self):
        new_block = SBlock()
        new_block.rotation_state = self.rotation_state
        new_block.id = self.id
        new_block.cells = {rot: [Position(p.row, p.col) for p in self.cells[rot]] for rot in self.cells}
        return new_block

class TBlock(Block):
    def __init__(self):
        super().__init__(id=6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

    def clone(self):
        new_block = TBlock()
        new_block.rotation_state = self.rotation_state
        new_block.id = self.id
        new_block.cells = {rot: [Position(p.row, p.col) for p in self.cells[rot]] for rot in self.cells}
        return new_block

class ZBlock(Block):
    def __init__(self):
        super().__init__(id=7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }
        self.move(0, 3)

    def clone(self):
        new_block = ZBlock()
        new_block.rotation_state = self.rotation_state
        new_block.id = self.id
        new_block.cells = {rot: [Position(p.row, p.col) for p in self.cells[rot]] for rot in self.cells}
        return new_block
