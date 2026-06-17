import pygame as pg

pg.init()

# ======================
# Window Setup
# ======================

WIDTH, HEIGHT = 1000, 700

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Sorting Visualizer")

clock = pg.time.Clock()

font = pg.font.Font(None, 50)
small_font = pg.font.Font(None, 35)

GOLD = (212, 175, 55)
BLACK = (0, 0, 0)



# ======================
# Sorting Algorithms
# (Unchanged)
# ======================

def bubble_sort(arr):

    n = len(arr)

    for i in range(n):

        swapped = False

        for j in range(n-i-1):

            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True

            yield arr.copy()

        if not swapped:
            return


def insertion_sort(arr):

    for i in range(1, len(arr)):

        key = arr[i]
        j = i - 1

        while j >= 0 and key < arr[j]:

            arr[j+1] = arr[j]
            j -= 1

            yield arr.copy()

        arr[j+1] = key

        yield arr.copy()


def merge_sort(arr):

    yield from merge_helper(
        arr,
        0,
        len(arr)-1
    )


def merge_helper(arr,left,right):

    if left >= right:
        return

    mid = (left+right)//2

    yield from merge_helper(arr, left, mid)
    yield from merge_helper(arr, mid+1, right)
    yield from merge(arr, left, mid, right)


def merge(arr,left,mid,right):

    L = arr[left:mid+1]
    R = arr[mid+1:right+1]

    i = j = 0
    k = left

    while i < len(L) and j < len(R):

        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1

        k += 1
        yield arr.copy()

    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1
        yield arr.copy()

    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1
        yield arr.copy()


# ======================
# Screen Functions
# ======================

def draw_input():

    screen.fill(GOLD)

    screen.blit(
        font.render("Sorting Visualizer", True, BLACK),
        (280, 50)
    )

    screen.blit(
        small_font.render(f"Numbers: {input_text}", True, BLACK),
        (50, 180)
    )

    screen.blit(
        small_font.render("Separate values with commas", True, BLACK),
        (50, 250)
    )

    screen.blit(
        small_font.render("Press ENTER when finished", True, BLACK),
        (50, 320)
    )

    pg.display.update()


def draw_algorithm():

    screen.fill(GOLD)

    screen.blit(
        font.render("Choose Algorithm", True, BLACK),
        (300, 60)
    )

    options = [
        "1) Bubble Sort",
        "2) Insertion Sort",
        "3) Merge Sort"
    ]

    y = 180
    for option in options:
        screen.blit(
            small_font.render(option, True, BLACK),
            (100, y)
        )
        y += 70

    pg.display.update()


def draw_visualizer():

    screen.fill(GOLD)

    screen.blit(
        font.render(algorithm, True, BLACK),
        (WIDTH // 2 - 120, 40)
    )

    if not values:
        pg.display.update()
        return

    max_value = max(abs(v) for v in values)

    total_width = WIDTH - 100
    bar_width = max(5, total_width // len(values))

    start_x = 50
    midline = HEIGHT - 250

    # axis line
    pg.draw.line(screen, BLACK, (50, midline), (WIDTH - 50, midline), 2)

    for i, value in enumerate(values):

        scaled = int((value / max_value) * 150)

        x = start_x + i * bar_width

        # bar positioning
        if value >= 0:
            y = midline - scaled
            height = scaled
            label_y = y - 18   # ABOVE bar
        else:
            y = midline
            height = abs(scaled)
            label_y = y + height + 18  # BELOW bar

        pg.draw.rect(
            screen,
            BLACK,
            (x, y, max(2, bar_width - 5), height)
        )

        # dynamic label positioning fix
        label = small_font.render(str(value), True, BLACK)
        label_rect = label.get_rect(center=(x + bar_width // 2, label_y))
        screen.blit(label, label_rect)

    # full array display
    screen.blit(
        small_font.render(str(values), True, BLACK),
        (WIDTH // 2 - 200, HEIGHT - 60)
    )

    if finished:
        screen.blit(
            font.render("DONE", True, BLACK),
            (WIDTH // 2 - 60, 120)
        )

    screen.blit(
        small_font.render("Press ESC to Return", True, BLACK),
        (30, 30)
    )

    pg.display.update()


# ======================
# Variables
# ======================

mode = "input"
input_text = ""
values = []

algorithm = ""
sorting = False
finished = False
sort_gen = None

animation_speed = 3


# ======================
# Main Loop
# ======================

running = True

while running:

    clock.tick(animation_speed)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:

            if mode == "input":

                if event.key == pg.K_BACKSPACE:
                    input_text = input_text[:-1]

                elif event.key == pg.K_RETURN:

                    try:
                        values = [
                            int(x.strip())
                            for x in input_text.split(",")
                            if x.strip()
                        ]
                        if values:
                            mode = "algorithm"
                    except ValueError:
                        pass

                else:
                    if event.unicode in "0123456789,- ":
                        input_text += event.unicode


            elif mode == "algorithm":

                arr = values.copy()

                if event.key == pg.K_1:
                    algorithm = "Bubble Sort"
                    sort_gen = bubble_sort(arr)
                    sorting = True
                    finished = False
                    mode = "visual"

                elif event.key == pg.K_2:
                    algorithm = "Insertion Sort"
                    sort_gen = insertion_sort(arr)
                    sorting = True
                    finished = False
                    mode = "visual"

                elif event.key == pg.K_3:
                    algorithm = "Merge Sort"
                    sort_gen = merge_sort(arr)
                    sorting = True
                    finished = False
                    mode = "visual"


            elif mode == "visual":

                if event.key == pg.K_ESCAPE:
                    mode = "input"
                    input_text = ""
                    values = []
                    sorting = False
                    finished = False
                    algorithm = ""

    if mode == "visual":

        if sorting:
            try:
                values = next(sort_gen)
            except StopIteration:
                sorting = False
                finished = True
                values = sorted(values)

        draw_visualizer()

    elif mode == "algorithm":
        draw_algorithm()

    else:
        draw_input()

pg.quit()