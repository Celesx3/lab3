"""Лаб 3-ын үр дүн, heuristic болон N-Queens шаардлагын шалгалтууд."""
import inspect
import unittest

from csp_lab3 import *
from n_queens import dfs_n_queens


class Lab3Tests(unittest.TestCase):
    def test_csp_and_map(self):
        csp = make_map_csp()
        self.assertEqual([len(csp.neighbors[v]) for v in ["SA", "T", "WA"]], [5, 0, 2])
        self.assertFalse(csp.is_consistent("NT", "red", {"WA": "red"}))
        self.assertTrue(csp.is_consistent("NT", "blue", {"WA": "red"}))
        self.assertTrue(csp.is_consistent("T", "red", {"WA": "red"}))
        for _, _, mrv, degree, lcv in CONFIGS:
            solution = backtracking_search(csp, mrv, degree, lcv)
            self.assertTrue(check_solution(csp, solution))
        self.assertFalse(check_solution(csp, {}))
        self.assertFalse(check_solution(csp, {v: "red" for v in csp.variables}))
        bad = solution.copy()
        bad["T"] = "purple"
        self.assertFalse(check_solution(csp, bad))

    def test_heuristics(self):
        csp = make_map_csp()
        self.assertEqual(select_unassigned_variable(csp, {"WA": "red"}), "NT")
        self.assertEqual(select_unassigned_variable(csp, {}, True, True), "SA")
        assignment = {"WA": "red", "NT": "green"}
        before = assignment.copy()
        self.assertEqual(order_domain_values(csp, "Q", assignment), ["red", "blue"])
        self.assertEqual(assignment, before)
        # SA-д боломжит утга байхгүй тул MRV эхэлж зөрчлийг илрүүлнэ.
        self.assertEqual(select_unassigned_variable(csp, {"WA": "red", "NT": "green", "Q": "blue"}), "SA")

    def test_solution_counts_and_validity(self):
        expected = [1, 0, 0, 2, 10, 4, 40, 92]
        for n, count in enumerate(expected, 1):
            csp = make_queens_csp(n)
            self.assertEqual(count_solutions(csp), count)
        for _, _, mrv, degree, lcv in CONFIGS:
            csp = make_queens_csp(8)
            solutions = enumerate_solutions(csp, mrv, degree, lcv)
            self.assertEqual(len(solutions), 92)
            self.assertEqual(len({tuple(s[r] for r in range(8)) for s in solutions}), 92)
            for s in solutions:
                self.assertTrue(check_solution(csp, s))
                cols = [s[r] for r in range(8)]
                self.assertEqual(len(set(cols)), 8)
                self.assertEqual(len({r - col for r, col in enumerate(cols)}), 8)
                self.assertEqual(len({r + col for r, col in enumerate(cols)}), 8)

    def test_counter_reset_and_limit_cleanup(self):
        csp = make_queens_csp(4)
        first = backtracking_search(csp)
        nodes = csp.nodes
        self.assertEqual(backtracking_search(csp), first)
        self.assertEqual(csp.nodes, nodes)
        assignment = {}
        csp.nodes = 0
        with self.assertRaises(SearchLimitExceeded):
            backtrack(csp, assignment, node_limit=1)
        self.assertEqual(assignment, {})
        self.assertEqual(csp.nodes, 1)
        self.assertTrue(check_solution(csp, backtracking_search(csp)))

    def test_optional_problems(self):
        self.assertIsNone(backtracking_search(make_map_csp(("red", "green")), True, True, True))
        for extras in [0, 1]:
            csp = make_schedule_csp(extras)
            result = backtracking_search(csp, True, True, True)
            self.assertTrue(check_solution(csp, result))
            self.assertLess(result["AI"], result["DM"])
            self.assertIn(result["NET"], [1, 2])
            self.assertIn(result["OS"], [1, 2])
        self.assertIsNone(backtracking_search(make_schedule_csp(2), True, True, True))

    def test_original_dfs_lab(self):
        self.assertEqual(len(inspect.signature(dfs_n_queens).parameters), 1)
        for n in [-5, -1, 0, 2, 3]:
            self.assertEqual(dfs_n_queens(n), [])
        self.assertEqual(dfs_n_queens(1), [[0]])
        self.assertEqual(dfs_n_queens(4), [[1, 3, 0, 2], [2, 0, 3, 1]])
        expected = [[0,2,4,1,3], [0,3,1,4,2], [1,3,0,2,4], [1,4,2,0,3],
                    [2,0,3,1,4], [2,4,1,3,0], [3,0,2,4,1], [3,1,4,2,0],
                    [4,1,3,0,2], [4,2,0,3,1]]
        self.assertEqual(dfs_n_queens(5), expected)
        self.assertEqual(len(dfs_n_queens(8)), 92)
        for n in range(1, 9):
            generic = enumerate_solutions(make_queens_csp(n))
            self.assertEqual(dfs_n_queens(n), [[s[r] for r in range(n)] for s in generic])


if __name__ == "__main__":
    unittest.main()
