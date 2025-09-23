from src.fibonacci_heap import FibonacciHeap

def main():
    H = FibonacciHeap()
    score = 0

    print("=== Fibonacci Heap Demo Game ===")
    print("Type a command and press Enter:")
    print("  insert X   -> insert number X ")
    print("  min        -> show the current minimum ")
    print("  merge      -> merge a mini-heap [demo only] ")
    print("  extract    -> (Baren's task, coming soon)")
    print("  decrease   -> (Harishman's task, coming soon)")
    print("  delete     -> (Harishman's task, coming soon)")
    print("  score      -> check your score")
    print("  quit       -> exit the game")
    print("=================================")

    while True:
        cmd = input("> ").strip().split()
        if not cmd:
            continue

        if cmd[0] == "insert" and len(cmd) == 2:
            try:
                x = int(cmd[1])
                H.insert(x)
                print(f"Inserted {x}. Heap size = {H.n}")
                score += 1
            except ValueError:
                print("Please enter a valid number.")

        elif cmd[0] == "min":
            try:
                m = H.minimum()
                print(f"The current minimum is {m}")
                score += 1
            except IndexError:
                print("Heap is empty. Insert something first!")

        elif cmd[0] == "merge":
            other = FibonacciHeap()
            for y in [42, 17]:
                other.insert(y)
            H.merge(other)
            print("Merged a small demo heap with [42, 17]")
            print(f"New minimum is {H.minimum()}")
            score += 2

        elif cmd[0] == "extract":
            print("extract_min not yet implemented (Baren will add this).")

        elif cmd[0] == "decrease":
            print("decrease_key not yet implemented (Harishman will add this).")

        elif cmd[0] == "delete":
            print("delete not yet implemented (Harishman will add this).")

        elif cmd[0] == "score":
            print(f"Your score = {score}")

        elif cmd[0] == "quit":
            print("Exiting the Fibonacci Heap Demo. Goodbye!")
            break

        else:
            print("Unknown command. Try: insert, min, merge, extract, decrease, delete, score, quit.")

if __name__ == "__main__":
    main()
