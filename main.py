import pygame
import random

pygame.init()

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualizer FINAL")

# ---------------- COLORS ----------------
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

font = pygame.font.SysFont("Arial", 20)

# ---------------- SETTINGS ----------------
speed = 20
size = 50
input_text = str(size)
active_input = False

# ---------------- DATA ----------------
def generate_data(n):
    return [random.randint(10, HEIGHT - 120) for _ in range(n)]

arr = generate_data(size)

# ---------------- DRAW BARS ----------------
def draw_bars(arr, highlight=[]):
    screen.fill(BLACK)

    n = len(arr)
    bar_width = max(2, WIDTH // n)
    gap = 1

    for i in range(n):
        x = i * bar_width
        y = HEIGHT - arr[i]

        color = GREEN
        if i in highlight:
            color = RED

        pygame.draw.rect(screen, color, (x, y, bar_width - gap, arr[i]))

# ---------------- BUTTON ----------------
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        txt = font.render(self.text, True, WHITE)
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 5))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ---------------- INPUT BOX ----------------
input_box = pygame.Rect(800, 20, 150, 30)

def draw_input():
    pygame.draw.rect(screen, WHITE, input_box, 2)
    txt = font.render(input_text, True, WHITE)
    screen.blit(txt, (input_box.x + 5, input_box.y + 5))

# ---------------- SORTS ----------------
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr)-i-1):
            draw_all(arr, [j, j+1])
            pygame.time.delay(speed)

            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            draw_all(arr, [min_idx, j])
            pygame.time.delay(speed)

            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            draw_all(arr, [j, j+1])
            pygame.time.delay(speed)

            arr[j+1] = arr[j]
            j -= 1

        arr[j+1] = key

# -------- MERGE SORT --------
def merge(arr, l, m, r):
    left = arr[l:m+1]
    right = arr[m+1:r+1]

    i = j = 0
    k = l

    while i < len(left) and j < len(right):
        draw_all(arr, [k])
        pygame.time.delay(speed)

        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

def merge_sort(arr, l, r):
    if l < r:
        m = (l + r) // 2
        merge_sort(arr, l, m)
        merge_sort(arr, m+1, r)
        merge(arr, l, m, r)

# -------- QUICK SORT --------
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        draw_all(arr, [j, high])
        pygame.time.delay(speed)

        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi-1)
        quick_sort(arr, pi+1, high)

# ---------------- UI ----------------
buttons = [
    Button("Bubble", 20, 520, 100, 40),
    Button("Selection", 130, 520, 110, 40),
    Button("Insertion", 250, 520, 110, 40),
    Button("Merge", 370, 520, 100, 40),
    Button("Quick", 480, 520, 100, 40),
    Button("New Array", 600, 520, 140, 40),
]

def draw_all(arr, highlight=[]):
    draw_bars(arr, highlight)
    for b in buttons:
        b.draw()
    draw_input()
    pygame.display.update()

# ---------------- MAIN ----------------
running = True

while running:
    draw_all(arr)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Input click
            if input_box.collidepoint(pos):
                active_input = True
                input_text = ""
            else:
                active_input = False

            # Buttons
            if buttons[0].is_clicked(pos):
                bubble_sort(arr)

            elif buttons[1].is_clicked(pos):
                selection_sort(arr)

            elif buttons[2].is_clicked(pos):
                insertion_sort(arr)

            elif buttons[3].is_clicked(pos):
                merge_sort(arr, 0, len(arr)-1)

            elif buttons[4].is_clicked(pos):
                quick_sort(arr, 0, len(arr)-1)

            elif buttons[5].is_clicked(pos):
                if input_text != "":
                    size = max(5, int(input_text))
                    arr = generate_data(size)

        # Typing
        if event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.unicode.isdigit():
                input_text += event.unicode

pygame.quit()