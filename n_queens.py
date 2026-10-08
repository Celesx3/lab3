# Мөр бүрд хатан байрлуулж, зөрчилгүй бүх шийдийг DFS-ээр олно.
def dfs_n_queens(n):
    """Return all N-Queens solutions in ascending column DFS order."""
    if n < 1:
        return []

    solutions = []
    placement = []
    columns = set()
    diagonals_down = set()
    diagonals_up = set()

    def dfs(row):
        if row == n:
            solutions.append(placement.copy())
            return

        for col in range(n):
            down = row - col
            up = row + col
            if col in columns or down in diagonals_down or up in diagonals_up:
                continue

            placement.append(col)
            columns.add(col)
            diagonals_down.add(down)
            diagonals_up.add(up)
            dfs(row + 1)
            placement.pop()
            columns.remove(col)
            diagonals_down.remove(down)
            diagonals_up.remove(up)

    dfs(0)
    return solutions
