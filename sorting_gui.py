
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
import threading

class SortingVisualizer:
    def draw_data(self, color_array):
        self.canvas.delete("all")
        c_height = 450
        c_width = 1000
        bar_width = c_width / (len(self.data) + 1)
        offset = 30
        normalized_data = [i / max(self.data) for i in self.data] if self.data else []

        comparison_color = "#ff6666"  
        swap_color = "#66ccff"        
        default_color = "#cccccc"    
        sorted_color = "#66ff66"      

        for i, height in enumerate(normalized_data):
            x0 = i * bar_width + offset
            y0 = c_height - height * 400
            x1 = (i + 1) * bar_width
            y1 = c_height

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i], outline="")
            self.canvas.create_text(x0 + bar_width/2, y0 - 10, text=str(self.data[i]), fill="black", font=("Arial", 9, "bold"))

        self.root.update_idletasks()

    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Sorting Visualizer")
        self.root.configure(bg="#f7f7f7")

        self.algorithms = {
            "Bubble Sort": self.bubble_sort,
            "Selection Sort": self.selection_sort,
            "Insertion Sort": self.insertion_sort,
            "Merge Sort": self.merge_sort_wrapper,
            "Quick Sort": self.quick_sort_wrapper,
            "Heap Sort": self.heap_sort,
            "Shell Sort": self.shell_sort
        }

        self.data = []
        self.speed = 0.1
        self.sorting = False
        self.paused = False
        self.swap_count = 0
        self.start_time = None
        
        self.start_sorting_thread = lambda: threading.Thread(target=self.start_sorting).start()
        self.setup_ui()
        

    def setup_ui(self):
        control_frame = tk.Frame(self.root, bg="#f7f7f7")
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Enter Numbers:", bg="#f7f7f7").grid(row=0, column=0)
        self.entry = tk.Entry(control_frame, width=40)
        self.entry.grid(row=0, column=1, padx=5)

        tk.Button(control_frame, text="Random Array", command=self.generate_random).grid(row=0, column=2)
        tk.Button(control_frame, text="Start Sort", command=self.start_sorting_thread).grid(row=0, column=3, padx=5)
        tk.Button(control_frame, text="Pause/Resume", command=self.toggle_pause).grid(row=0, column=4)
        tk.Button(control_frame, text="Reset", command=self.reset).grid(row=0, column=5)

        tk.Label(control_frame, text="Algorithm:", bg="#f7f7f7").grid(row=1, column=0, pady=5)
        self.algo_choice = ttk.Combobox(control_frame, values=list(self.algorithms.keys()), state="readonly")
        self.algo_choice.set("Choose Algorithm")
        self.algo_choice.grid(row=1, column=1)

        tk.Label(control_frame, text="Speed:", bg="#f7f7f7").grid(row=1, column=2)
        self.speed_scale = tk.Scale(control_frame, from_=0.005, to=1.0, length=200, resolution=0.005,
                                    orient=tk.HORIZONTAL, command=self.set_speed)
        self.speed_scale.set(0.05)
        self.speed_scale.grid(row=1, column=3)

        
        self.stats_label = tk.Label(self.root, text="", bg="#f7f7f7", font=("Arial", 10))
        self.stats_label.pack()

        self.canvas = tk.Canvas(self.root, width=1000, height=450, bg='white')
        self.canvas.pack(pady=10)

    def start_sorting(self):
        try:
            self.data = list(map(int, self.entry.get().strip().split()))
            algo = self.algo_choice.get()
            if algo not in self.algorithms:
                messagebox.showerror("Error", "Please choose a valid sorting algorithm.")
                return
            self.sorting = True
            self.paused = False
            self.swap_count = 0
            self.start_time = time.time()
            self.algorithms[algo]()
            elapsed = time.time() - self.start_time
            self.draw_data(['green'] * len(self.data))
            self.stats_label.config(text=f"Done! Time: {elapsed:.2f}s | Swaps: {self.swap_count}")
            self.sorting = False

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def wait_if_paused(self):
        while self.paused:
            time.sleep(0.1)

    def toggle_pause(self):e.sleep(0.1)
    def toggle_pause(self):
        if self.sorting:
            self.paused = not self.paused

    def reset(self):
        self.sorting = False
        self.paused = False
        self.data = []
        self.entry.delete(0, tk.END)
        self.canvas.delete("all")
        self.stats_label.config(text="")
        self.speed_scale.set(0.05)


        self.speed = float(val)

    def generate_random(self):
        self.data = random.sample(range(10, 100), 12)
        self.draw_data(['gray'] * len(self.data))
        self.entry.delete(0, tk.END)
        self.entry.insert(0, ' '.join(map(str, self.data)))

    def bubble_sort(self):
        for i in range(len(self.data)):
            for j in range(0, len(self.data) - i - 1):
                self.wait_if_paused()
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    self.swap_count += 1
                self.draw_data(['red' if x == j or x == j + 1 else 'gray' for x in range(len(self.data))])
                time.sleep(self.speed)

    def selection_sort(self):
        for i in range(len(self.data)):
            min_idx = i
            for j in range(i + 1, len(self.data)):
                self.wait_if_paused()
                if self.data[min_idx] > self.data[j]:
                    min_idx = j
                self.draw_data(['red' if x == j or x == min_idx else 'gray' for x in range(len(self.data))])
                time.sleep(self.speed)
            self.data[i], self.data[min_idx] = self.data[min_idx], self.data[i]
            self.swap_count += 1

    def insertion_sort(self):
        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i - 1
            while j >= 0 and self.data[j] > key:
                self.wait_if_paused()
                self.data[j + 1] = self.data[j]
                j -= 1
                self.draw_data(['red' if x == j + 1 or x == i else 'gray' for x in range(len(self.data))])
                time.sleep(self.speed)
                self.swap_count += 1
            self.data[j + 1] = key

    def merge_sort_wrapper(self):
        self.merge_sort(0, len(self.data) - 1)

    def merge_sort(self, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(left, mid)
            self.merge_sort(mid + 1, right)
            self.merge(left, mid, right)

    def merge(self, left, mid, right):
        L = self.data[left:mid + 1]
        R = self.data[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(L) and j < len(R):
            self.wait_if_paused()
            if L[i] <= R[j]:
                self.data[k] = L[i]
                i += 1
            else:
                self.data[k] = R[j]
                j += 1
            self.draw_data(['red' if x == k else 'gray' for x in range(len(self.data))])
            time.sleep(self.speed)
            self.swap_count += 1
            k += 1
        while i < len(L):
            self.data[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            self.data[k] = R[j]
            j += 1
            k += 1

    def quick_sort_wrapper(self):
        self.quick_sort(0, len(self.data) - 1)

    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)

    def partition(self, low, high):
        pivot = self.data[high]
        i = low - 1
        for j in range(low, high):
            self.wait_if_paused()
            if self.data[j] < pivot:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
                self.swap_count += 1
            self.draw_data(['red' if x == i or x == j else 'gray' for x in range(len(self.data))])
            time.sleep(self.speed)
        self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
        return i + 1

    def heap_sort(self):
        n = len(self.data)

        def heapify(n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            if l < n and self.data[l] > self.data[largest]:
                largest = l
            if r < n and self.data[r] > self.data[largest]:
                largest = r
            if largest != i:
                self.data[i], self.data[largest] = self.data[largest], self.data[i]
                self.swap_count += 1
                self.draw_data(['red' if x == i or x == largest else 'gray' for x in range(len(self.data))])
                time.sleep(self.speed)
                heapify(n, largest)

        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i)

        for i in range(n - 1, 0, -1):
            self.data[i], self.data[0] = self.data[0], self.data[i]
            self.swap_count += 1
            self.draw_data(['green' if x >= i else 'gray' for x in range(len(self.data))])
            time.sleep(self.speed)
            heapify(i, 0)

    def shell_sort(self):
        n = len(self.data)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = self.data[i]
                j = i
                while j >= gap and self.data[j - gap] > temp:
                    self.wait_if_paused()
                    self.data[j] = self.data[j - gap]
                    j -= gap
                    self.swap_count += 1
                    self.draw_data(['red' if x == j or x == i else 'gray' for x in range(len(self.data))])
                    time.sleep(self.speed)
                self.data[j] = temp
            gap //= 2

    def set_speed(self, val):
        self.speed = float(val)

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
