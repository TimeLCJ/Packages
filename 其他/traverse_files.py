import os, re

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if re.match(r'.*\d.*', f):
                fullname = os.path.join(root, f)
                yield fullname

def main():
    base = r'D:\Downloads\CH-HCNetSDKV6.1.6.4_build20201231_linux64\QtDemo\src'
    for i in findAllFile(base):
        print(i)

if __name__ == '__main__':
    main()