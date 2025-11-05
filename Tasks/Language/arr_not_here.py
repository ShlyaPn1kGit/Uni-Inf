def pack_array(array, amount, name):
    c = 0
    print(f"Введите {amount} элементов массива {name}:")
    for i in range(amount):
        array.append(int(input()))
        if array[-1] < 0:
            c+= 1
    wort[name] = c

n = int(input("Введите размер массива: "))
wort = {}
a = []
b = []

pack_array(a, n, "A")
pack_array(b, n, "B")

if wort.get("A") > wort.get("B"):
    print(a, b)
else:
    print(b, a)