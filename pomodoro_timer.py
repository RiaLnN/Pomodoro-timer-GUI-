import customtkinter as ctk
import tkinter as tk
import winsound

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.work_seconds_passed = 0
        self.cycles = 4
        self.is_break = False
        self.is_stop = False
        self.is_clear = False
        self.flashing = False
        self.flash_state = False
        self.current_cycle = 0
        self.second_left = 0
        self.progress_color = "#81E7AF"
        self.timer_job = None
        self.timer_running = False

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
        self.progressbar_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.progressbar_frame.pack(pady=10)
        self.progressbar_canvas = tk.Canvas(
            self.progressbar_frame,
            width=300,
            height=15,
            bg="#1e1f2e",
            highlightthickness=0
        )


        self.cycle_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.cycle_frame.pack(fill="both", expand=True, pady=(10, 10))

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
        self.show_buttons([self.button_start])

    def show_buttons(self, buttons):
        for widget in self.button_frame.winfo_children():
            widget.pack_forget()
        for btn in buttons:
            btn.pack(side="top", pady=8)

    def start_timer(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.button_start.pack_forget()
        self.stop_flashing_effect()
        self.progressbar_canvas.pack(pady=10)
        self.show_buttons([self.button_stop, self.button_clear])
        self.work_seconds_passed = 0
        self.current_cycle = 0
        self.start_work()

    def start_work(self):
        self.progress_color = "#81E7AF"
        self.label.configure(text="Work Time")
        self.label_cycle.configure(text=f"Cycle: {self.current_cycle + 1}/{self.cycles}")
        self.is_break = False
        self.is_stop = False
        self.is_clear = False
        self.timer_running = True
        self.second_left = self.work_duration
        self.update_timer()
        self.schedule_tick()

    def start_break(self):
        self.is_break = True
        self.timer_running = True
        self.progress_color = "#129990"
        self.label.configure(text="Break Time")
        self.second_left = self.break_duration
        self.update_timer()
        self.schedule_tick()

    def update_timer(self):
        if self.is_clear or not self.timer_running:
            return

        mins, secs = divmod(self.second_left, 60)
        self.label_timer.configure(text=f"{mins:02d}:{secs:02d}")
        self.progress_bar()

    def schedule_tick(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)

        self.timer_job = self.root.after(1000, self.tick)

    def tick(self):
        if not self.timer_running:
            return

        if self.second_left > 0:
            self.second_left -= 1
            if not self.is_break:
                self.work_seconds_passed += 1
            self.update_timer()
            self.schedule_tick()
        else:
            self.timer_running = False
            winsound.Beep(1000, 500)

            if self.is_break:
                self.current_cycle += 1
                self.start_work()
            elif self.current_cycle >= self.cycles - 1:
                self.label_timer.configure(text="00:00")
                self.label.configure(text="Done!")
                self.button_stop.pack_forget()
                self.button_clear.pack_forget()
                self.show_buttons([self.button_start])
                self.progress_color = "#077A7D"
                self.start_flashing_effect()
            else:
                self.start_break()

    def start_flashing_effect(self):
        self.flashing = True
        self.flash_state = True
        self.flash()

    def flash(self):
        if not self.flashing:
            return

        if self.flash_state:
            self.label_timer.configure(text_color="#FF5E5E")
        else:
            self.label_timer.configure(text_color="#F2E9E4")

        self.flash_state = not self.flash_state
        self.root.after(400, self.flash)

    def stop_flashing_effect(self):
        self.flashing = False
        self.label_timer.configure(text_color="#F2E9E4")

    def stop_timer(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_running = False
        self.button_clear.pack_forget()
        self.is_stop = True
        self.label.configure(text="Time Is Stop")
        self.progress_color = "#F4631E"
        self.progress_bar()
        self.show_buttons([self.button_continue])

    def continue_timer(self):
        self.is_stop = False
        self.timer_running = True
        if self.is_break:
            self.label.configure(text="Break Time")
            self.progress_color = "#077A7D"
        else:
            self.label.configure(text="Work Time")
            self.progress_color = "#81E7AF"
        self.update_timer()
        self.schedule_tick()
        self.show_buttons([self.button_stop, self.button_clear])

    def clear_timer(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.is_clear = True
        self.timer_running = False
        self.label.configure(text="Pomodoro Timer")
        self.show_buttons([self.button_start])
        self.second_left = 0
        self.label_timer.configure(text="00:00")
        self.label_cycle.configure(text="Cycle: 0 / 4")
        self.progressbar_canvas.pack_forget()

    def progress_bar(self):
        total_time = self.work_duration * self.cycles
        progress = self.work_seconds_passed / total_time
        self.progressbar_canvas.delete("all")
        self.progressbar_canvas.create_rectangle(0, 0, 300, 15, fill="#444", outline="")
        self.progressbar_canvas.create_rectangle(
            0, 0, 300 * progress, 15, fill=self.progress_color, outline="")
        for i in range(1, self.cycles):
            x = (300 / self.cycles) * i
            self.progressbar_canvas.create_line(x, 0, x, 15, fill="#2c2d3a")





ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.configure(fg_color="#333446")
app.title("Pomodoro Timer")
app.geometry("480x525")

PomodoroTimer(app)

app.mainloop()