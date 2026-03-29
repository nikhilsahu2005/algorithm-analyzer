import pygame
import random

pygame.init()

# ---------- WINDOW ----------
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualizer")

# ---------- COLORS ----------
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 80, 80)
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)

font = pygame.font.SysFont("Arial", 18)

# ---------- DATA ----------
def generate_data(n):
    return [random.randint(50, HEIGHT-100) for _ in range(n)]

arr = generate_data(50)

# ---------- DRAW BARS ----------
def draw_bars(arr, highlight=[]):
    screen.fill(BLACK)
    width = WIDTH // len(arr)

    for i in range(len(arr)):
        color = RED if i in highlight else GREEN
        pygame.draw.rect(screen, color,
                         (i*width, HEIGHT-arr[i], width-2, arr[i]))

# ---------- BUTTON ----------
class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 120, 40)

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        txt = font.render(self.text, True, WHITE)
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 10))

    def click(self, pos):
        return self.rect.collidepoint(pos)

# ---------- BUTTONS ----------
buttons = [
    Button("Bubble", 20, 540),
    Button("Selection", 160, 540),
    Button("Insertion", 300, 540),
    Button("Merge", 440, 540),
    Button("New Array", 580, 540)
]

# ---------- DRAW ALL ----------
def draw_all(arr, highlight=[]):
    draw_bars(arr, highlight)

    for b in buttons:
        b.draw()

    pygame.display.update()

# 🔵 SORTS (CLEAN + SIMPLE)

def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr)-i-1):
            draw_all(arr, [j, j+1])
            pygame.time.delay(20)

            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]


def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i

        for j in range(i+1, len(arr)):
            draw_all(arr, [min_idx, j])
            pygame.time.delay(20)

            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            draw_all(arr, [j])
            pygame.time.delay(20)

            arr[j+1] = arr[j]
            j -= 1

        arr[j+1] = key


# ---------- MERGE SORT ----------
def merge(arr, l, mid, r):
    temp = []
    i, j = l, mid+1

    while i <= mid and j <= r:
        draw_all(arr, [i, j])
        pygame.time.delay(20)

        if arr[i] < arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1

    while i <= mid:
        temp.append(arr[i])
        i += 1

    while j <= r:
        temp.append(arr[j])
        j += 1

    for k in range(len(temp)):
        arr[l+k] = temp[k]


def merge_sort(arr, l, r):
    if l >= r:
        return

    mid = (l + r) // 2
    merge_sort(arr, l, mid)
    merge_sort(arr, mid+1, r)
    merge(arr, l, mid, r)

# MAIN LOOP
running = True

while running:
    draw_all(arr)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if buttons[0].click(pos):
                bubble_sort(arr)

            elif buttons[1].click(pos):
                selection_sort(arr)

            elif buttons[2].click(pos):
                insertion_sort(arr)

            elif buttons[3].click(pos):
                merge_sort(arr, 0, len(arr)-1)

            elif buttons[4].click(pos):
                arr = generate_data(50)

pygame.quit()