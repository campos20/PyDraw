""" Created by:         Alexandre Campos
    Last modification:  01/22/2015
"""

import pygame

BLACK   =   0,   0,   0
WHITE   = 255, 255, 255
RED     = 255,   0,   0
GREEN   =   0, 255,   0
BLUE    =   0,   0, 255
LGRAY   = 220, 220, 220
GRAY    = 150, 150, 150

SIZE     = 1280, 720

def main():

    class Base():
        """Base to drawable objects."""
        def __init__(self):

            self.selected = False
            self.visible = True

    class Point(Base):
        """The points."""

        def __init__(self, color, pos, size):
            Base.__init__(self)
            self.color = color
            self.pos = pos
            self.size = size
            self.type = "Point"

            self.spec = "Point = (%s, %s)"%(self.pos[0]-left_bar_size, self.pos[1]-bar_size)

        def Render(self): #Draw the points
            if self.visible:
                if self.selected: # Mask if selected
                    pygame.draw.circle(screen, RED, self.pos, self.size+2)
                pygame.draw.circle(screen, self.color, self.pos, self.size)

        def Update(self):
            self.spec = "Point = (%s, %s)"%(self.pos[0]-left_bar_size, self.pos[1]-bar_size)

        def set_pos(self, pos): # Change the pos of point inside the workspace
            x, y = pos
            x = max(x, left_bar_size)
            x = min(x, SIZE[0])

            y = max(y, bar_size)
            y = min(y, SIZE[1])

            self.pos = [x, y]

    class Segment(Base):
        """The segments."""

        def __init__(self, start, end):
            Base.__init__(self)
            self.color = BLACK
            self.start = start
            self.end = end
            self.type = "Segment"

            self.spec = "Segment: %s"%Point_Distance(self.start.pos, self.end.pos)

        def Render(self):
            if self.visible:
                if self.selected: pygame.draw.line(screen, RED, self.start.pos, self.end.pos)
                else: pygame.draw.line(screen, self.color, self.start.pos, self.end.pos)

        def Update(self):
            self.spec = "Segment: %s"%Point_Distance(self.start.pos, self.end.pos)

    class Rectangle(Base):

        def __init__(self, p1, p2):
            Base.__init__(self)
            self.color = BLACK
            self.type = "Rectangle"
            self.width = abs(p1.pos[0]-p2.pos[0])
            self.height = abs(p1.pos[1]-p2.pos[1])
            self.p1 = p1
            self.p2 = p2

            self.spec = "Rectangle: %s x %s"%(self.width, self.height)

            self.start = ( min(p1.pos[0], p2.pos[0]), min(p1.pos[1], p2.pos[1]) ) # Takes the lower left corner as start

        def Render(self):
            if self.visible:
                if self.selected: pygame.draw.rect(screen, RED, [self.start[0], self.start[1], self.width, self.height], 2)
                else: pygame.draw.rect(screen, self.color, [self.start[0], self.start[1], self.width, self.height], 2)

        def Update(self):
            self.spec = "Rectangle: %s x %s"%(self.width, self.height)
            self.width = abs(self.p1.pos[0]-self.p2.pos[0])
            self.height = abs(self.p1.pos[1]-self.p2.pos[1])

            self.start = ( min(self.p1.pos[0], self.p2.pos[0]), min(self.p1.pos[1], self.p2.pos[1]) )

    class Circle(Base):

        def __init__(self, p1, p2):
            Base.__init__(self)
            self.color = BLACK
            self.type = "Circle"
            self.p1 = p1
            self.p2 = p2
            self.radius = Point_Distance(p1.pos, p2.pos)
            self.border = 2

            self.spec = "Circle: %s"%self.radius

        def Render(self):
            if self.visible:
                if self.selected: pygame.draw.circle(screen, RED, self.p1.pos, self.radius, min(self.border, self.radius))
                else: pygame.draw.circle(screen, self.color, self.p1.pos, self.radius, min(self.border, self.radius))

        def Update(self):
            self.radius = Point_Distance(self.p1.pos, self.p2.pos)
            self.spec = "Circle: %s"%self.radius

    class Polygon(Base):
        """The polygons."""

        def __init__(self, point_list):
            Base.__init__(self)
            self.point_list = point_list
            self.type = "Polygon"
            self.color = BLACK
            self.point_list
            self.width = 2

            self.spec = "Polygon: %s sides"%(len(point_list))

        def Render(self):
            if self.visible:
                if self.selected: pygame.draw.polygon(screen, RED, [x.pos for x in self.point_list], self.width )
                else: pygame.draw.polygon(screen, self.color, [x.pos for x in self.point_list], self.width )

        def Update(self): pass

    class Tool:
        """The tools."""

        def __init__(self, name, pos):
            self.name = name
            self.selected = False
            self.pos = pos
            self.type = "Tool"

        def Render(self):

            # Different color if the tool is selected
            if self.selected: self.color = LGRAY
            else: self.color = WHITE

            pygame.draw.rect(screen, self.color, [self.pos[0], self.pos[1], tool_size, bar_size])
            pygame.draw.rect(screen, BLACK, [self.pos[0], self.pos[1], tool_size, bar_size], 1) # Mask

            tool_label = tool_font.render(self.name, True, BLACK) # Label
            offset = (tool_size-tool_label.get_width())/2
            screen.blit(tool_label, [self.pos[0]+offset, 0])

    class Roll:
        """Offset for the scrolling in the left bar."""
        def __init__(self): self.roll = 0

        def update(self, offset = 0):
            self.roll += offset
            self.roll = min((len(RenderList)+1)*label_height-( SIZE[1]-bar_size), self.roll) # Don't scroll to much
            self.roll = max(0, self.roll) # Makes sure to limit the mouse scroll up

    def Point_Distance(A, B):
        """Euclidian distance between A and B."""
        return int( pow( pow(B[0]-A[0], 2) + pow(B[1]-A[1],2), 0.5 ) )

    def pick_tool(n = 0):
        """Select the tool number n."""
        for item in tools: item.selected = False # Resets all the tools
        tools[n].selected = True # Sets this tool to true

    def selection(item):
        """Selects object when mouse clicked."""
        if item.selected:
            item.selected = False
            selected_items.remove(item)
        else:
            item.selected = True
            selected_items.append(item)

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("PyDraw")

    done = False

    delay = 10
    border = 2 # The borders. Wherever this appears, is to let objects a little away of the limit line.
    label_height = 20 # The size of the label on the left bar
    RenderList = [] # List of objects
    selected_items = []

    tool_list = "Selector", "Point", "Segment", "Polygon", "Rectangle", "Circle"
    n_tool = len(tool_list)
    tool_size = SIZE[0]/2/n_tool
    bar_size = SIZE[1]/10
    left_bar_size = SIZE[0]/8
    selected_tool = 0 # First tool selected
    tool_help = (    "Click and drag objects. Press enter to deselect all.",
            "Click to create points",
            "Click two points",
            "Select the points then press enter.", "Click the points of diagonal.",
            "Select the center and other point.", "Type in.")

    # Mouse
    MousePressed = False # Pressed down THIS FRAME
    MouseDown = False # Mouse is held down
    MouseReleased = False # Released THIS FRAME
    clicks_mouse_selected = 0 # Count frames of mouse pressed. This helps in dragging around
    Target = None # Target of Drag/Drop
    roll = Roll()
    pygame.init()

    tool_font = pygame.font.SysFont('Arial', 20, True) # Label of everything
    help_font = pygame.font.SysFont('Arial', 12) # The help
    label_font = pygame.font.SysFont('Arial', 15) # Objects specification

    # Start the tools
    tools = []
    for i in xrange(n_tool):
        tools.append( Tool( tool_list[i], [i*tool_size, 0] ) )

    tools[selected_tool].selected = True # Selects the first tool

    while not done:

        screen.fill(WHITE) # clear screen

        mouse_pos = pygame.mouse.get_pos() # Get mouse

        for Event in pygame.event.get():

            print Event

            if Event.type == pygame.QUIT: # Close program
                done = True
                break

            elif Event.type == pygame.MOUSEBUTTONDOWN: # Mouse pressed

                if Event.button == 1: # Left mouse
                    MousePressed = True
                    MouseDown = True

            elif Event.type == pygame.MOUSEBUTTONUP: # Mouse released

                if Event.button == 1: # Left mouse
                    MouseReleased = True
                    MouseDown = False

                elif Event.button == 4: # Mouse wheel up
                    if mouse_pos[0] < left_bar_size and mouse_pos[1] > bar_size: # Scroll left bar
                        roll.update(-20)

                elif Event.button == 5: # Mouse wheel down
                    if mouse_pos[0] < left_bar_size and mouse_pos[1] > bar_size:
                        roll.update(20)

            elif Event.type == pygame.KEYDOWN: # Button pressed

                if Event.key == pygame.K_ESCAPE: # Resets tool if esc is pressed
                    selected_tool = 0
                    pick_tool(0)

                elif Event.key == pygame.K_DELETE: # Delete selected objects
                    for item in selected_items: RenderList.remove(item)
                    selected_items = []

                    roll.update() # Updates scrolling. This avoid problem after deleting.

                elif Event.key == pygame.K_h: # Change the visibility of items if h is pressed
                    for item in selected_items: item.visible = not item.visible

                elif Event.key == pygame.K_RETURN:

                    if selected_tool == 3: # Draw polygon if enter is pressed

                        n = len(selected_items)

                        if n > 2 and set(x.type for x in selected_items)==set("Point"): RenderList.append( Polygon( selected_items ) ) # More than two points

                    for item in selected_items: item.selected = False
                    selected_items = []

                elif Event.key == pygame.K_PAGEUP: # Move object up

                    for item in RenderList:
                        if item.selected:
                            i = RenderList.index(item)

                            RenderList[(i-1)%len(RenderList)], RenderList[i] = RenderList[i], RenderList[(i-1)%len(RenderList)]

                elif Event.key == pygame.K_PAGEDOWN: # Move object down

                    for item in RenderList[::-1]:
                        if item.selected:
                            i = RenderList.index(item)

                            RenderList[(i+1)%len(RenderList)], RenderList[i] = RenderList[i], RenderList[(i+1)%len(RenderList)]

        if MousePressed == True:

            if mouse_pos[1] < bar_size and mouse_pos[0] < SIZE[0]/2: # Mouse over the tools

                selected_tool = mouse_pos[0]/tool_size
                pick_tool(selected_tool) # Select tool based on user's choice

            elif mouse_pos[0] < left_bar_size: # Mouse over the left bar

                y = (mouse_pos[1]-bar_size+roll.roll-border)/label_height # Takes the element considering scrolling

                if 0 <= y < len(RenderList): # Selection on the left bar
                    item = RenderList[y]

                    if item in selected_items:
                        item.selected = False
                        selected_items.remove(item)

                    else:
                        item.selected = True
                        selected_items.append(item)

            else:

                for item in RenderList: # search all items

                    if item.type == "Point" and abs(item.pos[0]-mouse_pos[0]) <= item.size and abs(item.pos[1]-mouse_pos[1]) <= item.size:
                        Target = item # "pick up" item
            
                if Target is None: # didn't find any?

                    if selected_tool == 1:
                        Target = Point( (0, 0, 255), mouse_pos, 10) # create a new one
                        RenderList.append(Target) # add to list of things to draw
            
        if MouseDown and Target is not None: # if we are dragging something

            if selected_tool == 0 and clicks_mouse_selected > delay: # The mouse clicked part makes sure that the user isn't selecting
                Target.set_pos(mouse_pos) # move the target with us if the tool is the selector

            clicks_mouse_selected += 1
        
        if MouseReleased:

            if selected_tool == 0 and Target is not None and clicks_mouse_selected <= delay and Target.visible: # Simple selection

                selection(Target)

            elif selected_tool == 2 and Target is not None and clicks_mouse_selected <= delay: # Draw segment

                selection(Target)

                if len(selected_items) == 2: # Two points selected and the segment tool

                    # Draws the segment
                    RenderList.append( Segment( selected_items[0], selected_items[1] ) )

                    # Unselect items
                    for item in selected_items: item.selected = False
                    selected_items = []

            elif selected_tool == 4 and Target is not None and clicks_mouse_selected <= delay: # Draw rectangle

                selection(Target)

                if len(selected_items) == 2: # Two points selected and the rectangle tool

                    # Draws the segment
                    RenderList.append( Rectangle( selected_items[0], selected_items[1] ) )

                    # Unselect items
                    for item in selected_items: item.selected = False
                    selected_items = []

            elif selected_tool == 5 and Target is not None and clicks_mouse_selected <= delay: # Draw circle

                selection(Target)

                if len(selected_items) == 2: # Two points selected and the segment tool

                    # Draws the segment
                    RenderList.append( Circle( selected_items[0], selected_items[1] ) )

                    # Unselect items
                    for item in selected_items: item.selected = False
                    selected_items = []

            elif selected_tool == 3 and Target is not None and clicks_mouse_selected < delay: # Polygon tool selection

                selection(Target)

            clicks_mouse_selected = 0 # Resets clicks mouse selected

            Target = None # Drop item, if any
            
        for item in RenderList:
            item.Update()
            item.Render() # Draw all items
            
        MousePressed = False # Reset these to False
        MouseReleased = False

        # Draw left bar
        pygame.draw.rect(screen, LGRAY, [0, bar_size, left_bar_size, 720-bar_size], 0)
        pygame.draw.rect(screen, BLACK, [0, bar_size, left_bar_size, 720-bar_size], 2) # Mask

        # Put the objects in the left bar
        for i in xrange(len(RenderList)):

            x = border
            y = border+bar_size+i*label_height-roll.roll

            if RenderList[i].visible: this_color = BLACK
            else: this_color = GRAY

            obj_text = label_font.render("%s"%RenderList[i].spec, True, this_color)

            if RenderList[i].selected: pygame.draw.rect(screen, RED, [x, y, left_bar_size-border, label_height], border)

            screen.blit(obj_text, [x, y])

        # Render help.
        pygame.draw.rect(screen, WHITE, [0, 0, SIZE[0], bar_size], 0) # Rectangle containing tools and help
        pygame.draw.rect(screen, BLACK, [0, 0, SIZE[0], bar_size], 2) # Rectangle containing tools and help

        help_text = help_font.render(tool_help[selected_tool], True, BLACK)
        screen.blit(help_text, [SIZE[0]/2, border])

        # Draw the tools
        for item in tools: item.Render()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__": main()
