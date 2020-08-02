import subprocess
import sys
import math


# テキストファイルを読み込み2次元配列へ変換する
def load_sudoku(filepath):
    arr = []
    opened_squares = {}  # 開いているマスを記録する辞書

    with open(filepath, "r") as f:
        for line in f:
            str_row = (line[:-1].split(','))
            row = []
            for s in str_row:
                if s == "-":
                    row.append(int(0))
                else:
                    row.append(int(s))
            arr.append(row)
    
    for i in range(9):
        for j in range(9):
            if arr[i][j] != 0:
                s_index = "s{0}{1}".format(str(i+1), str(j+1))
                opened_squares[s_index] = arr[i][j]

    return arr, opened_squares


# 制約を生成する
def get_constrain(arr, opened_squares):
    cons1 = ""
    squares = []

    # 1. 既に開いているマスに関する制約
    for i in range(1,10):
        for j in range(1,10):
            s_index = "s{0}{1}".format(str(i), str(j))
            squares.append(s_index)
            if s_index in opened_squares:  # 既にマスが開いている場合
                num = opened_squares[s_index]
                cons1 += "{0}.{1} ".format(s_index, num)
            else:  # まだマスが開いていない場合
                for k in range(1,10):
                    cons1 += "{0}.{1} ".format(s_index, str(k))
            cons1 = cons1[:-1] + "\n"

    # 2. 同じ行に関する制約
    cons2 = ""
    for s_index in squares:
        for num in range(1,10):
            i_index = int(s_index[1])
            j_index = int(s_index[2])
            for j in range(1,10):
                if j_index != j:
                    ns_index = "s{0}{1}".format(i_index, j)
                    cons2 += "~{0}.{1} ~{2}.{3}\n".format(s_index, num, ns_index, num)
    
    # 3. 同じ列に関する制約
    cons3 = ""
    for s_index in squares:
        for num in range(1,10):
            i_index = int(s_index[1])
            j_index = int(s_index[2])
            for i in range(1,10):
                if i_index != i:
                    ns_index = "s{0}{1}".format(i, j_index)
                    cons3 += "~{0}.{1} ~{2}.{3}\n".format(s_index, num, ns_index, num)

    # 4. 3x3のブロックに関する制約
    cons4 = ""
    for s_index in squares:
        for num in range(1,10):
            i_index = int(s_index[1])
            j_index = int(s_index[2])
            sq3_i = 3 * (math.ceil(i_index / 3.0) - 1) + 1
            sq3_j = 3 * (math.ceil(j_index / 3.0) - 1) + 1
            for i in range(0,3):
                for j in range(0,3):
                    ns_index = "s{0}{1}".format(sq3_i+i, sq3_j+j)
                    if s_index != ns_index:
                        cons4 += "~{0}.{1} ~{2}.{3}\n".format(s_index, num, ns_index, num)

    constrain = cons1 + cons2 + cons3 + cons4
    return constrain


def print_array(arr):
    arr_string = ""
    for column in arr:
        column = ["-" if n == 0 else str(n) for n in column[:]]
        arr_string += ",".join(column) + "\n"
    print(arr_string)


if __name__ == "__main__":
    sudoku_txt = sys.argv[1]
    arr, opened_squares = load_sudoku(sudoku_txt)
    constrain = get_constrain(arr, opened_squares)
    
    print("**** puzzle ****")
    print_array(arr)

    # .satファイルの作成
    constrain_sat = sudoku_txt.replace("txt", "sat")
    with open(constrain_sat, "w") as f:
        f.write(constrain)
    print(".sat file: {0}".format(constrain_sat))
    
    # sat13を実行
    cmd = "sat13 < {0} ".format(constrain_sat)
    print("$ " + cmd)
    cp = subprocess.run(cmd, shell=True, encoding="utf-8", stdout=subprocess.PIPE)

    arr_answer = [[0 for i in range(9)] for j in range(9)]
    for s in cp.stdout.split():
        if s[0] != "~":
            i_index = int(s[1]) - 1
            j_index = int(s[2]) - 1
            num = int(s[4])
            arr_answer[i_index][j_index] = num
    
    print("\n**** answer ****")
    print_array(arr_answer)