import cv2
import tkinter as tk
from tkinter import Text
from PIL import Image, ImageTk
from hand_detector import HandDetector


class SignLanguageUI:
    def __init__(self, window):
        self.window = window
        self.window.title("SIGNOVA")
        self.window.geometry("1280x720")
        self.window.configure(bg="#F5F7FA")

        self.cap = None
        self.running = False
        self.detector = HandDetector(model_path="best.pt")

        self.last_appended_label = ""
        self.stable_count = 0
        self.STABLE_THRESHOLD = 15

        # ---------------- TITLE ----------------
        title = tk.Label(
            self.window,
            text="WELCOME TO SIGNOVA\nAn AI Based Sign Language Recognition System",
            font=("Segoe UI", 18, "bold"),
            bg="#F5F7FA",
            fg="#3A3A3A"
        )
        title.pack(pady=20)

        # ---------------- START BUTTON ----------------
        self.start_page_btn = tk.Button(
            self.window,
            text="Start Camera",
            font=("Segoe UI", 13),
            width=18,
            bg="#B8D8BA",
            fg="#1F3D2B",
            activebackground="#A5CDA7",
            relief="flat",
            command=self.start_camera_ui
        )
        self.start_page_btn.pack(pady=80)

        # ---------------- MAIN CONTENT FRAME (camera + reference side by side) ----------------
        self.main_frame = tk.Frame(self.window, bg="#F5F7FA")

        # Left: camera
        self.cam_frame = tk.Frame(
            self.main_frame,
            bg="#E8EEF7",
            bd=2,
            relief="ridge"
        )
        self.video_label = tk.Label(
            self.cam_frame,
            bg="#D6E4F0",
            width=480,
            height=360
        )
        self.video_label.pack(padx=5, pady=5)

        # Right: ASL reference image
        self.ref_frame = tk.Frame(self.main_frame, bg="#F5F7FA")

        ref_title = tk.Label(
            self.ref_frame,
            text="ASL Reference Chart",
            font=("Segoe UI", 11, "bold"),
            bg="#F5F7FA",
            fg="#3A3A3A"
        )
        ref_title.pack(pady=(0, 5))

        try:
            asl_img = Image.open("asl_letters.jpg")
            asl_img = asl_img.resize((320, 360), Image.LANCZOS)
            self.asl_photo = ImageTk.PhotoImage(asl_img)
            ref_label = tk.Label(
                self.ref_frame,
                image=self.asl_photo,
                bg="#F5F7FA",
                bd=2,
                relief="ridge"
            )
            ref_label.pack()
        except FileNotFoundError:
            tk.Label(
                self.ref_frame,
                text="asl_letters.jpg\nnot found!",
                font=("Segoe UI", 10),
                bg="#F5F7FA",
                fg="red"
            ).pack()

        # ---------------- CONTROL BUTTONS ----------------
        self.control_frame = tk.Frame(self.window, bg="#F5F7FA")

        self.close_btn = tk.Button(
            self.control_frame,
            text="Close Camera",
            font=("Segoe UI", 11),
            width=14,
            bg="#F2C6C2",
            fg="#5A1E1E",
            activebackground="#E8B2AE",
            relief="flat",
            command=self.close_camera
        )
        self.clear_btn = tk.Button(
            self.control_frame,
            text="Clear Text",
            font=("Segoe UI", 11),
            width=14,
            bg="#BFD7ED",
            fg="#1F3D5A",
            activebackground="#AAC9E6",
            relief="flat",
            command=self.clear_text
        )
        self.space_btn = tk.Button(
            self.control_frame,
            text="Space",
            font=("Segoe UI", 11),
            width=14,
            bg="#D8E8D8",
            fg="#1F3D2B",
            activebackground="#C5DCC5",
            relief="flat",
            command=lambda: self.text_box.insert(tk.END, " ")
        )
        self.backspace_btn = tk.Button(
            self.control_frame,
            text="⌫ Backspace",
            font=("Segoe UI", 11),
            width=14,
            bg="#F5E6C8",
            fg="#5A3E1E",
            activebackground="#EDD9A3",
            relief="flat",
            command=self.backspace_text
        )

        # ---------------- TEXT FRAME ----------------
        self.text_frame = tk.Frame(
            self.window,
            bg="#E8EEF7",
            bd=2,
            relief="ridge"
        )
        text_label = tk.Label(
            self.text_frame,
            text="TEXTBOX",
            font=("Segoe UI", 12, "bold"),
            bg="#E8EEF7",
            fg="#3A3A3A"
        )
        text_label.pack(anchor="w", padx=10, pady=(8, 2))

        text_container = tk.Frame(self.text_frame, bg="#E8EEF7")
        text_container.pack(padx=10, pady=(0, 10))

        self.text_box = Text(
            text_container,
            height=5,
            width=65,
            font=("Segoe UI", 11),
            bg="#FFFFFF",
            fg="#333333",
            bd=0,
            wrap="word"
        )
        self.text_box.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            text_container,
            orient="vertical",
            command=self.text_box.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.text_box.config(yscrollcommand=scrollbar.set)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------------- UI TRANSITION ----------------
    def start_camera_ui(self):
        self.start_page_btn.pack_forget()

        # Show camera and reference image side by side
        self.main_frame.pack(pady=10)
        self.cam_frame.pack(side="left", padx=(10, 5))
        self.ref_frame.pack(side="left", padx=(5, 10))

        self.control_frame.pack(pady=10)
        self.close_btn.grid(row=0, column=0, padx=8)
        self.clear_btn.grid(row=0, column=1, padx=8)
        self.space_btn.grid(row=0, column=2, padx=8)
        self.backspace_btn.grid(row=0, column=3, padx=8)
        self.text_frame.pack(pady=10)

        self.start_camera()

    # ---------------- CAMERA FUNCTIONS ----------------
    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.update_frame()

    def update_frame(self):
        if not self.running:
            return

        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = self.detector.process(frame)

                # Smart label appending
                label = self.detector.last_label
                if label:
                    if label == self.last_appended_label:
                        self.stable_count += 1
                    else:
                        self.stable_count = 0
                        self.last_appended_label = label

                    if self.stable_count == self.STABLE_THRESHOLD:
                        self.text_box.insert(tk.END, label)
                        self.text_box.see(tk.END)
                        self.stable_count = 0
                else:
                    self.stable_count = 0
                    self.last_appended_label = ""

                frame = cv2.resize(frame, (480, 360))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

        if self.running:
            self.window.after(15, self.update_frame)

    # ---------------- CONTROL FUNCTIONS ----------------
    def close_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None

        self.video_label.config(image="")
        self.main_frame.pack_forget()
        self.cam_frame.pack_forget()
        self.ref_frame.pack_forget()
        self.control_frame.pack_forget()
        self.text_frame.pack_forget()
        self.start_page_btn.pack(pady=80)

        self.stable_count = 0
        self.last_appended_label = ""

    def clear_text(self):
        self.text_box.delete("1.0", tk.END)

    def backspace_text(self):
        content = self.text_box.get("1.0", tk.END)
        if len(content) > 1:
            self.text_box.delete("end-2c", tk.END)

    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.window.destroy()


# ---------------- MAIN ----------------
root = tk.Tk()
app = SignLanguageUI(root)
root.mainloop()