import pythreejs as p3
from IPython.display import display
import numpy as np

# Adjust the existing terrain and bot visualization using pythreejs
class Terrain:
    def _init_(self, width, height):
        # Initialize terrain with specified height rule: 2 if x = y, otherwise 1
        self.width = width
        self.height = height
        self.grid = [[{'height': 2 if i == j else 1, 'light': 0, 'path': 0} for i in range(width)] for j in range(height)]

    def _str_(self):
        return '\n'.join([' '.join([str(cell['height']) if cell['light'] else '0' for cell in row]) for row in self.grid])

class Bot:
    def _init_(self, terrain):
        self.x = 0  # Initial x-coordinate
        self.y = 0  # Initial y-coordinate
        self.direction = 'right'  # Initially facing right
        self.terrain = terrain
        self.stopped = False  # Track if the bot stopped due to height issues
        self.terrain.grid[self.y][self.x]['path'] = 1  # Mark initial position as part of the path

    def move_forward(self):
        if self.stopped: return  # Stop execution if the bot is halted

        current_height = self.terrain.grid[self.y][self.x]['height']
        target_x, target_y = self.x, self.y

        if self.direction == 'right' and self.x < self.terrain.width - 1:
            target_x += 1
        elif self.direction == 'left' and self.x > 0:
            target_x -= 1
        elif self.direction == 'up' and self.y > 0:
            target_y -= 1
        elif self.direction == 'down' and self.y < self.terrain.height - 1:
            target_y += 1

        target_height = self.terrain.grid[target_y][target_x]['height']
        if target_height == current_height:
            self.x, self.y = target_x, target_y
            self.terrain.grid[self.y][self.x]['path'] = 1  # Mark new position as part of the path
        else:
            print("Your robot stopped due to height differences.")
            self.stopped = True

    def jump(self):
        if self.stopped: return  # Stop execution if the bot is halted

        current_height = self.terrain.grid[self.y][self.x]['height']
        target_x, target_y = self.x, self.y

        if self.direction == 'right' and self.x < self.terrain.width - 1:
            target_x += 1
        elif self.direction == 'left' and self.x > 0:
            target_x -= 1
        elif self.direction == 'up' and self.y > 0:
            target_y -= 1
        elif self.direction == 'down' and self.y < self.terrain.height - 1:
            target_y += 1

        target_height = self.terrain.grid[target_y][target_x]['height']
        # Jump only if the height difference is exactly 1
        if abs(target_height - current_height) == 1:
            self.x, self.y = target_x, target_y
            self.terrain.grid[self.y][self.x]['path'] = 1  # Mark new position as part of the path
        else:
            print("Your robot stopped due to height differences.")
            self.stopped = True

    def turn_right(self):
        if self.stopped: return  # Stop if halted
        directions = ['up', 'right', 'down', 'left']
        self.direction = directions[(directions.index(self.direction) + 1) % 4]

    def turn_left(self):
        if self.stopped: return  # Stop if halted
        directions = ['up', 'right', 'down', 'left']
        self.direction = directions[(directions.index(self.direction) - 1) % 4]

    def switch_light(self):
        if self.stopped: return  # Stop if halted
        current_cell = self.terrain.grid[self.y][self.x]
        if current_cell['light'] == 0:  # Toggle light and increase height only if off
            current_cell['light'] = 1
            current_cell['height'] = 2  # Lit boxes get height 2 as per rules

    def execute_instructions(self, instructions):
        for instruction in instructions:
            if self.stopped: break
            if instruction == '^':
                self.move_forward()
            elif instruction == '*':
                self.jump()
            elif instruction == '>':
                self.turn_right()
            elif instruction == '<':
                self.turn_left()
            elif instruction == '@':
                self.switch_light()

            print(f"Bot Position: ({self.x}, {self.y}), Direction: {self.direction}, Light: {self.terrain.grid[self.y][self.x]['light']}, Height: {self.terrain.grid[self.y][self.x]['height']}")

# Initialize terrain and bot
terrain = Terrain(10, 10)
bot = Bot(terrain)

# Visualization setup using pythreejs
cubes = []
for x in range(terrain.width):
    for z in range(terrain.height):
        cell = terrain.grid[z][x]
        color = 'yellow' if cell['light'] else ('green' if cell['path'] else 'lightblue')
        cube = p3.Mesh(
            geometry=p3.BoxGeometry(width=1, height=cell['height'], depth=1),
            material=p3.MeshLambertMaterial(color=color),
            position=[x, cell['height'] / 2, z]
        )
        cubes.append(cube)

# Create the scene
scene = p3.Scene(children=cubes + [
    p3.AmbientLight(color='#777777'),
    p3.DirectionalLight(position=[3, 5, 1], intensity=0.5)
])

# Set up the camera
camera = p3.PerspectiveCamera(position=[10, 10, 10], up=[0, 1, 0], children=[
    p3.DirectionalLight(color='white', position=[0, 10, 10], intensity=0.5)
])

# Set up the renderer
renderer = p3.Renderer(camera=camera, scene=scene, controls=[p3.OrbitControls(controlling=camera)], width=800, height=600)



# Execute a sample instruction
instruction_string = "^*<@>"
bot.execute_instructions(instruction_string)

# Update visualization after executing instructions
cubes = []
for x in range(terrain.width):
    for z in range(terrain.height):
        cell = terrain.grid[z][x]
        color = 'yellow' if cell['light'] else ('green' if cell['path'] else 'lightblue')
        cube = p3.Mesh(
            geometry=p3.BoxGeometry(width=1, height=cell['height'], depth=1),
            material=p3.MeshLambertMaterial(color=color),
            position=[x, cell['height'] / 2, z]
        )
        cubes.append(cube)

# Update the scene with new positions
scene.children = cubes + [
    p3.AmbientLight(color='#777777'),
    p3.DirectionalLight(position=[3, 5, 1], intensity=0.5)
]

# Re-render
display(renderer)

def lightbot_kernel():
    print("Lightbot Kernel Initialized")
