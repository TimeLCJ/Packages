def rreplace(string, old, new, *max):
    count = len(string)
    if max and str(max[0]).isdigit():
        count = max[0]
    return new.join(string.rsplit(old, count))

res = rreplace("lemon tree", "e", "3")
print(res)