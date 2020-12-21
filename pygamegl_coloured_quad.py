from OpenGL.GL import *
import OpenGL.GL.shaders
import ctypes
import pygame
import numpy

vertex_shader = """
#version 410
in vec4 position;
in vec4 colour;
out vec4 newColour;

void main()
{
   gl_Position = position;
   newColour = colour;
}
"""

fragment_shader = """
#version 410
in vec4 newColour;
out vec4 outColour;

void main()
{
   //gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
   outColour = newColour;
}
"""

vertices = [-0.5, -0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0,
            0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0,
            0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
            -0.5, 0.5, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0]
vertices = numpy.array(vertices, dtype=numpy.float32)

indices = [0, 1, 2,
           0, 2, 3]
indices = numpy.array(indices, dtype=numpy.uint32)


def create_object():
    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    # Generate buffers to hold our vertices
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)

    # Generate buffers to hold buffer indices
    element_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer)

    # Get the position of the 'position' in parameter of our shader and bind it.
    position = glGetAttribLocation(shader, 'position')
    glEnableVertexAttribArray(position)

    # Describe the position data layout in the buffer
    glVertexAttribPointer(position, 4, GL_FLOAT, False, 32, ctypes.c_void_p(0))

    # Get the position of the 'colour' in parameter of our shader and bind it.
    colour = glGetAttribLocation(shader, 'colour')
    glEnableVertexAttribArray(colour)

    # Describe the position data layout in the buffer
    glVertexAttribPointer(colour, 4, GL_FLOAT, False, 32, ctypes.c_void_p(16))

    # Send the data over to the buffers
    glBufferData(GL_ARRAY_BUFFER, 128, vertices, GL_STATIC_DRAW)         # Vertices array
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 24, indices, GL_STATIC_DRAW)  # Indices array

    # Unbind the VAO first (Important)
    glBindVertexArray(0)

    # Unbind other stuff
    # glDisableVertexAttribArray(position)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    return shader, vertex_array_object


def display(shader, vertex_array_object):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader)

    glBindVertexArray(vertex_array_object)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)  # Replaces glDrawArrays because we're drawing indices now.
    glBindVertexArray(0)

    glUseProgram(0)


def main():
    pygame.init()

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    pygame.display.set_mode((512, 512), pygame.OPENGL | pygame.DOUBLEBUF)
    glClearColor(0.0, 0.0, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)

    

    shader, vertex_array_object = create_object()

    clock = pygame.time.Clock()

    while True:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                return

        display(shader, vertex_array_object)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())
        pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
