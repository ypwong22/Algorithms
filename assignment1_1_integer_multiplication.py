"""
yp 2018/08/07

Implement the divide and conquer algorithm to multiply two large integers.
"""

def karatsuba(x, y):
    X = str(x)
    Y = str(y)

    # Pad to the same number of digits.
    if (len(X) > len(Y)):
        Y = Y.zfill(len(X))
    elif (len(X) < len(Y)):
        X = X.zfill(len(Y))

    if (len(X)==1):
        return x * y
    else:
        n = len(X) // 2
        m = len(X) - n

        a = int(X[:n])
        b = int(X[n:len(X)])
        c = int(Y[:n])
        d = int(Y[n:len(Y)])

        ac = karatsuba(a,c)
        bd = karatsuba(b,d)
        abcd = karatsuba(a+b, c+d)
        return ac * (100 ** m) + bd + (abcd - ac - bd) * (10 ** m)

x = 3141592653589793238462643383279502884197169399375105820974944592
y = 2718281828459045235360287471352662497757247093699959574966967627

print(x*y)
print(karatsuba(x,y))
