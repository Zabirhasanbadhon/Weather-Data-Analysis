import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import pandas as pd

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    Figure = None
    FigureCanvasTkAgg = None


# ------------------------- Cream White Theme -------------------------
BG = "#F8F5EE"
SIDEBAR = "#F1EBDD"
PANEL = "#FFFCF6"
PANEL2 = "#EDE5D6"
BORDER = "#DED5C5"
TEXT = "#292524"
MUTED = "#78716C"
ACCENT = "#20A879"
BLUE = "#5486D8"
ORANGE = "#D99545"
RED = "#D95D68"
FONT = "Segoe UI"


def readable_number(value, digits=2):
    try:
        if pd.isna(value):
            return "—"
        return f"{float(value):,.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


class WeatherAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZaBir | Weather Data Analysis")
        self.root.geometry("1280x820")
        self.root.minsize(980, 680)
        self.root.configure(bg=BG)
        self.root.option_add("*Font", (FONT, 10))

        self.data = pd.DataFrame()
        self.csv_path = None
        self.filtered_data = pd.DataFrame()
        self.active_page = "Dashboard"
        self.chart_canvas = None

        self._configure_styles()
        self._build_layout()
        self._load_default_if_found()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=PANEL,
            foreground=TEXT,
            fieldbackground=PANEL,
            rowheight=29,
            borderwidth=0,
            font=(FONT, 9)
        )

        style.configure(
            "Treeview.Heading",
            background=PANEL2,
            foreground=ACCENT,
            relief="flat",
            font=(FONT, 9, "bold"),
            padding=(8, 9)
        )

        style.map(
            "Treeview",
            background=[("selected", "#D5E9DE")],
            foreground=[("selected", TEXT)]
        )

        style.map(
            "Treeview.Heading",
            background=[("active", "#E3DAC9")]
        )

        style.configure(
            "TCombobox",
            fieldbackground=PANEL2,
            background=PANEL2,
            foreground=TEXT,
            arrowcolor=ACCENT,
            padding=7
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", PANEL2)],
            foreground=[("readonly", TEXT)]
        )

        style.configure(
            "Vertical.TScrollbar",
            background=PANEL2,
            troughcolor=BG,
            bordercolor=BG,
            arrowcolor=MUTED
        )

        style.configure(
            "Horizontal.TScrollbar",
            background=PANEL2,
            troughcolor=BG,
            bordercolor=BG,
            arrowcolor=MUTED
        )

        style.configure(
            "TNotebook",
            background=BG,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background=PANEL2,
            foreground=TEXT,
            padding=(14, 8),
            font=(FONT, 9, "bold")
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", PANEL)],
            foreground=[("selected", ACCENT)]
        )

    def _build_layout(self):
        self.sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=225
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=22, pady=(27, 34))

        tk.Label(
            brand,
            text="◈",
            font=(FONT, 26, "bold"),
            fg=ACCENT,
            bg=SIDEBAR
        ).pack(side="left")

        brand_text = tk.Frame(brand, bg=SIDEBAR)
        brand_text.pack(side="left", padx=(10, 0))

        tk.Label(
            brand_text,
            text="ZaBir HaSan",
            font=(FONT, 14, "bold"),
            fg=TEXT,
            bg=SIDEBAR
        ).pack(anchor="w")

        tk.Label(
            brand_text,
            text="ZHB | WEATHERIQ",
            font=(FONT, 8, "bold"),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(anchor="w")

        tk.Label(
            self.sidebar,
            text="WORKSPACE",
            font=(FONT, 8, "bold"),
            fg="#968A78",
            bg=SIDEBAR
        ).pack(anchor="w", padx=24, pady=(0, 10))

        self.nav_buttons = {}

        for name, symbol in [
            ("Dashboard", "▦"),
            ("Data Explorer", "▤"),
            ("Analysis", "◷")
        ]:
            btn = tk.Button(
                self.sidebar,
                text=f"  {symbol}     {name}",
                anchor="w",
                command=lambda n=name: self.show_page(n),
                font=(FONT, 10, "bold"),
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=18,
                pady=13,
                bg=SIDEBAR,
                fg=MUTED,
                activebackground=PANEL2,
                activeforeground=TEXT
            )
            btn.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[name] = btn

        tk.Frame(
            self.sidebar,
            bg=BORDER,
            height=1
        ).pack(fill="x", padx=20, pady=(25, 18))

        tk.Label(
            self.sidebar,
            text="DATA SOURCE",
            font=(FONT, 8, "bold"),
            fg="#968A78",
            bg=SIDEBAR
        ).pack(anchor="w", padx=24, pady=(0, 8))

        self.source_label = tk.Label(
            self.sidebar,
            text="No CSV loaded",
            bg=SIDEBAR,
            fg=MUTED,
            font=(FONT, 9),
            wraplength=175,
            justify="left"
        )
        self.source_label.pack(anchor="w", padx=24)

        tk.Button(
            self.sidebar,
            text="＋  Open CSV",
            command=self.open_csv,
            bg=ACCENT,
            fg="#FFFFFF",
            activebackground="#36B98B",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            font=(FONT, 10, "bold"),
            cursor="hand2",
            pady=11
        ).pack(fill="x", padx=20, pady=(14, 6))

        tk.Label(
            self.sidebar,
            text="CSV • Pandas • Matplotlib",
            font=(FONT, 8),
            fg="#968A78",
            bg=SIDEBAR
        ).pack(side="bottom", pady=18)

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self.topbar = tk.Frame(self.main, bg=BG)
        self.topbar.pack(fill="x", padx=30, pady=(24, 16))

        self.page_title = tk.Label(
            self.topbar,
            text="Weather overview",
            font=(FONT, 23, "bold"),
            fg=TEXT,
            bg=BG
        )
        self.page_title.pack(side="left")

        self.top_hint = tk.Label(
            self.topbar,
            text="YOUR DATA, MADE CLEAR",
            font=(FONT, 8, "bold"),
            fg=ACCENT,
            bg=BG
        )
        self.top_hint.pack(side="right", pady=(10, 0))

        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 22)
        )

        self.show_page("Dashboard")

    def _load_default_if_found(self):
        candidates = [
            Path.cwd() / "Weather_Dataset.csv",
            Path(__file__).resolve().parent / "Weather_Dataset.csv",
        ]

        for path in candidates:
            if path.exists():
                try:
                    self.load_csv(str(path))
                    return
                except Exception:
                    pass

        self._render_empty_state()

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def _card(self, parent, title, value, subtitle, accent=ACCENT):
        frame = tk.Frame(
            parent,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        tk.Frame(
            frame,
            bg=accent,
            width=4
        ).pack(side="left", fill="y")

        inner = tk.Frame(frame, bg=PANEL)
        inner.pack(
            side="left",
            fill="both",
            expand=True,
            padx=16,
            pady=14
        )

        tk.Label(
            inner,
            text=title.upper(),
            font=(FONT, 8, "bold"),
            fg=MUTED,
            bg=PANEL
        ).pack(anchor="w")

        tk.Label(
            inner,
            text=value,
            font=(FONT, 22, "bold"),
            fg=TEXT,
            bg=PANEL
        ).pack(anchor="w", pady=(6, 1))

        tk.Label(
            inner,
            text=subtitle,
            font=(FONT, 9),
            fg=accent,
            bg=PANEL
        ).pack(anchor="w")

        return frame

    def show_page(self, name):
        self.active_page = name

        for nav_name, btn in self.nav_buttons.items():
            selected = nav_name == name
            btn.configure(
                bg=PANEL2 if selected else SIDEBAR,
                fg=ACCENT if selected else MUTED
            )

        self._clear_content()

        if name == "Dashboard":
            self.page_title.configure(text="Weather overview")
            self._dashboard()

        elif name == "Data Explorer":
            self.page_title.configure(text="Data explorer")
            self._data_explorer()

        else:
            self.page_title.configure(text="Analysis lab")
            self._analysis_page()

    def _render_empty_state(self):
        self._clear_content()

        box = tk.Frame(
            self.content,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        box.pack(fill="both", expand=True)

        tk.Label(
            box,
            text="☁",
            font=(FONT, 52),
            fg=BLUE,
            bg=PANEL
        ).pack(pady=(85, 12))

        tk.Label(
            box,
            text="Bring your weather data to life",
            font=(FONT, 20, "bold"),
            fg=TEXT,
            bg=PANEL
        ).pack()

        tk.Label(
            box,
            text="Open the Weather_Dataset.csv file you used in your notebook.\n"
                 "The dashboard will calculate statistics and build charts automatically.",
            font=(FONT, 11),
            fg=MUTED,
            bg=PANEL,
            justify="center"
        ).pack(pady=12)

        tk.Button(
            box,
            text="＋  Open CSV file",
            command=self.open_csv,
            bg=ACCENT,
            fg="#FFFFFF",
            activebackground="#36B98B",
            relief="flat",
            bd=0,
            padx=20,
            pady=11,
            font=(FONT, 10, "bold"),
            cursor="hand2"
        ).pack(pady=12)

    def _dashboard(self):
        if self.data.empty:
            self._render_empty_state()
            return

        df = self.data
        rows, cols = df.shape

        temp_col = self._find_col(
            ["Temp_C", "Temperature", "Temperature_C"]
        )
        weather_col = self._find_col(
            ["Weather Condition", "Weather", "Conditions"]
        )
        humidity_col = self._find_col(
            ["Rel Hum_%", "Relative Humidity", "Humidity"]
        )
        visibility_col = self._find_col(
            ["Visibility_km", "Visibility"]
        )

        temp_mean = (
            readable_number(df[temp_col].mean())
            if temp_col else "—"
        )

        hum_mean = (
            readable_number(df[humidity_col].mean(), 1) + "%"
            if humidity_col else "—"
        )

        vis_mean = (
            readable_number(df[visibility_col].mean()) + " km"
            if visibility_col else "—"
        )

        null_count = int(df.isna().sum().sum())

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", pady=(0, 16))

        items = [
            ("Total records", f"{rows:,}", f"{cols} columns in dataset", ACCENT),
            ("Average temperature", f"{temp_mean}°C", "Across all records", BLUE),
            ("Average humidity", hum_mean, "Relative humidity", ORANGE),
            ("Missing values", f"{null_count:,}", "Cells needing attention", RED),
        ]

        for i, item in enumerate(items):
            card = self._card(cards, *item)
            card.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=(0 if i == 0 else 10, 0)
            )
            cards.grid_columnconfigure(i, weight=1, uniform="cards")

        row = tk.Frame(self.content, bg=BG)
        row.pack(fill="both", expand=True)

        chart_panel = tk.Frame(
            row,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        chart_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 12)
        )

        chart_header = tk.Frame(chart_panel, bg=PANEL)
        chart_header.pack(fill="x", padx=18, pady=(15, 3))

        tk.Label(
            chart_header,
            text="Weather insights",
            font=(FONT, 13, "bold"),
            fg=TEXT,
            bg=PANEL
        ).pack(side="left")

        self.chart_choice = tk.StringVar(value="Weather frequency")

        combo = ttk.Combobox(
            chart_header,
            textvariable=self.chart_choice,
            state="readonly",
            values=[
                "Weather frequency",
                "Temperature distribution",
                "Temperature by weather",
                "Humidity distribution",
                "Visibility distribution",
                "Temperature vs humidity",
                "Correlation matrix"
            ],
            width=26
        )
        combo.pack(side="right")
        combo.bind(
            "<<ComboboxSelected>>",
            lambda _e: self._draw_dashboard_chart()
        )

        self.chart_area = tk.Frame(chart_panel, bg=PANEL)
        self.chart_area.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        insights = tk.Frame(
            row,
            bg=PANEL,
            width=250,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        insights.pack(side="right", fill="y")
        insights.pack_propagate(False)

        tk.Label(
            insights,
            text="QUICK INSIGHTS",
            font=(FONT, 9, "bold"),
            fg=ACCENT,
            bg=PANEL
        ).pack(anchor="w", padx=17, pady=(18, 14))

        most_common = "—"

        if weather_col:
            counts = df[weather_col].dropna().astype(str).value_counts()
            if not counts.empty:
                most_common = counts.index[0]

        self._insight(
            insights,
            "Most common condition",
            most_common
        )

        self._insight(insights, "Mean visibility", vis_mean)

        if temp_col:
            self._insight(
                insights,
                "Coldest recorded",
                f"{readable_number(df[temp_col].min())} °C"
            )

            self._insight(
                insights,
                "Warmest recorded",
                f"{readable_number(df[temp_col].max())} °C"
            )

        if humidity_col:
            self._insight(
                insights,
                "Humidity range",
                f"{readable_number(df[humidity_col].min(), 0)}–"
                f"{readable_number(df[humidity_col].max(), 0)}%"
            )

        tk.Label(
            insights,
            text="Based on the loaded CSV",
            font=(FONT, 8),
            fg=MUTED,
            bg=PANEL
        ).pack(side="bottom", anchor="w", padx=17, pady=15)

        self._draw_dashboard_chart()

    def _insight(self, parent, title, value):
        box = tk.Frame(
            parent,
            bg=PANEL2,
            padx=11,
            pady=10
        )
        box.pack(fill="x", padx=13, pady=5)

        tk.Label(
            box,
            text=title,
            font=(FONT, 8),
            fg=MUTED,
            bg=PANEL2
        ).pack(anchor="w")

        tk.Label(
            box,
            text=str(value),
            font=(FONT, 11, "bold"),
            fg=TEXT,
            bg=PANEL2,
            wraplength=195,
            justify="left"
        ).pack(anchor="w", pady=(4, 0))

    def _draw_dashboard_chart(self):
        if not hasattr(self, "chart_area") or not self.chart_area.winfo_exists():
            return

        for widget in self.chart_area.winfo_children():
            widget.destroy()

        if Figure is None:
            tk.Label(
                self.chart_area,
                text="Charts need Matplotlib.\nRun: pip install matplotlib",
                bg=PANEL,
                fg=MUTED,
                font=(FONT, 11)
            ).pack(expand=True)
            return

        df = self.data

        weather_col = self._find_col(
            ["Weather Condition", "Weather", "Conditions"]
        )
        temp_col = self._find_col(
            ["Temp_C", "Temperature", "Temperature_C"]
        )

        fig = Figure(
            figsize=(7.2, 4.3),
            dpi=100,
            facecolor=PANEL
        )

        ax = fig.add_subplot(111)
        ax.set_facecolor(PANEL)

        choice = self.chart_choice.get()

        if choice == "Weather frequency" and weather_col:
            counts = (
                df[weather_col]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .head(10)
                .sort_values()
            )

            ax.barh(
                counts.index,
                counts.values,
                color=ACCENT
            )

            ax.set_xlabel("Records", color=MUTED)

            ax.set_title(
                "Top 10 weather conditions",
                color=TEXT,
                loc="left",
                pad=14,
                fontsize=12,
                fontweight="bold"
            )

        elif choice == "Temperature distribution" and temp_col:
            values = pd.to_numeric(
                df[temp_col],
                errors="coerce"
            ).dropna()

            ax.hist(
                values,
                bins=28,
                color=BLUE,
                edgecolor=PANEL,
                alpha=0.95
            )

            ax.set_xlabel("Temperature (°C)", color=MUTED)
            ax.set_ylabel("Frequency", color=MUTED)

            ax.set_title(
                "Temperature distribution",
                color=TEXT,
                loc="left",
                pad=14,
                fontsize=12,
                fontweight="bold"
            )

        elif choice == "Temperature by weather" and weather_col and temp_col:
            means = (
                df.assign(
                    _temp=pd.to_numeric(
                        df[temp_col],
                        errors="coerce"
                    )
                )
                .groupby(weather_col)["_temp"]
                .mean()
                .dropna()
                .sort_values()
                .tail(12)
            )

            ax.barh(
                means.index.astype(str),
                means.values,
                color=ORANGE
            )

            ax.set_xlabel(
                "Average temperature (°C)",
                color=MUTED
            )

            ax.set_title(
                "Average temperature by condition",
                color=TEXT,
                loc="left",
                pad=14,
                fontsize=12,
                fontweight="bold"
            )

        elif choice == "Humidity distribution":
            hum_col = self._find_col(
                ["Rel Hum_%", "Relative Humidity", "Humidity"]
            )

            if hum_col:
                values = pd.to_numeric(
                    df[hum_col],
                    errors="coerce"
                ).dropna()

                ax.hist(
                    values,
                    bins=24,
                    color=ACCENT,
                    edgecolor=PANEL
                )

                ax.set_xlabel(
                    "Relative humidity (%)",
                    color=MUTED
                )
                ax.set_ylabel("Frequency", color=MUTED)

                ax.set_title(
                    "Humidity distribution",
                    color=TEXT,
                    loc="left",
                    pad=14,
                    fontsize=12,
                    fontweight="bold"
                )

            else:
                ax.text(
                    0.5, 0.5,
                    "Humidity column not found",
                    color=TEXT,
                    ha="center",
                    va="center",
                    transform=ax.transAxes
                )

        elif choice == "Visibility distribution":
            vis_col = self._find_col(
                ["Visibility_km", "Visibility"]
            )

            if vis_col:
                values = pd.to_numeric(
                    df[vis_col],
                    errors="coerce"
                ).dropna()

                ax.hist(
                    values,
                    bins=24,
                    color=ORANGE,
                    edgecolor=PANEL
                )

                ax.set_xlabel("Visibility", color=MUTED)
                ax.set_ylabel("Frequency", color=MUTED)

                ax.set_title(
                    "Visibility distribution",
                    color=TEXT,
                    loc="left",
                    pad=14,
                    fontsize=12,
                    fontweight="bold"
                )

            else:
                ax.text(
                    0.5, 0.5,
                    "Visibility column not found",
                    color=TEXT,
                    ha="center",
                    va="center",
                    transform=ax.transAxes
                )

        elif choice == "Temperature vs humidity":
            hum_col = self._find_col(
                ["Rel Hum_%", "Relative Humidity", "Humidity"]
            )

            if temp_col and hum_col:
                plot_df = pd.DataFrame({
                    "temperature": pd.to_numeric(
                        df[temp_col],
                        errors="coerce"
                    ),
                    "humidity": pd.to_numeric(
                        df[hum_col],
                        errors="coerce"
                    )
                }).dropna()

                ax.scatter(
                    plot_df["temperature"],
                    plot_df["humidity"],
                    s=16,
                    alpha=0.55,
                    color=BLUE,
                    edgecolors="none"
                )

                ax.set_xlabel("Temperature (°C)", color=MUTED)
                ax.set_ylabel("Humidity (%)", color=MUTED)

                ax.set_title(
                    "Temperature vs humidity",
                    color=TEXT,
                    loc="left",
                    pad=14,
                    fontsize=12,
                    fontweight="bold"
                )

            else:
                ax.text(
                    0.5, 0.5,
                    "Temperature and humidity columns are required",
                    color=TEXT,
                    ha="center",
                    va="center",
                    transform=ax.transAxes
                )

        elif choice == "Correlation matrix":
            numeric = df.select_dtypes(include="number")

            if numeric.shape[1] >= 2:
                corr = numeric.corr(numeric_only=True)

                image = ax.imshow(
                    corr,
                    cmap="coolwarm",
                    vmin=-1,
                    vmax=1,
                    aspect="auto"
                )

                ax.set_xticks(
                    range(len(corr.columns)),
                    labels=[str(c) for c in corr.columns],
                    rotation=45,
                    ha="right",
                    fontsize=7
                )

                ax.set_yticks(
                    range(len(corr.index)),
                    labels=[str(c) for c in corr.index],
                    fontsize=7
                )

                ax.set_title(
                    "Numeric feature correlation",
                    color=TEXT,
                    loc="left",
                    pad=14,
                    fontsize=12,
                    fontweight="bold"
                )

                fig.colorbar(
                    image,
                    ax=ax,
                    fraction=0.046,
                    pad=0.04
                )

            else:
                ax.text(
                    0.5, 0.5,
                    "At least two numeric columns are required",
                    color=TEXT,
                    ha="center",
                    va="center",
                    transform=ax.transAxes
                )

        else:
            ax.text(
                0.5, 0.5,
                "Required columns were not found",
                color=TEXT,
                ha="center",
                va="center",
                transform=ax.transAxes
            )

        ax.tick_params(colors=MUTED, labelsize=8)
        ax.xaxis.label.set_color(MUTED)
        ax.yaxis.label.set_color(MUTED)

        for spine in ax.spines.values():
            spine.set_color(BORDER)

        ax.grid(
            axis="x",
            color=BORDER,
            linewidth=0.6,
            alpha=0.7
        )

        ax.set_axisbelow(True)
        fig.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.chart_area
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.chart_canvas = canvas

    def _data_explorer(self):
        if self.data.empty:
            self._render_empty_state()
            return

        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", pady=(0, 8))

        tk.Label(
            top,
            text=f"{len(self.data):,} records  •  {len(self.data.columns)} columns",
            fg=MUTED,
            bg=BG,
            font=(FONT, 10)
        ).pack(side="left")

        self.table_search = tk.StringVar()

        entry = tk.Entry(
            top,
            textvariable=self.table_search,
            bg=PANEL,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=(FONT, 10),
            width=24
        )
        entry.pack(side="right", ipady=7, ipadx=8)

        tk.Label(
            top,
            text="Search all columns",
            fg=MUTED,
            bg=BG
        ).pack(side="right", padx=8)

        self.table_search.trace_add(
            "write",
            lambda *_: self._populate_table()
        )

        controls = tk.Frame(
            self.content,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        controls.pack(fill="x", pady=(0, 10))

        columns = [str(c) for c in self.data.columns]

        self.filter_column = tk.StringVar(value="All columns")
        self.filter_value = tk.StringVar()
        self.sort_column = tk.StringVar(value="No sorting")
        self.sort_order = tk.StringVar(value="Ascending")

        tk.Label(
            controls,
            text="FILTER COLUMN",
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).grid(
            row=0, column=0,
            padx=(12, 5),
            pady=(9, 3),
            sticky="w"
        )

        self.filter_combo = ttk.Combobox(
            controls,
            textvariable=self.filter_column,
            values=["All columns"] + columns,
            state="readonly",
            width=20
        )
        self.filter_combo.grid(
            row=1, column=0,
            padx=(12, 8),
            pady=(0, 10),
            sticky="ew"
        )
        self.filter_combo.bind(
            "<<ComboboxSelected>>",
            lambda _e: self._refresh_filter_values()
        )

        tk.Label(
            controls,
            text="VALUE / CATEGORY",
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).grid(
            row=0, column=1,
            padx=5,
            pady=(9, 3),
            sticky="w"
        )

        self.filter_value_combo = ttk.Combobox(
            controls,
            textvariable=self.filter_value,
            width=20
        )
        self.filter_value_combo.grid(
            row=1, column=1,
            padx=5,
            pady=(0, 10),
            sticky="ew"
        )
        self.filter_value_combo.bind(
            "<<ComboboxSelected>>",
            lambda _e: self._populate_table()
        )
        self.filter_value_combo.bind(
            "<Return>",
            lambda _e: self._populate_table()
        )

        tk.Label(
            controls,
            text="SORT BY",
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).grid(
            row=0, column=2,
            padx=5,
            pady=(9, 3),
            sticky="w"
        )

        self.sort_combo = ttk.Combobox(
            controls,
            textvariable=self.sort_column,
            values=["No sorting"] + columns,
            state="readonly",
            width=18
        )
        self.sort_combo.grid(
            row=1, column=2,
            padx=5,
            pady=(0, 10),
            sticky="ew"
        )
        self.sort_combo.bind(
            "<<ComboboxSelected>>",
            lambda _e: self._populate_table()
        )

        tk.Label(
            controls,
            text="ORDER",
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).grid(
            row=0, column=3,
            padx=5,
            pady=(9, 3),
            sticky="w"
        )

        self.sort_order_combo = ttk.Combobox(
            controls,
            textvariable=self.sort_order,
            values=["Ascending", "Descending"],
            state="readonly",
            width=12
        )
        self.sort_order_combo.grid(
            row=1, column=3,
            padx=5,
            pady=(0, 10),
            sticky="ew"
        )
        self.sort_order_combo.bind(
            "<<ComboboxSelected>>",
            lambda _e: self._populate_table()
        )

        tk.Button(
            controls,
            text="Apply",
            command=self._populate_table,
            bg=ACCENT,
            fg="#FFFFFF",
            activebackground="#36B98B",
            relief="flat",
            bd=0,
            padx=14,
            pady=7,
            font=(FONT, 9, "bold"),
            cursor="hand2"
        ).grid(
            row=1, column=4,
            padx=8,
            pady=(0, 10)
        )

        tk.Button(
            controls,
            text="Reset",
            command=self._reset_table_filters,
            bg=PANEL2,
            fg=TEXT,
            activebackground="#DED5C5",
            relief="flat",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2"
        ).grid(
            row=1, column=5,
            padx=(0, 12),
            pady=(0, 10)
        )

        for i in range(6):
            controls.grid_columnconfigure(
                i,
                weight=1 if i < 4 else 0
            )

        self._refresh_filter_values()

        wrap = tk.Frame(
            self.content,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        wrap.pack(fill="both", expand=True)

        table_frame = tk.Frame(wrap, bg=PANEL)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tree = ttk.Treeview(
            table_frame,
            show="headings"
        )

        vsb = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        hsb = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        self.tree.grid(
            row=0, column=0,
            sticky="nsew"
        )

        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        bottom = tk.Frame(wrap, bg=PANEL)
        bottom.pack(
            fill="x",
            padx=15,
            pady=(0, 12)
        )

        tk.Button(
            bottom,
            text="Export filtered CSV",
            command=self.export_filtered,
            bg=PANEL2,
            fg=ACCENT,
            activebackground="#DED5C5",
            relief="flat",
            bd=0,
            padx=13,
            pady=8,
            cursor="hand2"
        ).pack(side="right")

        self.table_count = tk.Label(
            bottom,
            text="",
            fg=MUTED,
            bg=PANEL
        )
        self.table_count.pack(side="left")

        self._populate_table()

    def _refresh_filter_values(self):
        if not hasattr(self, "filter_value_combo") or self.data.empty:
            return

        col = self.filter_column.get()

        if col == "All columns" or col not in self.data.columns:
            values = []
        else:
            values = (
                self.data[col]
                .dropna()
                .astype(str)
                .value_counts()
                .index[:500]
                .tolist()
            )

        self.filter_value_combo.configure(values=[""] + values)

        if self.filter_value.get() not in ["", *values]:
            self.filter_value.set("")

        self._populate_table()

    def _reset_table_filters(self):
        self.table_search.set("")
        self.filter_column.set("All columns")
        self.filter_value.set("")
        self.sort_column.set("No sorting")
        self.sort_order.set("Ascending")
        self._refresh_filter_values()

    def _populate_table(self):
        if not hasattr(self, "tree") or not self.tree.winfo_exists():
            return

        df = self.data.copy()

        query = (
            self.table_search.get().strip().lower()
            if hasattr(self, "table_search")
            else ""
        )

        if query:
            mask = df.astype(str).apply(
                lambda col: col.str.lower().str.contains(
                    query,
                    na=False,
                    regex=False
                )
            ).any(axis=1)

            df = df.loc[mask]

        filter_col = (
            self.filter_column.get()
            if hasattr(self, "filter_column")
            else "All columns"
        )

        filter_val = (
            self.filter_value.get().strip()
            if hasattr(self, "filter_value")
            else ""
        )

        if filter_val and filter_col in df.columns:
            df = df[df[filter_col].astype(str) == filter_val]

        sort_col = (
            self.sort_column.get()
            if hasattr(self, "sort_column")
            else "No sorting"
        )

        if sort_col in df.columns:
            try:
                df = df.sort_values(
                    by=sort_col,
                    ascending=self.sort_order.get() != "Descending",
                    na_position="last",
                    kind="stable"
                )
            except (TypeError, ValueError):
                df = df.sort_values(
                    by=sort_col,
                    key=lambda col: col.astype(str).str.lower(),
                    ascending=self.sort_order.get() != "Descending",
                    na_position="last",
                    kind="stable"
                )

        self.filtered_data = df

        columns = list(self.data.columns)

        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = columns

        for col in columns:
            self.tree.heading(col, text=str(col))
            self.tree.column(
                col,
                width=max(115, min(190, len(str(col)) * 10)),
                minwidth=90,
                stretch=True
            )

        for _, row in df.head(1500).iterrows():
            vals = [
                "" if pd.isna(v) else str(v)
                for v in row.tolist()
            ]
            self.tree.insert("", "end", values=vals)

        suffix = (
            " (first 1,500 displayed)"
            if len(df) > 1500 else ""
        )

        self.table_count.configure(
            text=f"Showing {min(len(df), 1500):,} of "
                 f"{len(df):,} matching rows{suffix}"
        )

    def _analysis_page(self):
        if self.data.empty:
            self._render_empty_state()
            return

        df = self.data

        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", pady=(0, 14))

        tk.Label(
            top,
            text="Explore summary statistics and condition-level comparisons.",
            fg=MUTED,
            bg=BG,
            font=(FONT, 10)
        ).pack(side="left")

        tabs = ttk.Notebook(self.content)
        tabs.pack(fill="both", expand=True)

        stats_tab = tk.Frame(tabs, bg=PANEL)
        missing_tab = tk.Frame(tabs, bg=PANEL)
        group_tab = tk.Frame(tabs, bg=PANEL)

        tabs.add(stats_tab, text="  Summary statistics  ")
        tabs.add(missing_tab, text="  Missing values  ")
        tabs.add(group_tab, text="  By weather condition  ")

        self._make_text_table(
            stats_tab,
            df.describe(include="all")
            .round(3)
            .reset_index()
            .rename(columns={"index": "Statistic"})
        )

        missing = pd.DataFrame({
            "Column": df.columns,
            "Missing values": df.isna().sum().values,
            "Missing %": (df.isna().mean().values * 100).round(2),
            "Non-null values": df.notna().sum().values,
            "Data type": [str(t) for t in df.dtypes],
        })

        self._make_text_table(missing_tab, missing)

        weather_col = self._find_col(
            ["Weather Condition", "Weather", "Conditions"]
        )

        numeric = df.select_dtypes(include="number")

        if weather_col and not numeric.empty:
            grouped = (
                df.groupby(weather_col)[numeric.columns]
                .mean()
                .round(2)
                .reset_index()
            )
            self._make_text_table(group_tab, grouped)

        else:
            tk.Label(
                group_tab,
                text="A weather-condition column and numeric columns "
                     "are needed for this comparison.",
                bg=PANEL,
                fg=MUTED
            ).pack(padx=20, pady=20)

    def _make_text_table(self, parent, frame):
        outer = tk.Frame(parent, bg=PANEL)
        outer.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        tree = ttk.Treeview(
            outer,
            columns=list(frame.columns),
            show="headings"
        )

        vsb = ttk.Scrollbar(
            outer,
            orient="vertical",
            command=tree.yview
        )

        hsb = ttk.Scrollbar(
            outer,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        for col in frame.columns:
            tree.heading(col, text=str(col))
            tree.column(
                col,
                width=max(115, min(200, len(str(col)) * 10)),
                minwidth=90,
                stretch=True
            )

        for _, row in frame.iterrows():
            values = []

            for value in row.tolist():
                if pd.isna(value):
                    values.append("—")
                elif isinstance(value, float):
                    values.append(readable_number(value, 3))
                else:
                    values.append(str(value))

            tree.insert("", "end", values=values)

    def _find_col(self, options):
        if self.data.empty:
            return None

        for option in options:
            if option in self.data.columns:
                return option

        lower_map = {
            str(c).strip().lower(): c
            for c in self.data.columns
        }

        for option in options:
            if option.strip().lower() in lower_map:
                return lower_map[option.strip().lower()]

        return None

    def open_csv(self):
        filename = filedialog.askopenfilename(
            title="Select weather dataset",
            filetypes=[
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )

        if filename:
            try:
                self.load_csv(filename)
            except Exception as exc:
                messagebox.showerror(
                    "Could not open CSV",
                    f"Unable to read this file:\n\n{exc}"
                )

    def load_csv(self, filename):
        df = pd.read_csv(filename)

        if df.empty:
            raise ValueError("The selected CSV contains no data.")

        self.data = df
        self.csv_path = Path(filename)

        self.source_label.configure(
            text=self.csv_path.name,
            fg=TEXT
        )

        self.top_hint.configure(
            text=f"LOADED • {len(df):,} ROWS"
        )

        self.show_page(
            self.active_page if self.active_page else "Dashboard"
        )

    def export_filtered(self):
        if self.filtered_data.empty:
            messagebox.showinfo(
                "Nothing to export",
                "There are no matching rows to export."
            )
            return

        filename = filedialog.asksaveasfilename(
            title="Export filtered data",
            defaultextension=".csv",
            initialfile="weather_filtered.csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if filename:
            self.filtered_data.to_csv(filename, index=False)

            messagebox.showinfo(
                "Export complete",
                f"Saved {len(self.filtered_data):,} rows to:\n{filename}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherAnalysisApp(root)
    root.mainloop()