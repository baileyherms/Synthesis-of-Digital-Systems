import sys
import os


def matrix_tableau(m, n, bounds, coefficients, matrix_A):
    tableau = []
    # Do a for loop with m + 1 = rows and n + m + 1 = columns so that you can add
    # the necessary numbers to the matrix tableau
    # May want to switch m and n
    for i in range(m + 1):
        temp = []
        for j in range(m + n + 1):
            temp.append(0)
        tableau.append(temp)
    for i in range(m):
        for j in range(n):
            tableau[i][j] = matrix_A[i][j]
    for j in range(n):
        tableau[m][j] = coefficients[j] * -1
    for i in range(m):
        tableau[i][m + n] = bounds[i]
    #print(tableau)

    s_array = []
    for i in range(m):
        temp = []
        for j in range(m):
            temp.append(0)
        s_array.append(temp)
    #print(s_array)
    for i in range(m):
        for j in range(m):
            if i == j:
                s_array[i][j] = 1
    #print(s_array)
    for i in range(m + 1):
        for j in range(m + n + 1):
            if i < m:
                if (j > n - 1) and (j < m + n):
                    #print("i: ", i)
                    #print("j: ", j)
                    tableau[i][j] = s_array[i][j - n]
    #print(tableau)
    return tableau

def optimality_check(m, n, tableau):
    # Do optimality check for matrix tableau
    for j in range(m + n + 1):
        if tableau[m][j] < 0.0:
            return False
    return True

def pivot_tableau(m ,n, tableau):
    # Do pivot stuff in matrix tableau
    min = tableau[m][0]
    min_pos = 0
    for j in range(m + n + 1):
        if tableau[m][j] < min:
            min = tableau[m][j]
            min_pos = j
    #print("min_pos", min_pos)
    corr_basis = []
    for i in range(m):
        corr_basis.append(tableau[i][min_pos])
    frac = []
    for i in range(m):
        if(tableau[i][min_pos] > 0):
            frac.append(tableau[i][m + n] / corr_basis[i])
        else:
            frac.append(-99) # to show that this value won't work, but keep the location in the tableau
    min_frac = 1000
    min_frac_pos = 50
    for i in range(len(frac)):
        if frac[i] < min_frac and frac[i] >= 0.0:
            min_frac = frac[i]
            min_frac_pos = i
    if(min_frac == 1000):
        output_file = open('simplex.out', 'w')
        output_file.write("+inf")
        output_file.close()
        sys.exit()
    pivot = tableau[min_frac_pos][min_pos]
    pivot_pos = min_frac_pos
    min_pos_table = []
    for i in range(m + 1):
        min_pos_table.append(tableau[i][min_pos])
    hold_tableau = tableau
    for i in range(m + 1):
        for j in range(m + n + 1):
            if i == pivot_pos:
                tableau[i][j] = (1 / pivot) * tableau[pivot_pos][j]
            """
            else:
                print("hold_tableau a", i, j, hold_tableau[i][j])
                hold_tableau[i][j] = tableau[i][j] - min_pos_table[i]*tableau[pivot_pos][j]
                print("hold_tableau b", i, j, hold_tableau[i][j])
            """
    for i in range(m + 1):
        for j in range(m + n + 1):
            if i != pivot_pos:
                tableau[i][j] = tableau[i][j] - min_pos_table[i]*tableau[pivot_pos][j]
    return tableau

def optimal_solution(m, n, tableau):
    c = tableau[m][m+n]
    return c

def x_values_array(m, n, tableau):
    x_array = []
    columns_pos = []
    for j in range(m + n):
        column = []
        for i in range(m + 1):
            column.append(tableau[i][j])
        if(sum(column) == 1):
            columns_pos.append(j)
        #print(column)
    #print("column_pos:", columns_pos)
    solutions = []
    for i in range(m + n):
        solutions.append(0)
    for i in range(m + 1):
        for j in range(m + n):
            if j in columns_pos and tableau[i][j] == 1.0:
                #print("tableau", i, j, tableau[i][j])
                solutions[j] = tableau[i][m + n]
    #print("Solutions:", solutions)
    for i in range(len(solutions)):
        if solutions[i] < 0:
            output_file = open('simplex.out', 'w')
            output_file.write("bounded-infeasible")
            output_file.close()
            sys.exit()
    x_array = []
    for i in range(n):
        x_array.append(solutions[i])
    #print("x_array:", x_array)
    return x_array

def main():
    # Main code goes here
    file_name = sys.argv[1]
    # print(file_name)
    file = open(file_name, 'r')
    m, n = [int(x) for x in next(file).split()]
    #print(m)
    #print(n)
    temp_list = []
    temp_list.append([float(x) for x in next(file).split()])
    bounds = temp_list[0]
    #print(bounds)
    temp_list[0] = [float(x) for x in next(file).split()]
    coefficients = temp_list[0]
    #print(coefficients)
    # Rows of the matrix
    matrix_A = []
    for i in range (m):
        temp_list[0] = [float(x) for x in next(file).split()]
        matrix_A.append(temp_list[0])
    file.close()
    #print(matrix_A)
    is_optimal = False
    #print("Round 1:")
    tableau = matrix_tableau(m, n, bounds, coefficients, matrix_A)
    #print("Tableau: ", tableau)
    # while(not is_optimal):
    is_optimal = optimality_check(m, n, tableau)
    #print(is_optimal)
    while(is_optimal == False):
        #print("Round 2:")
        tableau = pivot_tableau(m, n, tableau)
        #print("tests:", tableau)
        is_optimal = optimality_check(m, n, tableau)
        #print(is_optimal)
    # Delete below after adding while loop
    """
    print("------------------------")
    print("Round 3:")
    tableau = pivot_tableau(m, n, tableau)
    print("tests:", tableau)
    is_optimal = optimality_check(m, n, tableau)
    print("------------------------")
    print(is_optimal)
    """
    c = optimal_solution(m, n, tableau)
    x_values = x_values_array(m, n, tableau)
    #print(tableau)
    #print(c)
    output_file = open('simplex.out', 'w')
    output_file.write(str(c))
    output_file.write("\n")
    for i in range(n):
        #print(x_values[i])
        output_file.write(str(x_values[i]))
        output_file.write("\n")
    output_file.close()

if __name__ == "__main__":
    main()