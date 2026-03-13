import customtkinter
from models.json_validator import validate_json_string

class ValidateJsonWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__()
        self.parent = parent
        self.controller = controller

        self.geometry("800x600")
        self.font = customtkinter.CTkFont(family="roboto", size=12, weight="bold")
        self.header_font = customtkinter.CTkFont(family="roboto", size=12, weight="bold")
        self.title("Validate JSON")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.attributes("-topmost", True) 
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.frame = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure((0,1), weight=1)
        self.frame.grid_rowconfigure((0), weight=1)

        # leftFrame
        self.left_frame = customtkinter.CTkFrame(master=self.frame, corner_radius=parent.frame_corner_radius, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.grid_columnconfigure((0), weight=1)
        self.left_frame.grid_rowconfigure((0), weight=1)

        self.left_inner_frame = customtkinter.CTkFrame(master=self.left_frame, corner_radius=parent.frame_corner_radius)
        self.left_inner_frame.grid(row=0, column=0, padx=parent.element_padx, pady=parent.element_pady, sticky="new")
        self.left_inner_frame.grid_columnconfigure((0), weight=1)
        self.left_inner_frame.grid_rowconfigure((0,1,2), weight=1)

        self.label = customtkinter.CTkLabel(master=self.left_inner_frame, text="JSON Data", font=self.header_font)
        self.label.grid(row=0, column=0, sticky="nw", padx=parent.element_padx, pady=parent.element_pady)

        self.text_box = customtkinter.CTkTextbox(master=self.left_inner_frame, corner_radius=parent.frame_corner_radius, height=490)
        self.text_box.grid(row=1, column=0, padx=parent.element_padx, pady=2, sticky="nsew")

        self.validate_json_btn = customtkinter.CTkButton(
            master=self.left_inner_frame,
            text="Validate JSON",
            command=self.on_validate_clicked
        )
        self.validate_json_btn.grid(row=2, column=0, sticky="new", padx=parent.element_padx, pady=parent.element_pady)

        # rightFrame
        self.right_frame = customtkinter.CTkFrame(master=self.frame, corner_radius=parent.frame_corner_radius, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid_columnconfigure((0), weight=1)
        self.right_frame.grid_rowconfigure((0), weight=1)  

        self.right_inner_frame = customtkinter.CTkFrame(master=self.right_frame, corner_radius=parent.frame_corner_radius)
        self.right_inner_frame.grid(row=0, column=0, padx=parent.element_padx, pady=parent.element_pady, sticky="new")
        self.right_inner_frame.grid_columnconfigure((0), weight=1)
        self.right_inner_frame.grid_rowconfigure((0,1), weight=1)

        self.validation_label = customtkinter.CTkLabel(master=self.right_inner_frame, text="Validation Result", font=self.header_font)
        self.validation_label.grid(row=0, column=0, sticky="nw", padx=parent.element_padx, pady=2)
       
        self.validation_text_box = customtkinter.CTkTextbox(master=self.right_inner_frame, corner_radius=parent.frame_corner_radius, height=550)
        self.validation_text_box.grid(row=1, column=0, padx=parent.element_padx, pady=parent.element_pady, sticky="nsew")

    def close_window(self):
        self.controller.close_validate_json()
        self.destroy()

    def set_json_content(self, content: str):
        self.text_box.delete("0.0", "end")
        self.text_box.insert("0.0", content)

    def on_validate_clicked(self):
        json_data = self.text_box.get("0.0", "end-1c")
        is_valid, msg = validate_json_string(json_data)
        
        self.validation_text_box.configure(state="normal")
        self.validation_text_box.delete("0.0", "end")
        self.validation_text_box.insert("0.0", msg)

        if not is_valid:
            self.validation_text_box.configure(text_color="red")
        else:
            self.validation_text_box.configure(text_color="green")
