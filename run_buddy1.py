from memsim import load
from buddy import Buddy

b = Buddy(log=True)
for n, (cmd, pid, *rest) in enumerate(load("ops1.txt"), 1):
    print(f"{n:>2} {cmd} {pid} {rest[0] if rest else ''}")
    if cmd == "alloc":
        if not b.alloc(pid, rest[0]):
            print("   ОТКАЗ")
    else:
        b.release(pid)
    print("   свободные:", {s: a for s, a in sorted(b.free.items()) if a})
print("отказов:", b.refused)
