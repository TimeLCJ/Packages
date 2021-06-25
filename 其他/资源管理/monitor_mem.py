import psutil
import GPUtil
import time

def cpu_memory():
    mem = psutil.virtual_memory()
    total = float(mem.total)/1024/1024/1024
    free = float(mem.free)/1024/1024/1024

    return total, free

def gpu_memory():
    gm = []
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        gm.append([gpu.memoryTotal/1024, gpu.memoryFree/1024])
    return gm

if __name__ == '__main__':
    while True:
        ct, cf = cpu_memory()
        print(f'free memory: {round(cf, 2)}GB, total memory: {round(ct, 2)}GB')
        gpus = gpu_memory()
        for gpu in gpus:
            print(f'free gpu memory: {round(gpu[1], 2)}GB, total gpu memory: {round(gpu[0], 2)}GB')
        time.sleep(5)
