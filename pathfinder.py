"""A* Pathfinding Algorithm"""

import math
import pygame
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165 ,0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
YELLOW = (255, 255, 0)

class Spot:
	def __init__(self, row, col, width, totalRows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.totalRows = totalRows

	def isOpen(self):
		return self.color == GREEN

	def isClosed(self):
		return self.color == GREY

	def getPos(self):
		return self.row, self.col

	def isStart(self):
		return self.color == TURQUOISE

	def isEnd(self):
		return self.color == BLACK

	def isBarrier(self):
		return self.color == ORANGE

	def reset(self):
		self.color = RED

	def makeStart(self):
		self.color = TURQUOISE

	def makeClosed(self):
		self.color = GREY

	def makeOpen(self):
		self.color = GREEN

	def makeBarrier(self):
		self.color = ORANGE

	def makeEnd(self):
		self.color = BLACK

	def makePath(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def updateNeighbors(self, grid):
		self.neighbors = []
		if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isBarrier():
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].isBarrier():
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isBarrier():
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].isBarrier():
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def Jj(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstructPath(origin,current, draw):
	while current in origin:
		current = origin[current]
		current.makePath()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	openSet = PriorityQueue()
	openSet.put((0, count, start))
	origin = {}
	gScore = {spot: float("inf") for row in grid for spot in row}
	gScore[start] = 0
	fScore = {spot: float("inf") for row in grid for spot in row}
	fScore[start] = Jj(start.getPos(), end.getPos())

	openSetHash = {start}

	while not openSet.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = openSet.get()[2]
		openSetHash.remove(current)

		if current == end:
			reconstructPath(origin,end,draw)
			end.makeEnd()
			return True

		for neighbor in current.neighbors:
			tempGScore = gScore[current] + 1

			if tempGScore<gScore[neighbor]:
				origin[neighbor] = current
				gScore[neighbor] = tempGScore
				fScore[neighbor] = tempGScore + Jj(neighbor.getPos(), end.getPos())
				if neighbor not in openSetHash:
					count += 1
					openSet.put((fScore[neighbor], count, neighbor))
					openSetHash.add(neighbor)
					neighbor.makeOpen()

		draw()

		if current != start:
			current.makeClosed()

	return False


def makeGrid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def drawGrid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	drawGrid(win, rows, width)
	pygame.display.update()


def getClickedPos(pos, rows, width):
	gap = width // rows
	y, x = pos


	col = x // gap
	row = y // gap
	return row, col


def main(win, width):
	ROWS = 38
	grid = makeGrid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = getClickedPos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.makeStart()

				elif not end and spot != start:
					end = spot
					end.makeEnd()

				elif spot != end and spot != start:
					spot.makeBarrier()

			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = getClickedPos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.updateNeighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = makeGrid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)

