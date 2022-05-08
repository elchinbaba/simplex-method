class Matrix:
    def __init__(self, n, m, matrix) -> None:
        self.n = n
        self.m = m
        self.matrix = matrix

    def change_basis(self, p, q):
        a_p_q = self.matrix[p][q]
        # print(f'p={p} q={q}')
        # for l in self.matrix:
        #     print(l)
        # print(self.matrix[p][q])
        # print(f'a_pq={a_p_q}')
        for i in range(self.n):
            self.matrix[p][i] /= a_p_q

        for i in range(self.m):
            if i != p:
                a_i_q = self.matrix[i][q]
                for j in range(self.n):
                    self.matrix[i][j] -= a_i_q*self.matrix[p][j]

class Simplex:
    def __init__(self, n, m, A_matrix, B_vector, c_vector, plan) -> None:
        self.n = n
        self.m = m
        self.A_matrix = A_matrix
        self.B_vector = B_vector
        self.c_vector = c_vector
        self.plan = plan
        self.calculate()
    
    def calculate(self):
        self.z_vector = []
        for i in range(self.n):
            self.z_vector.append(0)
            for j in range(self.m):
                self.z_vector[i] += self.A_matrix[j][i]*self.c_vector[self.plan[j] - 1]
            self.z_vector[i] -= self.c_vector[i]

        self.z_B = 0
        for k in range(self.m):
            self.z_B += self.B_vector[k]*self.c_vector[self.plan[k] - 1]
        
        self.simplex_matrix = []
        for j in range(self.m):
            mat = [x for x in self.A_matrix[j]]
            mat.insert(0, self.B_vector[j])
            self.simplex_matrix.append(mat)
        mat = [x for x in self.z_vector]
        mat.insert(0, self.z_B)
        self.simplex_matrix.append(mat)
        self.simplex_matrix = Matrix(self.n + 1, self.m + 1, self.simplex_matrix)
    
    def update_q(self):
        vector = self.z_vector
        max_ind = 0
        for i in range(1, self.n):
            if vector[i] > vector[max_ind] and vector[i] > 0:
                max_ind = i
        self.q = max_ind + 1

    def update_p(self):
        vector_b = self.B_vector
        # print(f'B={vector_b}')
        vector_A_i_q = [self.A_matrix[i][self.q - 1] for i in range(self.m)]
        # print(f'A_iq={vector_A_i_q}')
        vector = [vector_b[i]/vector_A_i_q[i] for i in range(self.m)]
        min_ind = 0
        for i in range(1, self.m):
            if vector[i] < vector[min_ind] and vector_A_i_q[i] > 0:
                min_ind = i
        self.p = min_ind

    def is_solution(self):
        for j in range(self.n):
            if self.z_vector[j] > 0:
                return False
        return True

    def no_solution(self):
        for j in range(self.n):
            if self.z_vector[j] > 0:
                check = True
                for i in range(self.m):
                    if self.A_matrix[i][j] > 0:
                        check = False
                        break
                if check == True:
                    return True

    def recalculate(self):
        matrix = self.simplex_matrix.matrix
        self.B_vector = [matrix[i][0] for i in range(self.m)]
        for i in range(self.m):
            for j in range(self.n):
                self.A_matrix[i][j] = matrix[i][j + 1]
        # self.A_matrix = [[matrix[i] for i in range(1, self.m)][j] for j in range(1, self.n)]
        # print(f'A={self.A_matrix}')
        # self.z_vector = [matrix[self.m][j] for j in range(1, self.n)]
        self.z_vector = matrix[self.m][1:self.n + 1]
        # print(f'z={self.z_vector}')
        self.z_B = matrix[self.m][0]
        # print(f'z_B={self.z_B}')
        # print()


    def find_min(self):
        i = 0
        while not self.is_solution():
            print(f'i={i}\n')
            i += 1
            if self.no_solution():
                return None
            self.update_q()
            self.update_p()

            print(self.p, self.q)
            print()

            self.simplex_matrix.change_basis(self.p, self.q)
            self.recalculate()

            for l in self.simplex_matrix.matrix:
                print(l)

            print()

            # if i == 10: break
        return self.simplex_matrix.matrix

a_matrix = [
    [1,2,1,0],
    [0,1,2,1]
]

b_vector = [8,6]

c_vector = [4,3,-1,-1]

simplex = Simplex(4, 2, a_matrix, b_vector, c_vector, [1,4])
matrix = simplex.find_min()

for l in matrix:
    print(l)