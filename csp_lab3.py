"""Лаборатори 3: ерөнхий CSP, backtracking ба heuristic."""


class CSP:
    # Хувьсагч, домэйн, хөрш, хязгаарлалт болон тоолуурыг хадгална.
    def __init__(self, variables, domains, neighbors, constraint):
        self.variables = list(variables)
        self.domains = {v: list(domains[v]) for v in self.variables}
        self.neighbors = {v: list(neighbors[v]) for v in self.variables}
        self.constraint = constraint
        self.nodes = 0
        self.attempts = 0

    # Зөвхөн оноогдсон хөршүүдтэй зөрчилдөх эсэхийг шалгана.
    def is_consistent(self, var, value, assignment):
        return all(
            self.constraint(var, value, other, assignment[other])
            for other in self.neighbors[var] if other in assignment
        )

    # Анхны дарааллаар оноогдоогүй хувьсагчдыг буцаана.
    def unassigned(self, assignment):
        return [v for v in self.variables if v not in assignment]


class SearchLimitExceeded(RuntimeError):
    """Зөвшөөрөгдсөн зангилааны хязгаарт хүрсэн хайлт."""


# Хоёр чиглэлтэй хөршийн жагсаалтыг ирмэгүүдээс үүсгэнэ.
def make_neighbors(variables, edges):
    neighbors = {v: [] for v in variables}
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    return neighbors


# Австралийн мужуудыг өгсөн өнгөөр будах CSP үүсгэнэ.
def make_map_csp(colors=("red", "green", "blue")):
    variables = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
    edges = [("WA", "NT"), ("WA", "SA"), ("NT", "SA"),
             ("NT", "Q"), ("SA", "Q"), ("SA", "NSW"),
             ("SA", "V"), ("Q", "NSW"), ("NSW", "V")]
    # Хөрш мужууд ялгаатай өнгөтэй байх ёстой.
    def constraint(a, color_a, b, color_b):
        return color_a != color_b
    return CSP(variables, {v: list(colors) for v in variables},
               make_neighbors(variables, edges), constraint)


# Мөрийг хувьсагч, баганыг домэйн болгон N-Queens CSP үүсгэнэ.
def make_queens_csp(n):
    if n < 1:
        raise ValueError("CSP самбарын n нь 1-ээс багагүй байна")
    variables = list(range(n))
    # Хатад нэг багана болон нэг диагональд байрлахгүй.
    def constraint(row_a, col_a, row_b, col_b):
        return col_a != col_b and abs(col_a - col_b) != abs(row_a - row_b)
    return CSP(variables, {v: list(range(n)) for v in variables},
               {v: [w for w in variables if w != v] for v in variables},
               constraint)


# Одоогийн оноолттой зөрчилгүй домэйны утгуудыг олно.
def legal_values(csp, var, assignment):
    return [value for value in csp.domains[var]
            if csp.is_consistent(var, value, assignment)]


# MRV ашиглан сонгоод тэнцвэл оноогдоогүй хөршийн degree-г хэрэглэнэ.
def select_unassigned_variable(csp, assignment, use_mrv=True, use_degree=False):
    remaining = csp.unassigned(assignment)
    # Эрэмбэлэх түлхүүр; min нь тэнцсэн үед анхны дарааллыг хадгална.
    def key(var):
        mrv = len(legal_values(csp, var, assignment)) if use_mrv else 0
        degree = (sum(w not in assignment for w in csp.neighbors[var])
                  if use_degree else 0)
        return mrv, -degree
    return min(remaining, key=key)


# Оноогдоогүй хөршүүдээс хамгийн цөөн боломжит утга хасах утгыг эхэлж өгнө.
def order_domain_values(csp, var, assignment, use_lcv=True):
    if not use_lcv:
        return list(csp.domains[var])
    values = legal_values(csp, var, assignment)
    neighbor_values = {
        w: legal_values(csp, w, assignment)
        for w in csp.neighbors[var] if w not in assignment
    }
    # Одоогоор боломжтой утгуудаас шинээр хасагдах тоог тоолно.
    def eliminated(value):
        return sum(not csp.constraint(var, value, w, other_value)
                   for w, choices in neighbor_values.items()
                   for other_value in choices)
    return sorted(values, key=eliminated)


# Consistent оноолтын тоог өсгөхөөс өмнө хайлтын хязгаарыг шалгана.
def record_node(csp, node_limit):
    if node_limit is not None and csp.nodes >= node_limit:
        raise SearchLimitExceeded(f"Зангилааны хязгаар: {node_limit}")
    csp.nodes += 1


# Рекурсив backtracking нь эхний шийд эсвэл None буцаана.
def backtrack(csp, assignment, use_mrv=False, use_degree=False,
              use_lcv=False, node_limit=None):
    if len(assignment) == len(csp.variables):
        return assignment.copy()
    var = select_unassigned_variable(csp, assignment, use_mrv, use_degree)
    for value in order_domain_values(csp, var, assignment, use_lcv):
        csp.attempts += 1
        if csp.is_consistent(var, value, assignment):
            record_node(csp, node_limit)
            assignment[var] = value
            try:
                result = backtrack(csp, assignment, use_mrv, use_degree,
                                   use_lcv, node_limit)
            finally:
                del assignment[var]
            if result is not None:
                return result
    return None


