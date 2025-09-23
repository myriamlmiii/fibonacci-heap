# scripts/demo_game.py
from src.fibonacci_heap import FibonacciHeap
try:
    from scripts.visualization import LiveHeapVisualizer
except Exception:
    LiveHeapVisualizer = None  # still works without viz deps

def main():
    H = FibonacciHeap()
    next_id = 1
    nodes = {}
    score = 0

    viz_enabled = False
    viz = None

    print("=== Fibonacci Heap Demo (Live Viz Ready) ===")
    print("Commands:")
    print("  insert X            -> insert number X (returns an id)")
    print("  min                 -> show the current minimum")
    print("  merge               -> merge a small demo heap [42, 17]")
    print("  extract             -> extract and print the current minimum")
    print("  decrease ID NEW     -> decrease key of node with id=ID to NEW")
    print("  delete ID           -> delete node with id=ID")
    print("  list                -> list known node IDs and their current keys")
    print("  viz on/off          -> toggle live visualization (requires matplotlib+networkx)")
    print("  visualize           -> draw one snapshot now")
    print("  score               -> show your score")
    print("  quit                -> exit")
    print("=================================")

    def maybe_viz(subtitle=""):
        nonlocal viz_enabled, viz
        if not viz_enabled:
            return
        if LiveHeapVisualizer is None:
            print("Visualization libraries not installed. Run: pip install networkx matplotlib")
            return
        if viz is None:
            viz = LiveHeapVisualizer()
        viz.update(H, subtitle=subtitle)

    def list_nodes():
        if not nodes:
            print("No tracked nodes (insert something).")
            return
        print("Tracked nodes (id: key):")
        # Best-effort list (deleted/extracted nodes will disappear gradually)
        for nid, node in list(nodes.items()):
            try:
                _ = node.key  # may raise if node is gone (unlikely)
                print(f"  {nid}: {node.key}")
            except Exception:
                nodes.pop(nid, None)

    while True:
        try:
            parts = input("> ").strip().split()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting. Goodbye!")
            if viz is not None:
                viz.close()
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
            maybe_viz("after insert")

        elif cmd == "min":
            try:
                m = H.minimum()
                print(f"Minimum = {m}")
                score += 1
                maybe_viz("after min")
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
            maybe_viz("after merge")

        elif cmd == "extract":
            try:
                val = H.extract_min()
                print(f"extract_min -> {val}. Heap size = {H.n}")
                score += 2
                # Cannot reliably map value->node id; leave nodes dict as-is.
                maybe_viz("after extract_min")
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
                maybe_viz("after decrease_key")
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
                maybe_viz("after delete")
            except Exception:
                print("That node may no longer be in the heap.")

        elif cmd == "list":
            list_nodes()

        elif cmd == "viz" and len(parts) == 2:
            opt = parts[1].lower()
            if opt == "on":
                if LiveHeapVisualizer is None:
                    print("Install: pip install networkx matplotlib")
                else:
                    viz_enabled = True
                    if viz is None:
                        viz = LiveHeapVisualizer()
                    print("Live visualization ON.")
                    maybe_viz("viz on")
            elif opt == "off":
                viz_enabled = False
                if viz is not None:
                    viz.close()
                    viz = None
                print("Live visualization OFF.")
            else:
                print("Usage: viz on | viz off")

        elif cmd == "visualize":
            if LiveHeapVisualizer is None:
                print("Install: pip install networkx matplotlib")
            else:
                if viz is None:
                    viz = LiveHeapVisualizer()
                viz.update(H, subtitle="snapshot")

        elif cmd == "score":
            print(f"Score = {score}")

        elif cmd == "quit":
            print("Exiting. Goodbye!")
            if viz is not None:
                viz.close()
            break

        else:
            print("Unknown command. Try:\n"
                  "  insert X | min | merge | extract | decrease ID NEW | delete ID | list | viz on | viz off | visualize | score | quit")

if __name__ == "__main__":
    main()
