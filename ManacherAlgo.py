def manacher(s):
    s = '#' + '#'.join(s) + '#'
    n = len(s)
    P = [0] * n
    C, R = 0, 0

    for i in range(n):
        if i < R:
            P[i] = min(R - i, P[2 * C - i])
        else:
            P[i] = 0

        a, b = i + P[i] + 1, i - P[i] - 1
        while a < n and b >= 0 and s[a] == s[b]:
            P[i] += 1
            a += 1
            b -= 1

        if i + P[i] > R:
            C, R = i, i + P[i]

    max_len, center = max((n, i) for i, n in enumerate(P))
    start = (center - max_len) // 2
    end = start + max_len
    return s[start:end].replace('#', '')

s = "babad"
print(manacher(s))
