menu_options = {1: 'Add matrices', 2: 'Multiply matrix by a constant',
                3: 'Multiply matrices', 4: 'Transpose matrix',
                5: 'Calculate a determinant', 6: 'Inverse matrix', 0: 'Exit'}

transp_options = {1: 'Main diagonal', 2: 'Side diagonal', 3: 'Vertical line',
                  4: 'Horizontal line'}

def get_mat_minor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def get_mat_det(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c] * get_mat_det(get_mat_minor(
            m,0,c))
    return determinant


class Matrix:
    def __init__(self, rowcols):
        i, j = input(rowcols).split()
        self.i = int(i)
        self.j = int(j)
        self.rows = []

    def get_data(self):
        for x in range(self.i):
            x = [float(x) for x in input().split()]
            self.rows.append(x)

    def matrix_print(self, mat):
        print('The result is:')
        for x in mat:
            print(*x)
        print("")

    def matrix_add(self, mat_b):
        if (self.i - mat_b.i) == 0 and (self.j - mat_b.j) == 0:
            output_mat = [[self.rows[i][j] + mat_b.rows[i][j] for j in range(
                len(self.rows[0]))] for i in range(len(self.rows))]

            self.matrix_print(output_mat)

        else:
            print('The operation cannot be performed.')

    def matrix_const(self):
        const = (float(input('Enter constant: ')))
        output_mat = [[const * self.rows[i][j] for j in range(self.j)]
                      for i in range(self.i)]
        self.matrix_print(output_mat)

    def matrix_multi(self, mat_b):
        if self.j == mat_b.i:
            output_mat = [[sum(i * j for i, j in zip(mat_a_row, mat_b_col))
                          for mat_b_col in zip(*mat_b.rows)] for
                          mat_a_row in
                          self.rows]

            self.matrix_print(output_mat)

        else:
            print('The operation cannot be performed.')

    def trans_main(self):
        output_mat = [[self.rows[j][i] for j in range(len(self.rows))] for
                      i in range(len(self.rows[0]))]
        self.matrix_print(output_mat)

    def trans_side(self):
        output_mat = [[self.rows[j][i] for j in range(len(self.rows))][::-1]
                      for i in range(len(self.rows[1]))[::-1]]
        self.matrix_print(output_mat)

    def trans_vert(self):
        output_mat = [j[::-1] for j in self.rows]
        self.matrix_print(output_mat)

    def trans_hor(self):
        output_mat = self.rows[::-1]
        self.matrix_print(output_mat)

    def mat_det(self):
        mat = self.rows
        if self.i != self.j:
            print("This operation cannot be performed")
        elif self.i == 1:
            self.matrix_print(mat)
        else:
            new = [list(map(float, mat[i])) for i in range(len(mat))]
            result = get_mat_det(new)
            print("The result is:")
            print(result)
            print("")

    def mat_inv(self):
        m = self.rows
        determinant = get_mat_det(m)
        # special case for 2x2 matrix:
        if len(m) == 2:
            return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                    [-1 * m[1][0] / determinant, m[0][0] / determinant]]

        # find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = get_mat_minor(m, r, c)
                cofactorRow.append(((-1) ** (r + c)) * get_mat_det(minor))
            cofactors.append(cofactorRow)
        # cofactors = transposeMatrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c] / determinant

        output_mat = [[cofactors[j][i] for j in range(len(cofactors))] for i in
                      range(len(cofactors[0]))]

        self.matrix_print(output_mat)


def main():
    while True:
        print(f'1. {menu_options[1]}\n'
              f'2. {menu_options[2]}\n'
              f'3. {menu_options[3]}\n'
              f'4. {menu_options[4]}\n'
              f'5. {menu_options[5]}\n'
              f'6. {menu_options[6]}\n'
              f'0. {menu_options[0]}')
        user_sel = int(input('Your choice: '))
        print("")

        try:
            if menu_options[user_sel] == 'Exit':
                break

            elif menu_options[user_sel] == 'Add matrices':
                matrix_a = Matrix('Enter size of first matrix: ')
                print('Enter first matrix: ')
                matrix_a.get_data()
                matrix_b = Matrix('Enter size of second matrix: ')
                print('Enter second matrix: ')
                matrix_b.get_data()
                matrix_a.matrix_add(matrix_b)

            elif menu_options[user_sel] == 'Multiply matrix by a constant':
                matrix_a = Matrix('Enter size of matrix: ')
                matrix_a.get_data()
                matrix_a.matrix_const()

            elif menu_options[user_sel] == 'Multiply matrices':
                matrix_a = Matrix('Enter size of first matrix: ')
                print('Enter first matrix')
                matrix_a.get_data()
                matrix_b = Matrix('Enter size of second matrix: ')
                print('Enter second matrix')
                matrix_b.get_data()
                matrix_a.matrix_multi(matrix_b)

            elif menu_options[user_sel] == 'Transpose matrix':
                print(f'1. Main diagonal\n'
                      f'2. Side diagonal\n'
                      f'3. Vertical line\n'
                      f'4. Horizontal line')

                trans_op = int(input("Your choice: "))
                print("")
                try:
                    if trans_op == 1:
                        matrix_a = Matrix('Enter matrix size: ')
                        print('Enter matrix: ')
                        matrix_a.get_data()
                        matrix_a.trans_main()

                    elif trans_op == 2:
                        matrix_a = Matrix('Enter matrix size: ')
                        print('Enter matrix: ')
                        matrix_a.get_data()
                        matrix_a.trans_side()

                    elif trans_op == 3:
                        matrix_a = Matrix('Enter matrix size: ')
                        print('Enter matrix: ')
                        matrix_a.get_data()
                        matrix_a.trans_vert()

                    elif trans_op == 4:
                        matrix_a = Matrix('Enter matrix size: ')
                        print('Enter matrix: ')
                        matrix_a.get_data()
                        matrix_a.trans_hor()

                except ValueError:
                    print('Invalid selection, please start again')

            elif menu_options[user_sel] == 'Calculate a determinant':
                matrix_a = Matrix('Enter matrix size: ')
                print('Enter matrix: ')
                matrix_a.get_data()
                matrix_a.mat_det()

            elif menu_options[user_sel] == 'Inverse matrix':
                matrix_a = Matrix('Enter matrix size: ')
                print('Enter matrix: ')
                matrix_a.get_data()
                matrix_a.mat_inv()


        except KeyError:
            print('Invalid selection, please try again.')


if __name__ == '__main__':
    main()
