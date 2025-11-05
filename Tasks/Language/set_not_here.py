def find_common(a, b):
    union = a | b
    for i in union:
        if -10 <= i <= 10:
            print(i)

a = set()
b = set()
n = 1

print("Введите элементы множетсва A: ")
n = int(input())
while n != 0:
    a.add(n)
    n = int(input())

print("Введите элементы множетсва B: ")
n = int(input())
while n != 0:
    b.add(n)
    n = int(input())

print("-------------")

print(a)
print(b)
find_common(a, b)
