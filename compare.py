from memsim import MemoryManager, load
from buddy import Buddy

ops = load("ops2.txt")


def simulate(make, alloc, free, stats):
    m, ext, internal = make(), [], []
    for cmd, pid, *rest in ops:
        alloc(m, pid, rest[0]) if cmd == "alloc" else free(m, pid)
        tot, mx, extra = stats(m)
        ext.append(1 - mx / tot if tot else 0)
        internal.append(extra)
    return m.refused, sum(ext) / len(ext), sum(internal) / len(internal)


rows = []
for merge in (False, True):
    for s in ["first", "best", "worst"]:
        r, e, i = simulate(lambda: MemoryManager(s, coalesce=merge),
                           MemoryManager.alloc, MemoryManager.free,
                           lambda m: (*m.stats()[:2], 0))
        rows.append((f"{s}{' +merge' if merge else ''}", r, e, i))
r, e, i = simulate(Buddy, Buddy.alloc, Buddy.release, Buddy.stats)
rows.append(("buddy", r, e, i))

print(f"{'подход':<16}{'отказов':>8}{'внешняя фр.':>13}{'внутренняя':>12}")
for n, r, e, i in rows:
    print(f"{n:<16}{r:>8}{e:>13.2f}{i:>12.0f}")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

names = [r[0] for r in rows]
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
for a, k, t in zip(ax, (1, 2, 3), ("Отказы", "Внешняя фрагментация (средняя)", "Внутренняя фрагментация (средняя, ед.)")):
    a.bar(names, [r[k] for r in rows])
    a.set_title(t)
    a.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig("compare.png", dpi=120)
print("график: compare.png")
