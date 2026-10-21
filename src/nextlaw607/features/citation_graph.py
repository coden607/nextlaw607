from __future__ import annotations

def expand(seeds: list[str], edges: dict[str, list[str]], *, depth: int = 1) -> tuple[str, ...]:
    seen = set(seeds)
    frontier = list(seeds)
    for _ in range(max(depth, 0)):
        next_frontier: list[str] = []
        for node in frontier:
            for neighbor in edges.get(node, []):
                if neighbor not in seen:
                    seen.add(neighbor); next_frontier.append(neighbor)
        frontier = next_frontier
    return tuple(sorted(seen))
