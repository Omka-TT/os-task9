import sys
from memsim import load, run

strategy = sys.argv[1] if len(sys.argv) > 1 else "first"
merge = len(sys.argv) > 2 and sys.argv[2] == "merge"
mm = run(load("ops1.txt"), strategy, coalesce=merge, verbose=True)
total, largest, holes = mm.stats()
print(f"свободно={total} макс. дыра={largest} дыр={holes} отказов={mm.refused}")
