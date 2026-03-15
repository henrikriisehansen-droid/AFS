import customtkinter

class NotificationPopup(customtkinter.CTkToplevel):
    """A lightweight, auto-dismissable notification popup for errors or info messages."""

    STYLE = {
        "error":   {"title": "Error",   "icon": "✗", "title_color": "#FF5555", "btn_color": "#FF5555", "btn_hover": "#CC3333"},
        "warning": {"title": "Warning", "icon": "⚠", "title_color": "#FFAA00", "btn_color": "#FFAA00", "btn_hover": "#CC8800"},
        "info":    {"title": "Info",    "icon": "ℹ", "title_color": "#55AAFF", "btn_color": "#337ACC", "btn_hover": "#2255AA"},
        "success": {"title": "Success", "icon": "✔", "title_color": "#55CC88", "btn_color": "#339966", "btn_hover": "#227755"},
    }

    def __init__(self, parent, message: str, level: str = "error"):
        super().__init__(parent)

        style = self.STYLE.get(level, self.STYLE["error"])

        self.title(style["title"])
        self.geometry("400x180")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.grab_set()  # Modal behaviour

        # Centre on parent
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width() // 2 - 200
        py = parent.winfo_rooty() + parent.winfo_height() // 2 - 90
        self.geometry(f"+{px}+{py}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header bar
        header = customtkinter.CTkFrame(master=self, fg_color=style["title_color"], corner_radius=0, height=40)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(0, weight=1)

        icon_font = customtkinter.CTkFont(family="roboto", size=18, weight="bold")
        customtkinter.CTkLabel(
            master=header,
            text=f"  {style['icon']}  {style['title']}",
            font=icon_font,
            text_color="white",
            fg_color="transparent"
        ).grid(row=0, column=0, sticky="w", padx=10, pady=6)

        # Body
        body = customtkinter.CTkFrame(master=self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=16, pady=(12, 8))
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(0, weight=1)

        msg_font = customtkinter.CTkFont(family="roboto", size=12)
        customtkinter.CTkLabel(
            master=body,
            text=message,
            font=msg_font,
            wraplength=360,
            justify="left",
            anchor="w"
        ).grid(row=0, column=0, sticky="w")

        # OK button
        customtkinter.CTkButton(
            master=body,
            text="OK",
            width=80,
            fg_color=style["btn_color"],
            hover_color=style["btn_hover"],
            command=self.destroy
        ).grid(row=1, column=0, sticky="e", pady=(10, 0))

        self.protocol("WM_DELETE_WINDOW", self.destroy)


def show_notification(parent, message: str, level: str = "error"):
    """Helper to fire a notification popup from anywhere with a parent widget reference."""
    NotificationPopup(parent, message, level)
