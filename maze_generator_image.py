import random
from PIL import Image
import sys
import astar
import os


# globals

WALL = '#'  # Wall char
WAY = ' '  # Open way char
WPX = (0, 0, 0)  # Wall Pixel
PPX = (255, 0, 0)  # Path Pixel


# functions

to2d: (tuple[int, int]) = lambda index: (
    index//(size[0]*2-1), index % (size[0]*2-1))
to1d: (int) = lambda x, y: (x) * (size[0]*2-1) + (y)


def new_maze(x, y):
    maze = []
    for _ in range(x*2-1):
        for _ in range(y*2-1):
            maze.append(WALL)

    return maze


def maze_to_image(maze, image: Image.Image, _x, _y, ii,) -> Image.Image:
    pixels = list(image.getdata())
    for y in range(_y*2-1):
        for x in range(_x*2-1):

            if maze[(y) * (_x*2-1) + (x)] == WALL:
                for i in range(ii):
                    pixels[(y*ii) * (s[0]) + (x*ii) + i:
                           ((y+1)*ii) * (s[0]) + (x*ii):
                           s[0]
                           ] = [WPX]*ii

    image.putdata(pixels)

    return image


def decision_tree(index, maze):
    maze[index] = WAY

    possible_dir = []

    y = index//(size[0]*2-1)
    x = index % (size[0]*2-1)

    if x > 1 and maze[(x-2)+(y)*(size[0]*2-1)] == WALL:
        possible_dir.append((-1, 0))

    if x < size[0]*2-3 and maze[(x+2)+(y)*(size[0]*2-1)] == WALL:
        possible_dir.append((1, 0))

    if y > 1 and maze[(x)+(y-2)*(size[0]*2-1)] == WALL:
        possible_dir.append((0, -1))

    if y < size[1]*2-3 and maze[(x)+(y+2)*(size[0]*2-1)] == WALL:
        possible_dir.append((0, 1))

    random.shuffle(possible_dir)

    def newindex1(x2, y2): return (y+y2) * (size[0]*2-1) + (x+x2)
    def newindex(x2, y2): return (y+2*y2) * (size[0]*2-1) + (x+2*x2)

    for _dir in possible_dir:
        i = newindex(*_dir)
        if maze[i] == WALL:
            maze[i] = WAY
            maze[newindex1(*_dir)] = WAY

        decision_tree(i, maze)


def save_maze(maze, x, y):
    '''Save the maze in a txt file'''
    with open('maze.txt', 'a') as f:
        f.write('...............\n')
        for i in range(x*2-1):
            f.write(' '.join([maze[j*(x*2-1)+i] for j in range(y*2-1)]))
            f.write('\n')


def tracepath(image: Image.Image, solution, _x, _y, ii) -> Image.Image:
    '''Create a new image with the maze and the solution path.'''
    path = [to1d(a, b) for a, b in solution]
    pixels = list(image.getdata())
    for y in range(_y*2-1):
        for x in range(_x*2-1):

            if (y) * (_x*2-1) + (x) in path:
                for i in range(ii):
                    pixels[(y*ii) * (s[0]) + (x*ii) + i:
                           ((y+1)*ii) * (s[0]) + (x*ii):
                           s[0]
                           ] = [PPX]*ii

            elif maze[(y) * (_x*2-1) + (x)] == WALL:
                for i in range(ii):
                    pixels[(y*ii) * (s[0]) + (x*ii) + i:
                           ((y+1)*ii) * (s[0]) + (x*ii):
                           s[0]
                           ] = [WPX]*ii

    image.putdata(pixels)

    return image


def unique(name: str, extension: str):
    files = os.listdir()
    i = 0
    while (f'{name}{i}.{extension}' in files):
        i += 1
    return f'{name}{i}.{extension}'


for current_image in sys.argv[1:]:  # allow imagenames as arguments

    print(f"Using image {current_image}")

    with Image.open(current_image) as im:
        s = im.size

        print('Creating the maze ... ', end='')

        for i in range(1, 100):
            size = s[0]//i, s[1]//i
            maze = new_maze(*size)
            maze[1] = WAY  # ENTRY
            maze[-2] = WAY  # SCAPE

            try:
                a = int(s[0] / (size[0]*2-1))
                decision_tree(index=(size[0]*2-1) *
                              (size[1]*2-3) + 1, maze=maze)
                print('Done')

            except Exception:
                continue

            try:
                print('Creating the image ... ', end='')
                im1 = maze_to_image(maze, im, *size, a)
                im1.crop((0, 0, a*(size[0]*2-1), a *
                         (size[1]*2-1))).save(unique('maze', 'jpg'))
                print('Done')

            except Exception as e:
                print(e)
                sys.exit()

            try:
                print('Finding the solution ... ', end='')
                maze2d = [[1 if e == WALL else 0 for e in maze[(
                    size[0]*2-1)*i:(size[0]*2-1)*(i+1)]]
                    for i in range(size[1]*2-1)]
                solution = astar.aStarSearch(maze2d, to2d(
                    1), to2d((size[0]*2-1)*(size[1]*2-1)-2))
                print('Done')

            except Exception as e:
                print(e)
                sys.exit()

            try:
                print('Creating the solved image ... ', end='')
                solvedim = tracepath(im, solution, *size, a)
                solvedim.crop(
                    (0, 0, a*(size[0]*2-1), a*(size[1]*2-1))
                ).save(unique('maze_solved', 'jpg'))
                print('Done')
                break

            except Exception as e:
                print(e)
                sys.exit()

        else:
            print('Failed')
