"""
================================================
 AGRICULTURE SUPPORT SYSTEM
 PROG103 – Principle of Structured Programming
 Group 1 | DIT1201F | Limkwing University – SL
 Members: James Banya, Haja Jenabu Bah, Henry Frank Hindolo Kpanabom
================================================
 SDG Alignment:
   SDG 2  – Zero Hunger
   SDG 8  – Decent Work & Economic Growth
   SDG 15 – Life on Land
================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
APP_TITLE    = "Agriculture Support System – Sierra Leone"
APP_VERSION  = "v1.0"
PRIMARY_CLR  = "#2E7D32"   # deep green
ACCENT_CLR   = "#A5D6A7"   # light green
BG_CLR       = "#F1F8E9"   # pale green-white
TEXT_CLR     = "#1B5E20"
WHITE        = "#FFFFFF"
HEADER_FONT  = ("Tahoma", 16, "bold")
LABEL_FONT   = ("Tahoma", 10)
BUTTON_FONT  = ("Tahoma", 10, "bold")
ENTRY_FONT   = ("Tahoma", 10)

CROP_DATA = {
    "Rice":    {"season": "May – September",  "soil": "Clayey / Loamy",   "rainfall": "High (>1500mm)",  "price_per_bag": 250000},
    "Cassava": {"season": "Year-round",        "soil": "Sandy Loam",       "rainfall": "Medium (800mm)",  "price_per_bag": 80000},
    "Maize":   {"season": "April – August",    "soil": "Loamy",            "rainfall": "Medium (700mm)",  "price_per_bag": 120000},
    "Groundnut":{"season":"November – March",  "soil": "Sandy / Loam",     "rainfall": "Low (500mm)",     "price_per_bag": 180000},
    "Sweet Potato":{"season":"March – July",   "soil": "Well-drained Loam","rainfall": "Medium (600mm)",  "price_per_bag": 100000},
}

FERTILIZER_DATA = {
    "Rice":    {"npk": "15-15-15", "urea_kg_per_acre": 50, "lime": True},
    "Cassava": {"npk": "10-10-10", "urea_kg_per_acre": 30, "lime": False},
    "Maize":   {"npk": "23-10-5",  "urea_kg_per_acre": 60, "lime": True},
    "Groundnut":{"npk":"0-20-20",  "urea_kg_per_acre": 20, "lime": False},
    "Sweet Potato":{"npk":"5-15-15","urea_kg_per_acre":40, "lime": False},
}


# ─────────────────────────────────────────────
#  PROCESSING / LOGIC FUNCTIONS
# ─────────────────────────────────────────────

def calculate_yield_estimate(crop: str, land_acres: float,
                              irrigation: bool, fertilizer: bool) -> dict:
    """
    Estimate harvest yield (bags) and revenue (SLL) for a given crop.
    Returns a dict with yield_bags, revenue_sll, and grade.
    """
    base_yield = {
        "Rice": 25, "Cassava": 40, "Maize": 30,
        "Groundnut": 20, "Sweet Potato": 35
    }

    bags_per_acre = base_yield.get(crop, 20)

    # Apply decision-structure bonuses
    if irrigation:
        bags_per_acre = int(bags_per_acre * 1.25)
    if fertilizer:
        bags_per_acre = int(bags_per_acre * 1.15)

    total_bags   = bags_per_acre * land_acres
    price_per_bag = CROP_DATA[crop]["price_per_bag"]
    revenue      = total_bags * price_per_bag

    # Grade classification using decision structure
    if bags_per_acre >= 40:
        grade = "Excellent"
    elif bags_per_acre >= 30:
        grade = "Good"
    elif bags_per_acre >= 20:
        grade = "Average"
    else:
        grade = "Below Average"

    return {
        "bags_per_acre": bags_per_acre,
        "total_bags":    round(total_bags, 1),
        "revenue_sll":   int(revenue),
        "grade":         grade
    }


def get_fertilizer_recommendation(crop: str, land_acres: float) -> str:
    """
    Return a fertilizer recommendation string for a given crop & farm size.
    Demonstrates iteration and string formatting.
    """
    if crop not in FERTILIZER_DATA:
        return "No data available for selected crop."

    info       = FERTILIZER_DATA[crop]
    total_urea = info["urea_kg_per_acre"] * land_acres
    lines      = []

    lines.append(f"  Recommended NPK Ratio : {info['npk']}")
    lines.append(f"  Urea Needed           : {total_urea:.1f} kg "
                 f"({info['urea_kg_per_acre']} kg × {land_acres} acres)")
    if info["lime"]:
        lines.append("  Lime Application      : Recommended (acidic soil)")
    else:
        lines.append("  Lime Application      : Not required")

    # Iterate over application schedule
    schedule = ["Week 1 – Basal application (at planting)",
                "Week 4 – Top dressing (first)",
                "Week 8 – Top dressing (second, if needed)"]
    lines.append("\n  Application Schedule:")
    for item in schedule:
        lines.append(f"    • {item}")

    return "\n".join(lines)


def get_crop_info(crop: str) -> str:
    """Return formatted crop information string."""
    if crop not in CROP_DATA:
        return "No information available."
    info = CROP_DATA[crop]
    return (
        f"  Planting Season : {info['season']}\n"
        f"  Soil Type       : {info['soil']}\n"
        f"  Rainfall Needed : {info['rainfall']}\n"
        f"  Market Price    : SLL {info['price_per_bag']:,} / bag"
    )


def validate_inputs(land_str: str) -> tuple:
    """
    Validate user inputs. Returns (is_valid: bool, value: float | str).
    Demonstrates decision structures and error handling.
    """
    try:
        land = float(land_str)
        if land <= 0:
            return False, "Land size must be greater than 0."
        if land > 10000:
            return False, "Land size seems unrealistic (max 10,000 acres)."
        return True, land
    except ValueError:
        return False, "Please enter a valid numeric value for land size."


def format_currency(amount: int) -> str:
    """Format integer as Sierra Leone Leones string."""
    return f"SLL {amount:,}"


# ─────────────────────────────────────────────
#  GUI CLASS
# ─────────────────────────────────────────────

class AgricultureSupportApp:
    """Main GUI application class using tkinter."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configure_root()
        self._build_header()
        self._build_notebook()
        self._build_footer()

    # ── Window setup ──────────────────────────
    def _configure_root(self):
        self.root.title(f"{APP_TITLE}  {APP_VERSION}")
        self.root.geometry("820x680")
        self.root.resizable(True, True)
        self.root.configure(bg=BG_CLR)
        self.root.minsize(700, 550)

    # ── Header banner ─────────────────────────
    def _build_header(self):
        header_frame = tk.Frame(self.root, bg=PRIMARY_CLR, pady=10)
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text="🌾  Agriculture Support System",
                 font=HEADER_FONT, bg=PRIMARY_CLR, fg=WHITE).pack()
        tk.Label(header_frame,
                 text="Sierra Leone  |  SDG 2 · SDG 8 · SDG 15  |  Group 1 – DIT1201F",
                 font=("Tahoma", 9), bg=PRIMARY_CLR, fg=ACCENT_CLR).pack()

    # ── Tabbed notebook ───────────────────────
    def _build_notebook(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",        background=BG_CLR, borderwidth=0)
        style.configure("TNotebook.Tab",    font=LABEL_FONT, padding=[12, 5],
                        background=ACCENT_CLR, foreground=TEXT_CLR)
        style.map("TNotebook.Tab",
                  background=[("selected", PRIMARY_CLR)],
                  foreground=[("selected", WHITE)])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        self._build_tab_yield()
        self._build_tab_fertilizer()
        self._build_tab_cropinfo()
        self._build_tab_records()

    # ── TAB 1: Yield Estimator ────────────────
    def _build_tab_yield(self):
        frame = tk.Frame(self.notebook, bg=BG_CLR)
        self.notebook.add(frame, text="  📊 Yield Estimator  ")

        # ── Input panel
        inp = tk.LabelFrame(frame, text=" Farm Details ", font=LABEL_FONT,
                            bg=BG_CLR, fg=PRIMARY_CLR, padx=15, pady=10)
        inp.pack(fill=tk.X, padx=20, pady=(15, 5))

        # Crop
        tk.Label(inp, text="Crop Type:", font=LABEL_FONT,
                 bg=BG_CLR, fg=TEXT_CLR).grid(row=0, column=0, sticky="w", pady=5)
        self.yield_crop = ttk.Combobox(inp, values=list(CROP_DATA.keys()),
                                       font=ENTRY_FONT, state="readonly", width=20)
        self.yield_crop.set("Rice")
        self.yield_crop.grid(row=0, column=1, sticky="w", padx=10)

        # Land
        tk.Label(inp, text="Land Size (acres):", font=LABEL_FONT,
                 bg=BG_CLR, fg=TEXT_CLR).grid(row=1, column=0, sticky="w", pady=5)
        self.yield_land = tk.Entry(inp, font=ENTRY_FONT, width=22)
        self.yield_land.insert(0, "1.0")
        self.yield_land.grid(row=1, column=1, sticky="w", padx=10)

        # Checkboxes
        self.irrig_var = tk.BooleanVar()
        self.fert_var  = tk.BooleanVar()
        tk.Checkbutton(inp, text="Irrigation available",
                       variable=self.irrig_var, font=LABEL_FONT,
                       bg=BG_CLR, fg=TEXT_CLR, activebackground=BG_CLR
                       ).grid(row=2, column=0, columnspan=2, sticky="w", pady=2)
        tk.Checkbutton(inp, text="Fertilizer will be applied",
                       variable=self.fert_var, font=LABEL_FONT,
                       bg=BG_CLR, fg=TEXT_CLR, activebackground=BG_CLR
                       ).grid(row=3, column=0, columnspan=2, sticky="w", pady=2)

        # Buttons
        btn_frame = tk.Frame(frame, bg=BG_CLR)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="  Calculate Yield  ",
                  font=BUTTON_FONT, bg=PRIMARY_CLR, fg=WHITE,
                  relief=tk.FLAT, padx=10, pady=6,
                  command=self._calculate_yield).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_frame, text="  Clear  ",
                  font=BUTTON_FONT, bg="#757575", fg=WHITE,
                  relief=tk.FLAT, padx=10, pady=6,
                  command=self._clear_yield).pack(side=tk.LEFT, padx=6)

        # Output
        out = tk.LabelFrame(frame, text=" Yield Results ", font=LABEL_FONT,
                            bg=BG_CLR, fg=PRIMARY_CLR, padx=15, pady=8)
        out.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        self.yield_output = scrolledtext.ScrolledText(
            out, font=ENTRY_FONT, bg=WHITE, fg=TEXT_CLR,
            relief=tk.SUNKEN, state=tk.DISABLED, height=10, wrap=tk.WORD)
        self.yield_output.pack(fill=tk.BOTH, expand=True)

    # ── TAB 2: Fertilizer Advisor ─────────────
    def _build_tab_fertilizer(self):
        frame = tk.Frame(self.notebook, bg=BG_CLR)
        self.notebook.add(frame, text="  🌿 Fertilizer Advisor  ")

        inp = tk.LabelFrame(frame, text=" Input ", font=LABEL_FONT,
                            bg=BG_CLR, fg=PRIMARY_CLR, padx=15, pady=10)
        inp.pack(fill=tk.X, padx=20, pady=(15, 5))

        tk.Label(inp, text="Crop Type:", font=LABEL_FONT,
                 bg=BG_CLR, fg=TEXT_CLR).grid(row=0, column=0, sticky="w", pady=5)
        self.fert_crop = ttk.Combobox(inp, values=list(CROP_DATA.keys()),
                                      font=ENTRY_FONT, state="readonly", width=20)
        self.fert_crop.set("Rice")
        self.fert_crop.grid(row=0, column=1, sticky="w", padx=10)

        tk.Label(inp, text="Land Size (acres):", font=LABEL_FONT,
                 bg=BG_CLR, fg=TEXT_CLR).grid(row=1, column=0, sticky="w", pady=5)
        self.fert_land = tk.Entry(inp, font=ENTRY_FONT, width=22)
        self.fert_land.insert(0, "1.0")
        self.fert_land.grid(row=1, column=1, sticky="w", padx=10)

        btn_frame = tk.Frame(frame, bg=BG_CLR)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="  Get Recommendation  ",
                  font=BUTTON_FONT, bg=PRIMARY_CLR, fg=WHITE,
                  relief=tk.FLAT, padx=10, pady=6,
                  command=self._get_fertilizer).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_frame, text="  Clear  ",
                  font=BUTTON_FONT, bg="#757575", fg=WHITE,
                  relief=tk.FLAT, padx=10, pady=6,
                  command=self._clear_fertilizer).pack(side=tk.LEFT, padx=6)

        out = tk.LabelFrame(frame, text=" Recommendation ", font=LABEL_FONT,
                            bg=BG_CLR, fg=PRIMARY_CLR, padx=15, pady=8)
        out.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        self.fert_output = scrolledtext.ScrolledText(
            out, font=ENTRY_FONT, bg=WHITE, fg=TEXT_CLR,
            relief=tk.SUNKEN, state=tk.DISABLED, height=12, wrap=tk.WORD)
        self.fert_output.pack(fill=tk.BOTH, expand=True)

    # ── TAB 3: Crop Information ───────────────
    def _build_tab_cropinfo(self):
        frame = tk.Frame(self.notebook, bg=BG_CLR)
        self.notebook.add(frame, text="  🌱 Crop Information  ")

        inp = tk.LabelFrame(frame, text=" Select Crop ", font=LABEL_FONT,
                            bg=BG_CLR, fg=PRIMARY_CLR, padx=15, pady=10)
        inp.pack(fill=tk.X, padx=20, pady=(15, 5))

        tk.Label(inp, text="Crop:", font=LABEL_FONT,
                 bg=BG_CLR, fg=TEXT_CLR).grid(row=0, column=0, sticky="w")
        self.info_crop = ttk.Combobox(inp, values=list(CROP_DATA.keys()),
                                      font=ENTRY_FONT, state="readonly", width=20)
        self.info_crop.set("Rice")
        self.info_crop.grid(row=0, column=1, sticky="w", padx=10)
        self.info_crop.bind("<<ComboboxSelected>>", lambda e: self._show_crop_info())

        btn_frame = tk.Frame(frame, bg=BG_CLR)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="  Show Information  ",
                  font=BUTTON_FONT, bg=PRIMARY_CLR, fg=WHITE,
                  relief=tk.FLAT, padx=10, pady=6,
                  command=self._show_crop_info).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_frame, text="  Show All Crops  ",
                  font=BUTTON_FONT, bg="#388E3C", fg=WHITE,
                  relief=tk.FLAT, padx=10, pady=6,
                  command=self._show_all_crops).pack(side=tk.LEFT, padx=6)

        out = tk.LabelFrame(frame, text=" Crop Details ", font=LABEL_FONT,
                            bg=BG_CLR, fg=PRIMARY_CLR, padx=15, pady=8)
        out.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        self.info_output = scrolledtext.ScrolledText(
            out, font=ENTRY_FONT, bg=WHITE, fg=TEXT_CLR,
            relief=tk.SUNKEN, state=tk.DISABLED, height=14, wrap=tk.WORD)
        self.info_output.pack(fill=tk.BOTH, expand=True)

    # ── TAB 4: Records Log ────────────────────
    def _build_tab_records(self):
        frame = tk.Frame(self.notebook, bg=BG_CLR)
        self.notebook.add(frame, text="  📋 Session Records  ")

        tk.Label(frame,
                 text="All calculations performed in this session are logged below.",
                 font=("Tahoma", 9, "italic"), bg=BG_CLR, fg="#555").pack(pady=(12, 4))

        btn_frame = tk.Frame(frame, bg=BG_CLR)
        btn_frame.pack()
        tk.Button(btn_frame, text="  Clear Log  ",
                  font=BUTTON_FONT, bg="#B71C1C", fg=WHITE,
                  relief=tk.FLAT, padx=10, pady=5,
                  command=self._clear_log).pack()

        self.log_output = scrolledtext.ScrolledText(
            frame, font=("Courier New", 9), bg="#FAFAFA", fg="#333",
            relief=tk.SUNKEN, state=tk.DISABLED, wrap=tk.WORD)
        self.log_output.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self._log_entry("Session started – " + datetime.now().strftime("%d %b %Y  %H:%M:%S"))

    # ── Footer ────────────────────────────────
    def _build_footer(self):
        footer = tk.Frame(self.root, bg=PRIMARY_CLR, pady=4)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer,
                 text="Group 1  |  James Banya · Haja Jenaba Bah · Henry Frank Hindolo Kpanabom  |  DIT1201F  |  PROG103",
                 font=("Tahoma", 8), bg=PRIMARY_CLR, fg=ACCENT_CLR).pack()

    # ─────────────────────────────────────────
    #  EVENT HANDLERS (connect GUI ↔ logic)
    # ─────────────────────────────────────────

    def _calculate_yield(self):
        crop      = self.yield_crop.get()
        land_str  = self.yield_land.get().strip()

        valid, result = validate_inputs(land_str)
        if not valid:
            messagebox.showerror("Input Error", result)
            return

        land     = result
        irrig    = self.irrig_var.get()
        fert     = self.fert_var.get()
        data     = calculate_yield_estimate(crop, land, irrig, fert)
        timestamp = datetime.now().strftime("%H:%M:%S")

        lines = [
            f"  Crop             : {crop}",
            f"  Land Size        : {land} acres",
            f"  Irrigation       : {'Yes' if irrig else 'No'}",
            f"  Fertilizer Used  : {'Yes' if fert else 'No'}",
            "",
            f"  Yield / Acre     : {data['bags_per_acre']} bags",
            f"  Total Yield      : {data['total_bags']} bags",
            f"  Estimated Revenue: {format_currency(data['revenue_sll'])}",
            f"  Performance Grade: {data['grade']}",
            "",
            f"  [Calculated at {timestamp}]",
        ]
        text = "\n".join(lines)
        self._write_output(self.yield_output, text)
        self._log_entry(f"[YIELD] {crop} | {land} acres → {data['total_bags']} bags | "
                        f"{format_currency(data['revenue_sll'])}")

    def _clear_yield(self):
        self._write_output(self.yield_output, "")
        self.yield_land.delete(0, tk.END)
        self.yield_land.insert(0, "1.0")
        self.irrig_var.set(False)
        self.fert_var.set(False)

    def _get_fertilizer(self):
        crop     = self.fert_crop.get()
        land_str = self.fert_land.get().strip()

        valid, result = validate_inputs(land_str)
        if not valid:
            messagebox.showerror("Input Error", result)
            return

        land = result
        rec  = get_fertilizer_recommendation(crop, land)
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = (f"  Crop      : {crop}\n"
                f"  Land      : {land} acres\n\n"
                f"  Fertilizer Recommendation:\n{rec}\n\n"
                f"  [Generated at {timestamp}]")
        self._write_output(self.fert_output, text)
        self._log_entry(f"[FERTILIZER] {crop} | {land} acres → recommendation generated")

    def _clear_fertilizer(self):
        self._write_output(self.fert_output, "")
        self.fert_land.delete(0, tk.END)
        self.fert_land.insert(0, "1.0")

    def _show_crop_info(self):
        crop = self.info_crop.get()
        info = get_crop_info(crop)
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = f"  Crop: {crop}\n\n{info}\n\n  [Viewed at {timestamp}]"
        self._write_output(self.info_output, text)
        self._log_entry(f"[CROP INFO] Viewed: {crop}")

    def _show_all_crops(self):
        lines = ["  ALL SUPPORTED CROPS – SIERRA LEONE\n",
                 "  " + "─" * 52]
        for crop in CROP_DATA:
            lines.append(f"\n  ▸ {crop}")
            lines.append(get_crop_info(crop))
            lines.append("  " + "─" * 52)
        self._write_output(self.info_output, "\n".join(lines))
        self._log_entry("[CROP INFO] Viewed all crops")

    def _clear_log(self):
        self._write_output(self.log_output, "")
        self._log_entry("Log cleared – " + datetime.now().strftime("%H:%M:%S"))

    # ─────────────────────────────────────────
    #  UTILITY HELPERS
    # ─────────────────────────────────────────

    def _write_output(self, widget: scrolledtext.ScrolledText, text: str):
        """Enable widget, replace content, then disable."""
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.config(state=tk.DISABLED)

    def _log_entry(self, message: str):
        """Append a timestamped entry to the session log."""
        ts   = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}]  {message}\n"
        self.log_output.config(state=tk.NORMAL)
        self.log_output.insert(tk.END, line)
        self.log_output.see(tk.END)
        self.log_output.config(state=tk.DISABLED)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

def main():
    root = tk.Tk()
    app  = AgricultureSupportApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()