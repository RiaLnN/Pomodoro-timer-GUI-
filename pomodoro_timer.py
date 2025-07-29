import customtkinter as ctk
import winsound

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.cycles = 4
        self.is_break = False
        self.is_stop = False
        self.is_clear = False
        self.current_cycle = 0
        self.second_left = 0

        self.container = ctk.CTkFrame(root, corner_radius=12, fg_color="#333446")
        self.container.pack(padx=20, pady=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(
            self.container,
            text="Pomodoro Timer",
            font=("Arial", 34, "bold"),
            text_color="#E5EDF1",
            fg_color="#333446",
            corner_radius=8,
            width=300,
            height=70
        )
        self.label.pack(pady=(20, 10))

        self.label_timer = ctk.CTkLabel(
            self.container,
            text="00:00",
            font=("Arial", 40, "bold"),
            text_color="#F2E9E4",
            fg_color="#7F8CAA",
            corner_radius=10,
            width=200,
            height=80
        )
        self.label_timer.pack(pady=15)

        self.button_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.cycle_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.cycle_frame.pack(fill="both", expand=True, pady=(10, 20))

        self.label_cycle = ctk.CTkLabel(
            self.cycle_frame,
            text="Cycle: 0 / 4",
            font=("Arial", 16, "bold"),
            text_color="#F2E9E4",
            fg_color="#333446",
            corner_radius=6,
            width=110,
            height=30
        )
        self.label_cycle.pack(side="bottom", anchor="se", padx=(0, 10), pady=(0, 10))

        self.btn_cfg = {
            "width": 120,
            "height": 40,
            "corner_radius": 8,
            "font": ("Arial", 14, "bold")
        }

        self.button_start = ctk.CTkButton(
            self.button_frame,
            text="Start",
            command=self.start_timer,
            fg_color="#129990",
            hover_color="#90D1CA",
            **self.btn_cfg
        )

        self.button_stop = ctk.CTkButton(
            self.button_frame,
            text="Stop",
            command=self.stop_timer,
            fg_color="#DC3C22",
            hover_color="#C87A7F",
            **self.btn_cfg
        )

        self.button_continue = ctk.CTkButton(
            self.button_frame,
            text="Continue",
            command=self.continue_timer,
            fg_color="#129990",
            hover_color="#90D1CA",
            **self.btn_cfg
        )

        self.button_clear = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            command=self.clear_timer,
            fg_color="#E55050",
            hover_color="#E89A89",
            **self.btn_cfg
        )

        self.show_buttons([self.button_start])

    def show_buttons(self, buttons):
        for widget in self.button_frame.winfo_children():
            widget.pack_forget()
        for btn in buttons:
            btn.pack(side="top", pady=8)

    def start_timer(self):
        self.button_start.pack_forget()
        self.show_buttons([self.button_stop, self.button_clear])
        self.current_cycle = 0
        self.start_work()

    def start_work(self):
        if self.current_cycle >= self.cycles:
            self.label_timer.configure(text="00:00")
            self.label.configure(text="Done!")
            self.button_stop.pack_forget()
            self.button_clear.pack_forget()
            self.show_buttons([self.button_start])
            return
        self.label.configure(text="Work Time")
        self.label_cycle.configure(text=f"Cycle: {self.current_cycle + 1}/{self.cycles}")
        self.is_break = False
        self.is_stop = False
        self.is_clear = False
        self.second_left = self.work_duration
        self.update_timer()

    def start_break(self):
        self.is_break = True
        self.label.configure(text="Break Time")
        self.second_left = self.break_duration
        self.update_timer()


    def update_timer(self):
        if self.is_clear:
            self.second_left = 0
            self.label_timer.configure(text="00:00")
            return
        else:
            mins, secs = divmod(self.second_left, 60)
            self.label_timer.configure(text=f"{mins:02d}:{secs:02d}")
            if self.is_stop:
                return
            else:
                if self.second_left > 0:
                    self.second_left -= 1
                    self.root.after(1000, self.update_timer)
                else:
                    winsound.Beep(1000, 500)
                    if self.is_break:
                        self.current_cycle += 1
                        self.start_work()
                    else:
                        self.start_break()

    def stop_timer(self):
        self.button_clear.pack_forget()
        self.is_stop = True
        self.label.configure(text="Time Is Stop")
        self.show_buttons([self.button_continue])

    def continue_timer(self):
        self.is_stop = False
        self.label.configure(text="Work Time")
        self.update_timer()
        self.show_buttons([self.button_stop, self.button_clear])

    def clear_timer(self):
        self.is_clear = True
        self.label.configure(text="Pomodoro Timer")
        self.show_buttons([self.button_start])
        self.label_cycle.configure(text="Cycle: 0 / 4")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.configure(fg_color="#333446")
app.title("Pomodoro Timer")
app.geometry("480x450")

PomodoroTimer(app)

app.mainloop()