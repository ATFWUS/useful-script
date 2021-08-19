> 在CTF各大类别的题型中，都会有爆破的需求，那么如何优雅的爆破一个32位整数呢？这里分享一个多线程爆破32位整数的一个方法。

---
[toc]

---

# 1.脚本与使用须知
- 正常情况下，修改check函数就可以使用。
- thread_num为线程数，默认为cpu核心数，建议不修改，线程远超cpu核心数，多线程反而会变慢。一定要为2的整数次幂。
- print_threshold 为输出枚举中间状态的阈值，凡是遍历到能整除该数的 都将打印出信息，相当于给爆破过程一些反馈。
- bit_num 数字的比特位，默认为32位整数。
- check函数是校验num的正确性的，此处一定要修改。
- 脚本运行结束后，结果会在enumeration_result.txt中，也可以在控制台搜索reult。
- 这种类型的脚本一般不做面向对象封装。

```python
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

```

# 2.脚本实现细节
## 2.1 脚本整体思路
每个线程其实主要是在爆一个高位，例如采用8个线程，那么实际上第1个线程，爆破的是`0*2^28---1*2^28`，第二个线程，爆破的是`1*2^28---2*2^28`，依此类推。

## 2.2 线程数选择
线程数最好等于cpu核心数，低了或者高了都会影响效率。
## 2.3 爆破过程反馈
如果爆破的时候控制台一点反馈都没有，就不知道现在的速度如何，进度如何。如果反馈太多，那么眼花缭乱的找不到有用信息。所以专门设置了一个反馈阈值，每到一个指定数字节点会输出一段信息。
## 2.4 结果反馈
只要有一个进程找到了需要的数，立刻退出所有的线程。将结果打印，并存储到文件（方便查看结果）

---

>**<font size=5>ATFWUS 2021-08-19**
