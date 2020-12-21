from OpenGL.GL import *
from pathlib import Path
import ctypes
import pygame
import numpy
import pyrr
from PIL import Image
from ShaderLoader import compile_shader


vertices = [
    -0.5, -0.5, 0.5, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # Front
    0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0,
    0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
    -0.5, 0.5, 0.5, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,

    0.5, -0.5, -0.5, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0,
    -0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0,  # Back
    -0.5, 0.5, -0.5, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
    0.5, 0.5, -0.5, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0,

    -0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # Left
    -0.5, -0.5, 0.5, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
    -0.5, 0.5, 0.5, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0,
    -0.5, 0.5, -0.5, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0,

    0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0,  # Right
    0.5, -0.5, -0.5, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
    0.5, 0.5, -0.5, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0,
    0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,

    -0.5, 0.5, 0.5, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0,  # Top
    0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0,
    0.5, 0.5, -0.5, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0,
    -0.5, 0.5, -0.5, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,

    -0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # Bottom
    0.5, -0.5, -0.5, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
    0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0,
    -0.5, -0.5, 0.5, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0
]
vertices = numpy.array(vertices, dtype=numpy.float32)
vertices_row_length = 10

indices = [0, 1, 2, 0, 2, 3,          # front
           4, 5, 6, 4, 6, 7,          # back         7b    6c
           16, 17, 18, 16, 18, 19,    # top       3m    2w
           12, 13, 14, 12, 14, 15,    # right
           20, 21, 22, 20, 22, 23,    # bottom       4k    5g
           8, 9, 10, 8, 10, 11        # left      0r    1y
           ]
indices = numpy.array(indices, dtype=numpy.uint32)


def init_gl():
    # glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.1, 1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    # glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glDepthFunc(GL_LEQUAL)


def create_object():
    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)

    shader = compile_shader(Path('shaders', 'perspective_vertex.glsl'),
                            Path('shaders', 'perspective_fragment.glsl'))

    # Generate buffers to hold our vertices
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)

    # Set the position of the 'position' in parameter of our shader and bind it.
    position = 0
    glBindAttribLocation(shader, position, 'position')
    glEnableVertexAttribArray(position)

    # Describe the position data layout in the buffer
    glVertexAttribPointer(position, 4, GL_FLOAT, False, vertices.itemsize * vertices_row_length, ctypes.c_void_p(0))

    # Send the data over to the buffers
    glBufferData(GL_ARRAY_BUFFER, vertices.itemsize * len(vertices), vertices, GL_STATIC_DRAW)       # Vertices array

    # Generate buffers to hold buffer indices
    element_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer)

    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)  # Indices array
    
    # Set the position of the 'colour' in parameter of our shader and bind it.
    colour = 1
    glBindAttribLocation(shader, colour, 'colour')
    glEnableVertexAttribArray(colour)
    # Describe the position data layout in the buffer
    glVertexAttribPointer(colour, 4, GL_FLOAT, False, vertices.itemsize * vertices_row_length, ctypes.c_void_p(16))

    # Generate buffers to hold our texture
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    
    
    # Set the position of the 'inTexCoords' in parameter of our shader and bind it.
    texture_coords = 2
    glBindAttribLocation(shader, texture_coords, 'inTexCoords')
    glEnableVertexAttribArray(texture_coords)
    # Describe the texture data layout in the buffer
    glVertexAttribPointer(texture_coords, 2, GL_FLOAT, False, vertices.itemsize * vertices_row_length,
                          ctypes.c_void_p(32))

    # Texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # Load and convert Texture
    image = Image.open(Path('res', 'crate.jpg'))
    img_data = image.convert('RGB').tobytes()

    
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    # Unbind the VAO first (Important)
    glBindVertexArray(0)

    # Unbind other stuff
    # glDisableVertexAttribArray(position)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    return shader, vertex_array_object


def display(shader, vertex_array_object, aspect_ratio):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(shader)
    rot_x = pyrr.matrix44.create_from_x_rotation(0.5 * pygame.time.get_ticks() / 1000, dtype=numpy.float32)
    rot_y = pyrr.matrix44.create_from_y_rotation(0.8 * pygame.time.get_ticks() / 1000, dtype=numpy.float32)
    transform_location = glGetUniformLocation(shader, 'transformation')
    glUniformMatrix4fv(transform_location, 1, GL_FALSE, rot_x @ rot_y)

    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -3.0]))
    projection = pyrr.matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)
    model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))

    view_loc = glGetUniformLocation(shader, 'view')
    proj_loc = glGetUniformLocation(shader, 'projection')
    modl_loc = glGetUniformLocation(shader, 'model')

    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(modl_loc, 1, GL_FALSE, model)

    glBindVertexArray(vertex_array_object)
    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)  # Replaces glDrawArrays because we're drawing indices now.
    glBindVertexArray(0)
    glUseProgram(0)

def window_resize(width, height):
    pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
    glViewport(0, 0, width, height)


def main():
    window_width = 512
    window_height = 512
    pygame.init()

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    window_resize(window_width, window_height)
    init_gl()

    
    shader, vertex_array_object = create_object()
    # glUseProgram(shader)

    clock = pygame.time.Clock()
    looping = True

    while looping:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            elif event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.size
                window_resize(window_width, window_height)
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                looping = False

        display(shader, vertex_array_object, window_width / window_height)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())
        pygame.display.flip()

    # glUseProgram(0)


if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
