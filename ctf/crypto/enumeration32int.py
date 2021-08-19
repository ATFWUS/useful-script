from threading import Thread
from multiprocessing import cpu_count
import os
import math


# 线程数 一定要为2的整数次幂
thread_num = cpu_count()

# 输出枚举中间状态的阈值 凡是遍历到能整除该数的 都将打印出信息
print_threshold = 2 ** 19

# 数字的比特位
bit_num = 32

# 此处需要重写 校验num是否为所需要的 该处校验的复杂度不能太高
def checkNum(num):

    return True

def enumeration(num, pid):
    # 输出线程启动信息
    print("[Process%d]: start from %d" % (pid, num))
    # 单个线程的枚举
    while num < 2**(bit_num - math.log2(thread_num) - 1)*(pid + 1):
        # 校验num
        if checkNum(num):
            print("[Process%d]: The result is num = %d" % (pid, num))
            f = open('enumeration_result.txt', 'w')
            # 将答案写入文件
            f.write("[Process%d]: The result is num = %d" % (pid, num))
            f.close()
            # 退出所有线程
            os._exit(0)
        num+=1
        # 输出中间时段的信息
        if num % print_threshold == 0:
            print('[Process%d]: now is %d' % (pid, num))
    # 输出线程退出信息
    print('[Process%d]: exited!' % pid)

for i in range(0, thread_num):
    t = Thread(target=enumeration, args=(i * (2 ** (bit_num - math.log2(thread_num) - 1)), i))
    t.start()
