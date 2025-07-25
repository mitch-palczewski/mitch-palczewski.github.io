import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, vertical=True, horizontal=False, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.v_scroll = tk.Scrollbar(self, orient="vertical",
                                     command=self.canvas.yview) if vertical else None
        self.h_scroll = tk.Scrollbar(self, orient="horizontal",
                                     command=self.canvas.xview) if horizontal else None
        if self.v_scroll:
            self.canvas.configure(yscrollcommand=self.v_scroll.set)
            self.v_scroll.pack(side="right", fill="y")
        if self.h_scroll:
            self.canvas.configure(xscrollcommand=self.h_scroll.set)
            self.h_scroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollable_frame = tk.Frame(self.canvas)
        self.window_id = self.canvas.create_window((0, 0),
                                                   window=self.scrollable_frame,
                                                   anchor="nw")

        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self._bind_scroll_events()

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        if self.h_scroll is None:
            self.canvas.itemconfig(self.window_id, width=event.width)
        if self.v_scroll is None:
            self.canvas.itemconfig(self.window_id, height=event.height)

    def _bind_scroll_events(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)
        for key in ("<Up>", "<Down>", "<Left>", "<Right>"):
            self.canvas.bind_all(key, self._on_arrow)

    def _on_mousewheel(self, event):
        delta = 0
        if event.num == 4 or event.delta > 0:
            delta = -1
        elif event.num == 5 or event.delta < 0:
            delta = 1
        if (event.state & 0x0001) and self.h_scroll:
            self.canvas.xview_scroll(delta, "units")
        elif self.v_scroll:
            self.canvas.yview_scroll(delta, "units")

    def _on_arrow(self, event):
        if event.keysym in ("Up", "Down") and self.v_scroll:
            dirn = -1 if event.keysym == "Up" else 1
            self.canvas.yview_scroll(dirn, "units")
        if event.keysym in ("Left", "Right") and self.h_scroll:
            dirn = -1 if event.keysym == "Left" else 1
            self.canvas.xview_scroll(dirn, "units")

    def get_scrollable_frame(self):
        """Return the inner frame to place widgets into."""
        return self.scrollable_frame

if __name__ == "__main__":
  root = tk.Tk()
  root.geometry("400x300")

  scroll_frame = ScrollableFrame(root, vertical=True, horizontal=True, bg="lightgray")
  scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

  inner = scroll_frame.get_scrollable_frame()
  for i in range(50):
      tk.Label(inner, text=f"Item {i+1}").grid(row=i, column=0, padx=5, pady=2)

  root.mainloop()