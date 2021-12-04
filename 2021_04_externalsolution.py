FILE="input/2021_04_input"
FILE='/tmp/input'
file = open(FILE, "r");
numbers = [int(i) for i in (file.readlines()[0]).split(",")]
file.close()
file = open(FILE, "r");

boards = []

curr = []

x = 1

for i in file.readlines()[2:]:
    if x == 6:
        boards.append(curr)
        curr = []
        x = 1
        continue
    curr.append([int(j) for j in i[:-1].split()]) 
    x += 1
def check(arr):
    for i in arr:
        if sum(i) == -5:
            return True
    for i in range(5):
        Sum = 0
        for j in range(5):
            Sum += arr[j][i]
        if Sum == -5:
            return True
    return False   

def FindSum(arr):
    SUM = 0
    for i in arr:
        for j in i:
            if j != -1:
                SUM += j
    return SUM

seen = []

winningBoards = []

for i in numbers:
    for j in range(len(boards)):
        for k in range(len(boards[j])):
            for l in range(len(boards[j][k])):
                if boards[j][k][l] == i:
                    boards[j][k][l] = -1
        if check(boards[j]) and j not in seen:
            print("Board {} wins with score {} * {}".format(j, i, FindSum(boards[j])));
            print(boards[j])
            winningBoards.append(i * FindSum(boards[j]))
            seen.append(j)
    
#ANSWERS
print(winningBoards[0])
print(winningBoards[-1])
