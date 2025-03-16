import tkinter as tk
from tkinter import messagebox
import random

# تنظیمات اولیه
WIDTH = 600
HEIGHT = 600
SQUARE_SIZE = 20
SPEED_OPTIONS = [100, 80, 60, 40]  # چهار سطح سرعت (بالاترین عدد = کندتر)
COLOR_OPTIONS = ["green", "blue", "red", "yellow"]

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.speed = SPEED_OPTIONS[0]
        self.snake_color = COLOR_OPTIONS[0]

        # منوی اصلی
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack()

        tk.Label(self.menu_frame, text="Snake Game", font=("Arial", 20)).pack(pady=10)

        tk.Label(self.menu_frame, text="Select Speed:").pack()
        self.speed_var = tk.IntVar(value=self.speed)
        for idx, speed in enumerate(SPEED_OPTIONS):
            tk.Radiobutton(self.menu_frame, text=f"Level {idx + 1}", variable=self.speed_var, value=speed).pack()

        tk.Label(self.menu_frame, text="Select Color:").pack()
        self.color_var = tk.StringVar(value=self.snake_color)
        for color in COLOR_OPTIONS:
            tk.Radiobutton(self.menu_frame, text=color.capitalize(), variable=self.color_var, value=color).pack()

        tk.Button(self.menu_frame, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        self.speed = self.speed_var.get()
        self.snake_color = self.color_var.get()
        self.menu_frame.destroy()

        # صفحه بازی
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # متغیرهای بازی
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.direction = "Right"
        self.score = 0

        # نمایش امتیاز
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 14), fg="white", bg="black")
        self.score_label.pack()

        # بستن بازی با دکمه Esc
        self.root.bind("<Escape>", lambda event: self.end_game())

        # کلیدهای جهت‌دار
        self.root.bind("<KeyPress>", self.change_direction)

        # شروع حلقه بازی
        self.next_turn()

    def create_food(self):
        while True:
            x = random.randint(0, (WIDTH - SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE
            y = random.randint(0, (HEIGHT - SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE
            if (x, y) not in self.snake:
                return x, y

    def next_turn(self):
        x, y = self.snake[0]

        if self.direction == "Up":
            y -= SQUARE_SIZE
        elif self.direction == "Down":
            y += SQUARE_SIZE
        elif self.direction == "Left":
            x -= SQUARE_SIZE
        elif self.direction == "Right":
            x += SQUARE_SIZE

        # بررسی برخورد با دیوار یا خود مار
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or (x, y) in self.snake:
            self.end_game()
            return

        self.snake.insert(0, (x, y))

        # بررسی برخورد با غذا
        if (x, y) == self.food:
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            self.food = self.create_food()
        else:
            self.snake.pop()

        # رسم مار و غذا
        self.canvas.delete("all")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + SQUARE_SIZE, segment[1] + SQUARE_SIZE, fill=self.snake_color)
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + SQUARE_SIZE, self.food[1] + SQUARE_SIZE, fill="red")

        # تاخیر برای حرکت بعدی
        self.root.after(self.speed, self.next_turn)

    def change_direction(self, event):
        new_direction = event.keysym
        if new_direction in ["Up", "Down", "Left", "Right"]:
            opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if new_direction != opposites.get(self.direction):
                self.direction = new_direction

    def end_game(self):
        self.canvas.destroy()
        self.score_label.destroy()
        messagebox.showinfo("Game Over", f"Your score: {self.score}")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()    