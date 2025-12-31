import pathlib as pl
from functools import lru_cache
from collections import defaultdict


def read_server_rack_file(file_path: pl.Path) -> dict[str, set[str]]:
    """
    Reads a file containing the server rack layout.
    Each line represents one row of the rack, with server IDs connected to it via a colon.
    Example file content:

    aaa: you hhh
    you: bbb ccc
    bbb: ddd eee
    ccc: ddd eee fff
    ddd: ggg
    eee: out
    fff: out
    ggg: out
    hhh: ccc fff iii
    iii: out
    """
    content = file_path.read_text().strip().splitlines()
    rack = defaultdict(set)

    for line in content:
        server_id, connections = line.split(": ")
        connected_servers = connections.split(" ") if connections else []
        rack[server_id].update(connected_servers)

    return rack


def invert_server_rack(rack: dict[str, set[str]]) -> dict[str, set[str]]:
    """
    Inverts the server rack mapping to get a mapping from each server to the servers that connect to it.
    """
    all_server_ids = set([server for server_connections in rack.values() for server in server_connections])
    inverted_rack = {server_id: set() for server_id in all_server_ids}

    for server_id, connections in rack.items():
        for connected_server in connections:
            inverted_rack[connected_server].add(server_id)
    return inverted_rack


def find_paths_to_out(rack: dict[str, set[str]], start_server: str, end_server: str, path=None) -> list[list[str]]:
    """
    Finds all paths from the start_server to the 'out' server.
    """
    if path is None:
        path = []
    path = path + [start_server]

    if start_server == end_server:
        return [path]

    if start_server not in rack:
        return []

    paths = []
    for _, connected_server in enumerate(rack[start_server]):
        if connected_server not in path:  # Avoid cycles
            new_paths = find_paths_to_out(rack, connected_server, end_server, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths


def find_paths_inverted(inverted_rack: dict[str, list[str]], start_server: str, end_server: str, path=None) -> list[list[str]]:
    """
    Finds all paths from the end server to the start server using the inverted rack mapping.
    """
    if path is None:
        path = []
    path = path + [end_server]

    if end_server == start_server:
        return [path]

    if end_server not in inverted_rack:
        return []

    paths = []
    for _, connected_server in enumerate(inverted_rack[end_server]):
        if connected_server not in path:  # Avoid cycles
            new_paths = find_paths_inverted(inverted_rack, start_server, connected_server, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"
    start_server = "svr"
    end_server = "out"

    server_rack = read_server_rack_file(input_file)
    print(server_rack)

    inverted_server_rack = invert_server_rack(server_rack)
    print(inverted_server_rack)

    @lru_cache(maxsize=None)
    def dfs(node: str, v_dac=False, v_fft=False) -> int:
        # End condition: reached 'out' with both 'dac' and 'fft' visited
        if node == "out" and v_dac and v_fft:
            return 1

        # Recursion through children
        total = 0
        for child in server_rack.get(node, []):
            total += dfs(child, v_dac or node == "dac", v_fft or node == "fft")
        return total

    total_paths = dfs(start_server)
    print(f"Total number of valid paths from '{start_server}' to '{end_server}': {total_paths}")
    # all_paths = find_paths_to_out(server_rack, start_server, end_server)
    # all_paths = find_paths_inverted(inverted_server_rack, start_server, end_server)
    # print(f"All paths from '{start_server}' to '{end_server}':")
    # for path in all_paths:
    #     print(" -> ".join(path))
    # print(f"Total number of paths from '{start_server}' to '{end_server}': {len(all_paths)}")


if __name__ == "__main__":
    main()
