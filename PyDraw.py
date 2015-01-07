import pygame

BLACK	=   0,   0,   0
WHITE	= 255, 255, 255
GRAY	= 200, 200, 200
RED	= 255,   0,   0
GREEN	=   0, 255,   0
BLUE	=   0,   0, 255

SIZE	= 1280, 720

def main():

	class Point:
		"""The points."""

		def __init__(self, color, pos, size):
			self.color = color
			self.pos = pos
			self.size = size
			self.selected = False
			self.type = "Point"
			self.visible = True
		
		def Render(self): #Draw the points

			if self.visible:

				if self.selected: # Mask if selected
					pygame.draw.circle(screen, RED, self.pos, self.size+2)

				pygame.draw.circle(screen, self.color, self.pos, self.size)

		def set_pos(self, pos): # Change the pos of point inside the limit rectangle
			x, y = pos

			x = max(x, left_bar_size)
			x = min(x, SIZE[0])

			y = max(y, bar_size)
			y = min(y, SIZE[1])

			self.pos = x, y

	class Segment:
		"""The segments."""

		def __init__(self, start, end):
			self.color = BLACK
			self.start = start
			self.end = end
			self.type = "Segment"
			self.visible = "True"

		def Render(self):
			if self.visible: pygame.draw.line(screen, self.color, self.start.pos, self.end.pos)

	class Polygon:
		"""The polygons."""

		def __init__(self, point_list):
			self.point_list = point_list
			self.type = "Polygon"
			self.visible = "True"
			self.color = BLACK
			self.point_list
			self.width = 2

		def Render(self):
			if self.visible: pygame.draw.polygon(screen, self.color, [x.pos for x in self.point_list], self.width )

	class Tool:
		"""The tools."""

		def __init__(self, name, pos):
			self.name = name
			self.selected = False
			self.pos = pos
			self.type = "Tool"

		def Render(self):

			# Different color if the tool is selected
			if self.selected: self.color = GRAY
			else: self.color = WHITE

			pygame.draw.rect(screen, self.color, [self.pos[0], self.pos[1], tool_size, bar_size])
			pygame.draw.rect(screen, BLACK, [self.pos[0], self.pos[1], tool_size, bar_size], 1) # Mask

			tool_label = tool_font.render(self.name, True, BLACK) # Label
			offset = (tool_size-tool_label.get_width())/2
			screen.blit(tool_label, [self.pos[0]+offset, 0])

	pygame.display.set_caption("PyDraw")
	screen = pygame.display.set_mode(SIZE)

	done = False

	RenderList = [] # List of objects

	MousePressed = False # Pressed down THIS FRAME
	MouseDown = False # Mouse is held down
	MouseReleased = False # Released THIS FRAME
	Target = None # Target of Drag/Drop

	tool_list = "Selector", "Point", "Segment", "Polygon"
	n_tool = len(tool_list)
	tool_size = SIZE[0]/2/n_tool
	bar_size = SIZE[1]/10
	left_bar_size = SIZE[0]/8
	selected_tool = 0 # First tool selected
	tool_help = (	"Click and drag objects.",
			"Click to create points",
			"Click two points",
			"Selected the points then press enter.")

	selected_items = []
	clicks_mouse_selected = 0 # Count frames of mouse pressed. This helps in dragging around

	pygame.init()

	tool_font = pygame.font.SysFont('Arial', 20, True) #Label of everything
	help_font = pygame.font.SysFont('Arial', 12)

	# Start the tools
	tools = []
	for i in xrange(n_tool):
		tools.append( Tool( tool_list[i], [i*tool_size, 0] ) )

	tools[selected_tool].selected = True # Selects the first tool

	while not done:

		screen.fill(WHITE) # clear screen

		pos = pygame.mouse.get_pos() # Get mouse

		for Event in pygame.event.get():

			if Event.type == pygame.QUIT: # Close program
				done = True
				break

			elif Event.type == pygame.MOUSEBUTTONDOWN:

				if Event.button == 1: # Left mouse
					MousePressed = True
					MouseDown = True 

			elif Event.type == pygame.MOUSEBUTTONUP:

				if Event.button == 1: # Left mouse
					MouseReleased = True
					MouseDown = False

			elif Event.type == pygame.KEYDOWN:

				if Event.key == pygame.K_DELETE: # Delete selected objects
					pass

				elif Event.key == pygame.K_h: # Change the visibility of items if h is pressed
					for item in selected_items:
						item.visible = not item.visible

				elif Event.key == pygame.K_RETURN:

					if selected_tool == 3: # Draw polygon if enter is pressed

						n = len(selected_items)

						if n > 2: RenderList.append( Polygon( selected_items ) )

					for item in selected_items: item.selected = False
					selected_items = []

		if MousePressed == True:

			if pos[1] < bar_size and pos[0] < SIZE[0]/2: # Mouse over the tools

				selected_tool = pos[0]/tool_size

				for item in tools: item.selected = False # Resets all the tools
				tools[selected_tool].selected = True # Sets this tool to true

			else:

				for item in RenderList: # search all items

					if item.type == "Point" and abs(item.pos[0]-pos[0]) <= item.size and abs(item.pos[1]-pos[1]) <= item.size:
						Target = item # "pick up" item
			
				if Target is None: # didn't find any?

					if selected_tool == 1:
						Target = Point( (0, 0, 255), pos, 10) # create a new one
						RenderList.append(Target) # add to list of things to draw
			
		if MouseDown and Target is not None: # if we are dragging something

			if selected_tool == 0:
				Target.set_pos(pos) # move the target with us if the tool is the selector

			clicks_mouse_selected += 1
		
		if MouseReleased:

			if selected_tool == 0 and Target is not None and clicks_mouse_selected < 10:

				if Target.selected:
					Target.selected = False
					selected_items.remove(Target)
				else:
					Target.selected = True
					selected_items.append(Target)

			elif selected_tool == 2 and Target is not None and clicks_mouse_selected < 10:

				if Target.selected:
					Target.selected = False
					selected_items.remove(Target)
				else:
					Target.selected = True
					selected_items.append(Target)

				if len(selected_items) == 2:

					# Draws the segment
					RenderList.append( Segment( selected_items[0], selected_items[1] ) )

					# Unselect items
					for item in selected_items: item.selected = False
					selected_items = []

			elif selected_tool == 3 and Target is not None and clicks_mouse_selected < 10:

				if Target.selected:
					Target.selected = False
					selected_items.remove(Target)
				else:
					Target.selected = True
					selected_items.append(Target)

			clicks_mouse_selected = 0 # Resets clicks mouse selected

			Target = None # Drop item, if any
			
		for item in RenderList: item.Render() # Draw all items
			
		MousePressed = False # Reset these to False
		MouseReleased = False

		pygame.draw.rect(screen, BLACK, [0, 0, SIZE[0], bar_size], 2) # Rectangle containing tools and help

		# Draw the tools
		for item in tools: item.Render()

		# Draw left bar
		pygame.draw.rect(screen, GRAY, [0, bar_size, left_bar_size, 720-bar_size], 0)
		pygame.draw.rect(screen, BLACK, [0, bar_size, left_bar_size, 720-bar_size], 2) # Mask

		# Render help.
		pygame.draw.rect(screen, WHITE, [SIZE[0]/2, 0, SIZE[0]/2, bar_size], 0)
		help_text = help_font.render(tool_help[selected_tool], True, BLACK)
		screen.blit(help_text, [SIZE[0]/2, 0])

		pygame.display.flip()
		pygame.time.Clock().tick(60)

	pygame.quit()