# Хайлт бүрийн өмнө тоолуурыг тэглэж хоосон оноолтоос эхлүүлнэ.
def backtracking_search(csp, use_mrv=False, use_degree=False,
                        use_lcv=False, node_limit=None):
    csp.nodes = csp.attempts = 0
    return backtrack(csp, {}, use_mrv, use_degree, use_lcv, node_limit)


# Шийдийг хайлтаас үл хамааран бүрэн байдал, домэйн, хязгаарлалтаар шалгана.
def check_solution(csp, assignment):
    if assignment is None or set(assignment) != set(csp.variables):
        return False
    if any(assignment[v] not in csp.domains[v] for v in csp.variables):
        return False
    return all(csp.constraint(v, assignment[v], w, assignment[w])
               for v in csp.variables for w in csp.neighbors[v])


# Бүх шийдийг тоолох эсвэл тусдаа dictionary болгон цуглуулах DFS хийнэ.
def enumerate_solutions(csp, use_mrv=False, use_degree=False,
                        use_lcv=False, collect=True, node_limit=None):
    csp.nodes = csp.attempts = 0
    assignment, solutions = {}, []
    # Шийд олсон ч бусад салааг үргэлжлүүлнэ.
    def visit():
        if len(assignment) == len(csp.variables):
            if collect:
                solutions.append(assignment.copy())
            return 1
        total = 0
        var = select_unassigned_variable(csp, assignment, use_mrv, use_degree)
        for value in order_domain_values(csp, var, assignment, use_lcv):
            csp.attempts += 1
            if csp.is_consistent(var, value, assignment):
                record_node(csp, node_limit)
                assignment[var] = value
                try:
                    total += visit()
                finally:
                    del assignment[var]
        return total
    count = visit()
    return solutions if collect else count


# Шийдүүдийг хадгалахгүйгээр зөвхөн тоог буцаана.
def count_solutions(csp, use_mrv=False, use_degree=False, use_lcv=False):
    return enumerate_solutions(csp, use_mrv, use_degree, use_lcv, collect=False)


# Хатан байрласан нүдийг Q, бусдыг цэгээр хэвлэнэ.
def print_board(assignment, n):
    for row in range(n):
        print(" ".join("Q" if assignment[row] == col else "." for col in range(n)))


# Сургалтын цагийн хуваарьт багш, бүлэг, дарааллын binary хязгаарлалт үүсгэнэ.
def make_schedule_csp(extra_group1=0):
    variables = ["AI", "DM", "NET", "OS", "MATH", "ENG"]
    teachers = dict(zip(variables, ["A", "A", "B", "B", "C", "C"]))
    groups = dict(zip(variables, [1, 2, 1, 2, 2, 1]))
    for i in range(extra_group1):
        name = f"EXTRA{i + 1}"
        variables.append(name)
        teachers[name], groups[name] = f"D{i + 1}", 1
    domains = {v: [1, 2] if teachers[v] == "B" else [1, 2, 3, 4]
               for v in variables}
    edges = [(a, b) for i, a in enumerate(variables) for b in variables[i + 1:]
             if teachers[a] == teachers[b] or groups[a] == groups[b]
             or {a, b} == {"AI", "DM"}]
    # Зааврын DB-г хүснэгтэд байгаа DM гэж үзэж AI < DM шаардлагыг шалгана.
    def constraint(a, slot_a, b, slot_b):
        if (teachers[a] == teachers[b] or groups[a] == groups[b]) and slot_a == slot_b:
            return False
        if a == "AI" and b == "DM":
            return slot_a < slot_b
        if a == "DM" and b == "AI":
            return slot_b < slot_a
        return True
    csp = CSP(variables, domains, make_neighbors(variables, edges), constraint)
    csp.teachers, csp.groups = teachers, groups
    return csp


CONFIGS = [
    ("A", "Heuristic-гүй", False, False, False),
    ("B", "MRV", True, False, False),
    ("C", "MRV + Degree", True, True, False),
    ("D", "MRV + Degree + LCV", True, True, True),
]


# Ижил нөхцөлтэй эхний шийдийн хайлтыг хэмжиж бодит үр дүнг буцаана.
def benchmark(node_limit=1_000_000, repeats=3):
    from time import perf_counter
    from statistics import median
    rows = []
    for code, label, mrv, degree, lcv in CONFIGS:
        for name, n in [("Map", None), ("8-Queens", 8),
                        ("12-Queens", 12), ("16-Queens", 16)]:
            durations = []
            for _ in range(repeats):
                csp = make_map_csp() if n is None else make_queens_csp(n)
                start = perf_counter()
                try:
                    result = backtracking_search(csp, mrv, degree, lcv, node_limit)
                    status = "solved" if result is not None else "unsatisfiable"
                except SearchLimitExceeded:
                    result, status = None, "limit"
                durations.append((perf_counter() - start) * 1000)
                if status == "solved" and not check_solution(csp, result):
                    raise AssertionError("Хүчингүй шийд")
            rows.append(dict(config=code, label=label, problem=name,
                             nodes=csp.nodes, attempts=csp.attempts,
                             milliseconds=median(durations), status=status,
                             solution=result, repeats=repeats))
    return rows
