# scripts/visualization.py
import matplotlib.pyplot as plt
import networkx as nx

class LiveHeapVisualizer:
    """
    Live non-blocking visualization for a Fibonacci Heap using matplotlib + networkx.
    - Call viz.update(heap) after each operation to redraw.
    - Use viz.close() at the end if you want to close the window.
    """
    def __init__(self, title="Fibonacci Heap (Live)"):
        plt.ion()  # interactive mode: don't block input()
        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        try:
            self.fig.canvas.manager.set_window_title(title)
        except Exception:
            pass

    def _build_graph(self, H):
        G = nx.DiGraph()
        if H.min is None:
            return G

        def traverse_ring(start, parent=None):
            node = start
            first = True
            while first or node is not start:
                first = False
                G.add_node(id(node), label=str(node.key))
                if parent is not None:
                    G.add_edge(id(parent), id(node))
                if node.child is not None:
                    traverse_ring(node.child, node)
                node = node.right

        traverse_ring(H.min, parent=None)
        return G

    def update(self, H, subtitle=""):
        self.ax.clear()
        if H.min is None:
            self.ax.set_title("Heap is empty" + (f" — {subtitle}" if subtitle else ""))
            self.ax.axis("off")
            self.fig.canvas.draw(); self.fig.canvas.flush_events()
            plt.pause(0.001)
            return

        G = self._build_graph(H)
        labels = nx.get_node_attributes(G, "label")

        pos = nx.spring_layout(G, seed=42)
        nx.draw_networkx(G, pos, ax=self.ax, with_labels=False, node_size=900)
        nx.draw_networkx_labels(G, pos, labels=labels, ax=self.ax, font_size=10)

        self.ax.set_title(f"Min = {H.minimum()} | Size = {H.n}" + (f" — {subtitle}" if subtitle else ""))
        self.ax.axis("off")
        self.fig.tight_layout()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.001)

    def close(self):
        try:
            plt.ioff()
            plt.close(self.fig)
        except Exception:
            pass
