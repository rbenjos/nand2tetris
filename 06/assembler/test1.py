def add(a,b):
    c = a+b
    return c


def subtract(a,b):
    c = a-b
    return c


def power (a,b):
    return a**b

def mul_list (list1,a):
    list_a = []
    for i in range(0,len(list1)):
        list_a.append(list1[i] * a)
    return list_a

def square_list(list1):
    list_a = []
    for i in range(0,len(list1)):
        list_a.append(list1[i] ** 2)
    return list_a

list2 = [2,3,54,3,3,4,3,3,2,2]
list3 = mul_list(list2,3)
list4 = square_list(list3)

print(list2)
print(list3)
print(list4)