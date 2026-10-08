# Lab 3 CSP

Backtracking хайлт ашиглан газрын зураг будах, N-Queens, цагийн хуваарийн бодлогыг шийдсэн Python лабораторийн ажил.

## Файлууд

- `csp_lab3.py` — ерөнхий CSP класс, backtracking, MRV, degree, LCV, бодлогын загварууд, хэмжилт.
- `n_queens.py` — `dfs_n_queens(n)` функц; мөр бүрийн хатны баганыг жагсаалтаар илэрхийлсэн бүх шийдийг буцаана.
- `test_lab3_csp.py` — solver, heuristic, шийдийн тоо болон нэмэлт даалгаврын шалгалтууд.
- `Lab3_CSP.ipynb` — монгол тайлбартай бүх алхам, ажиллуулж хадгалсан шалгалт ба үр дүн.

## Ажиллуулах

Python 3.10+ ашиглана. Solver болон тестэд Python-ийн стандарт сан хангалттай.

```sh
python -m unittest test_lab3_csp -v
```

N-Queens-ийн жишээ:

```sh
python -c "from n_queens import dfs_n_queens; print(dfs_n_queens(4))"
```

```text
[[1, 3, 0, 2], [2, 0, 3, 1]]
```

Ерөнхий solver-ийн жишээ:

```python
from csp_lab3 import make_queens_csp, backtracking_search, check_solution, print_board

csp = make_queens_csp(8)
solution = backtracking_search(csp, use_mrv=True)
assert check_solution(csp, solution)
print_board(solution, 8)
print("Nodes:", csp.nodes)
```

Notebook-ийг Jupyter эсвэл VS Code-ийн Python, Jupyter өргөтгөлөөр нээгээд Python kernel сонгон **Run All** хийнэ. Notebook бүх хэрэгжүүлэлтийг өөртөө агуулсан. Хэмжилтийн JSON файлууд ажиллаж буй хавтасны `tmp/lab3/` дотор үүснэ.

## Үр дүн

| Тохиргоо | Газрын зураг | 8 Queens | 12 Queens | 16 Queens |
|---|---:|---:|---:|---:|
| A Heuristic-гүй | 7 | 113 | 261 | 10052 |
| B MRV | 7 | 75 | 153 | 44 |
| C MRV + Degree | 7 | 75 | 153 | 44 |
| D MRV + Degree + LCV | 7 | 39 | 32 | 332 |

Хүснэгт нь эхний шийд хүртэлх consistent оноолтын тоо буюу `nodes`-ийг харуулна. `attempts` нь үндсэн хайлтаар туршсан утгын тоо; heuristic-ийн дотоод шалгалтыг оруулахгүй. Хугацаанд heuristic-ийн тооцоолол багтана.

8-Queens-ийн бүх шийдийг тоолсон тусдаа туршилтад дөрвөн тохиргоо тус бүр 92 давхцаагүй, зөв шийд олсон. Heuristic нь шийдийн тоог өөрчлөхгүй.

## Цагийн хуваарийн тайлбар

Гарын авлагын хүснэгтэд `DM`, дарааллын дүрэмд `DB` гэж бичсэн зөрүүг `AI < DM` гэж тайлбарласан. 1-р бүлэг эхэндээ гурван хичээлтэй тул нэг нэмэлт хичээлтэй хувилбар шийдтэй, хоёр нэмэлт хичээлтэй буюу нийт таван хичээлийг дөрвөн слотод хуваарилах хувилбар шийдгүй байна. Хоёр тохиолдлыг хоёуланг нь тестээр шалгасан.
