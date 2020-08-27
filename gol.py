from PIL import Image
from argparse import ArgumentParser

#create parser to read command line arguments
parser = ArgumentParser(description = 'Import inial state')
parser.add_argument('input', type = str, help = 'Name of the input file')
parser.add_argument('--epochs', type = int, help = 'Number of epochs')
parser.add_argument('--output', type = str, help = 'Name of the output file')
args = parser.parse_args()

it = args.epochs #number of epochs
inputImg = Image.open(args.input)
grid = [] #array to store input image data
grid_1D = [] #array to flatten input image data for packing
data = list(inputImg.getdata())
count = 0 #counter to index through 'data'

for i in range(0, len(data)): #convert 255s to ones if necessary
    if data[i] != 0:
        data[i] = 1

for i in range(0,inputImg.size[0]): #append columns
    grid.append([])

for i in range(0,inputImg.size[0]): #append input image data to array
    for j in range(0,inputImg.size[1]):
        grid[i].append(data[count])
        count = count + 1

outputImg = Image.new('1',(len(grid),len(grid[1])),'white')

#neighbours to each cell
def north(grid, row, col):
    return grid[(row-1) % len(grid)][col]

def south(grid, row, col):
    return grid[(row+1) % len(grid)][col]

def east(grid, row, col):
    return grid[row][(col+1) % len(grid[row])]

def west(grid, row, col):
    return grid[row][(col-1) % len(grid[row])]

def north_east(grid, row, col):
    return grid[(row-1) % len(grid)][(col+1) % len(grid[row])]

def north_west(grid, row, col):
    return grid[(row-1) % len(grid)][(col-1) % len(grid[row])]

def south_east(grid, row, col):
    return grid[(row+1) % len(grid)][(col+1) % len(grid[row])]

def south_west(grid, row, col):
    return grid[(row+1) % len(grid)][(col-1) % len(grid[row])]

def neighbours(grid, row, col): #sum neighbours
    return (north(grid, row, col) + south(grid, row, col) +
            east(grid, row, col)+ west(grid, row, col) +
            north_east(grid, row, col) + north_west(grid, row, col) +
            south_east(grid, row, col) + south_west(grid, row, col))

def next_epoch(grid): #calculate next epoch
    grid_temp = [row.copy() for row in grid] #define temporary storage array

    for row in range(0,len(grid)):
        for col in range(0,len(grid[1])):

            if grid[row][col] == 1: #impose game rules
                if neighbours(grid, row, col) < 2 or neighbours(grid, row, col) > 3:
                    grid_temp[row][col] = 0
            elif grid[row][col] == 0:
                if neighbours(grid, row, col) == 3:
                    grid_temp[row][col] = 1
    return grid_temp

def iterate(grid,it): #calculate it epochs
    for n in range(0,it):
        grid = next_epoch(grid)
    return grid

def pack_grid(grid): #convert 2D grid array to 1D a array
    for i in range(0,len(grid)):
        for j in range(0,len(grid[1])):
            grid_1D.append(grid[i][j])
    return grid_1D

grid = iterate(grid, it)
grid_1D = pack_grid(grid)

outputImg.putdata(grid_1D)
outputImg.save(args.output)
