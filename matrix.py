import numpy as np

class Tensor:
    
    def __init__(self, dim, data):
        self.dimension = dim
        self.data = data

    def __str__(self):
        return str(self.data)
    

class Matrix(Tensor):
    def __init__(self, dim: tuple, data):

        if len(dim) == 2:
            self.rows, self.cols = dim
            dim = tuple(dim)
        else:
            raise ValueError('Wrong matrix dimensions')
        
        super().__init__(dim, data)

    def conv_rc2i(self, r: int, c: int) -> int:
        return r * self.cols + c

    def conv_i2rc(self, i:int) -> int:
        return (i // self.cols, i % self.cols)

    def __str__(self) -> str:
        if (not self.data):
            return "[]"
        output = "["
        longest = max(len(str(el)) for el in self.data)
        for i in range(self.rows):
            output += '\n'
            for j in range(self.cols):
                output += f"{self.data[self.conv_rc2i(i, j)] :> {longest + 2}}"
            output += '\n'
        output += ']'
        return output
    
    def parse_col_getitem(self, matrix, key):
        if (isinstance(key, int)):

            if (key < 0):
                key = matrix.cols + key
            if (key >= matrix.cols or key < 0):
                raise IndexError("Index out of range")
            
            return Matrix((matrix.rows, 1), matrix.data[key::matrix.cols])
        
        if (isinstance(key, slice)):
            
            start, stop, step = key.indices(matrix.cols)
            data = []
            count = 0
            for row in range(matrix.rows):
                count = 0
                for col in range(start, stop, step):
                    count += 1
                    data.append(matrix.data[matrix.cols * row + col])

            return Matrix((matrix.rows, count), data.copy())

        if (isinstance(key, list)):
            data = []
            for row in range(matrix.rows):
                for i in key:
                    if (i < 0):
                        i = matrix.cols + i
                    if (i > matrix.cols or i < 0):
                        raise IndexError("Index out of range")
                    data.append(matrix.data[row * matrix.cols + i])
            return Matrix((matrix.rows, len(key)), data)
        
        raise ValueError("Wrong argument type")

    def parse_row_getitem(self, matrix, key):
        if (isinstance(key, int)):

            if (key < 0):
                key = matrix.rows + key
            if (key >= matrix.rows or key < 0):
                raise IndexError("Index out of range")
            
            return Matrix((1, matrix.cols), matrix.data[matrix.cols * key : matrix.cols * (key + 1)])
        
        if (isinstance(key, slice)):

            start, stop, step = key.indices(matrix.rows)
            data = []
            count = 0
            for row in range(start, stop, step):
                count += 1
                data.extend(matrix.data[matrix.cols * row : matrix.cols * (row + 1)])
            return Matrix((count, matrix.cols), data.copy())
            
        if (isinstance(key, list)):
            data = []
            for i in key:
                if (i < 0):
                    i = matrix.rows + i
                if (i > matrix.rows or i < 0):
                    raise IndexError("Index out of range")
                data.extend(matrix.data[matrix.cols * i : matrix.cols * (i + 1)])
            return Matrix((len(key), matrix.cols), data)

        raise ValueError("Wrong argument type")

    def __getitem__(self, key):
        if (isinstance(key, tuple)):

            if (len(key) > 2):
                raise ValueError("Too many arguments")
            if (len(key) == 2 and isinstance(key[0], int) and isinstance(key[1], int)):
                row = key[0]
                col = key[1]
                if (row < 0):
                    row += self.rows
                if (col < 0):
                    col += self.cols
                if (row >= self.rows or col >= self.cols or row < 0 or col < 0):
                    raise IndexError("Index out of range")
                
                return self.data[self.conv_rc2i(row, col)]
        if (isinstance(key, list) or isinstance(key, slice) or isinstance(key, int)):
            return self.parse_row_getitem(self, key)

        return self.parse_col_getitem(self.parse_row_getitem(self, key[0]), key[1])
        

if __name__ == "__main__":
    arr = [i for i in range(0, 100)]

    m = Matrix((10, 10), arr)

    print(m[1, 1])
