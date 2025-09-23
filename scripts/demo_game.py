from src.fibonacci_heap import FibonacciHeap

def main():
    H = FibonacciHeap()
    next_id = 1            # assign a simple integer ID to each inserted node
    nodes = {}             # id -> node handle (needed for decrease/delete)
    score = 0

    print("=== Fibonacci Heap Demo ===")
    print("Commands:")
    print("  insert X          -> insert number X (returns an id)")
    print("  min               -> show the current minimum")
    print("  merge             -> merge a small demo heap [42, 17]")
    print("  extract           -> extract and print the current minimum")
    print("  decrease ID NEW   -> decrease key of node with id=ID to NEW")
    print("  delete ID         -> delete node with id=ID")
    print("  list              -> list known node IDs and their current keys")
    print("  score             -> show your score")
    print("  quit              -> exit")
    print("=================================")

    def list_nodes():
        # best-effort: show id->key for handles that still exist (not deleted/extracted)
        if not nodes:
            print("No tracked nodes (insert something).")
            return
        lines = []
        for nid, node in nodes.items():
            # node may have been deleted/extracted; skip handles no longer in heap
            if node.left is node and node.parent is None and H.min is None:
                # heap empty; nothing to show
                continue
            try:
                # if node is still linked, it will have a key
                lines.append(f"{nid}: {node.key}")
            except Exception:
                pass
        if lines:
            print("Tracked nodes:")
            for ln in lines:
                print(" ", ln)
        else:
            print("No tracked nodes currently in heap.")

    while True:
        try:
            parts = input("> ").strip().split()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting. Goodbye!")
            break

        if not parts:
            continue

        cmd = parts[0].lower()

        if cmd == "insert" and len(parts) == 2:
            try:
                x = int(parts[1])
            except ValueError:
                print("Please enter a valid number.")
                continue
            node = H.insert(x)
            nid = next_id
            next_id += 1
            nodes[nid] = node
            print(f"Inserted {x} with id={nid}. Heap size = {H.n}")
            score += 1

        elif cmd == "min":
            try:
                m = H.minimum()
                print(f"Minimum = {m}")
                score += 1
            except IndexError:
                print("Heap is empty.")

        elif cmd == "merge":
            other = FibonacciHeap()
            for y in [42, 17]:
                other.insert(y)
            H.merge(other)
            print("Merged a demo heap [42, 17].")
            try:
                print(f"New minimum = {H.minimum()}")
            except IndexError:
                print("Heap is empty after merge (unexpected).")
            score += 2

        elif cmd == "extract":
            try:
                val = H.extract_min()
                print(f"extract_min -> {val}. Heap size = {H.n}")
                score += 2
                # best effort: remove any one tracked id that matches this key
                # (keys can repeat; this is just for the demo)
                to_delete = None
                for nid, node in nodes.items():
                    try:
                        if node.key == val:
                            to_delete = nid
                            break
                    except Exception:
                        pass
                if to_delete is not None:
                    del nodes[to_delete]
            except IndexError:
                print("Heap is empty.")

        elif cmd == "decrease" and len(parts) == 3:
            try:
                nid = int(parts[1])
                new_key = int(parts[2])
            except ValueError:
                print("Usage: decrease ID NEW   (ID and NEW must be integers)")
                continue
            if nid not in nodes:
                print("Unknown id. Use 'list' to see tracked ids.")
                continue
            node = nodes[nid]
            try:
                H.decrease_key(node, new_key)
                print(f"decrease_key: id={nid} now has key={node.key}. New min={H.minimum()}")
                score += 2
            except ValueError as e:
                print(f"Error: {e}")
            except Exception:
                print("That node may no longer be in the heap.")

        elif cmd == "delete" and len(parts) == 2:
            try:
                nid = int(parts[1])
            except ValueError:
                print("Usage: delete ID   (ID must be an integer)")
                continue
            if nid not in nodes:
                print("Unknown id. Use 'list' to see tracked ids.")
                continue
            node = nodes[nid]
            try:
                H.delete(node)
                del nodes[nid]
                print(f"Deleted node id={nid}. Heap size = {H.n}")
                score += 2
            except Exception:
                print("That node may no longer be in the heap.")

        elif cmd == "list":
            list_nodes()

        elif cmd == "score":
            print(f"Score = {score}")

        elif cmd == "quit":
            print("Exiting. Goodbye!")
            break

        else:
            print("Unknown command. Try: insert X | min | merge | extract | decrease ID NEW | delete ID | list | score | quit")

if __name__ == "__main__":
    main()
