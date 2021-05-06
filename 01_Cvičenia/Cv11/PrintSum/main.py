def _range(start, end):
    return range(start, end + 1)


# b_n = sum<k=0..n-1> {b_k * b_n-1-k}
def bst(n):
    if n == 0:
        return 1

    bn = 0
    for k in _range(0, n - 1):          # 0...n-1
        bn += bst(k) * bst(n - 1 - k)   # b_k * b_n-1-k
    return bn


# b_n = sum<k=0..min(3,n-1)> {b_k * b_n-1-k}
def vojsic_bst(n):
    if n == 0:
        return 1

    bn = 0
    for k in _range(0, min(3, n - 1)):               # 0..min(3, n-1)
        bn += vojsic_bst(k) * vojsic_bst(n - 1 - k)  # b_k * b_n-1-k

    return bn


if __name__ == '__main__':
    for x in range(1, 11):
        print("n =", x, ": vsetky=", bst(x), "vojsicove=", vojsic_bst(x))
