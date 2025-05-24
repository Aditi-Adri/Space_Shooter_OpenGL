from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

colors = []
point = []
speed = 0 
left_mouse = False
prev = None
spacebar = False
time = 0 


def draw_box () :
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(500,800)
    glVertex2f(0,800)
    glVertex2f(0,800)
    glVertex2f(0, 0)
    glVertex2f(500,0)
    glVertex2f(0,0)
    glVertex2f(500, 0)
    glVertex2f(800, 500)
    glEnd()


def iterate():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 800, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 1.0)
    draw_box()
    draw_point()
    glutSwapBuffers()


def create_point(x, y):
    global colors
    global point
    if 0 < x < 500 and 0 < y < 800:
        red, green, blue = (random.random(), random.random(), random.random())
        color = (red, green, blue)
        update_x = random.choice([-1, 1])
        update_y = random.choice([-1, 1])
        point.append((x, y, color, update_x, update_y))
        colors.append(color)


def arrow_key(key, x, y):
    global speed
    if key == GLUT_KEY_UP :
        speed += 6
        print("Speed Increased")
    elif key == GLUT_KEY_DOWN:
        if speed <= 0 :
            speed = 0
            print("Max speed limit crossed")
        else:
            speed -= 6
            print("Speed Decreased")


def click_mouse(button, state, x, y):
    global left_mouse, spacebar
    if spacebar:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        create_point(x,800 - y)
        print("New point added")
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if left_mouse == False:
            left_mouse = not left_mouse
            print("Blinking On")
        else:
            left_mouse = not left_mouse
            print("Blinking Off")


def click_keyboard (key, x,y):
    global spacebar, left_mouse , prev ,point
    if key == b" ":
        spacebar = not spacebar
        if spacebar :
            prev = left_mouse
            left_mouse = False
            for i in range(len(point)):
                x, y, color, x1 , y1  = point[i]
                x1 = 0
                y1 = 0
                point[i] = ( x, y, color, x1 , y1 )
            print("Points freeze")
        
        else:
            left_mouse = prev
            prev = None
            for i in range(len(point)):
                x1 = random.choice([-1, 1])
                y1 = random.choice([-1, 1])
                point[i] = (point[i][0], point[i][1], point[i][2], x1 , y1)
            print("Points going")


def draw_point():
    global left_mouse, time, spacebar
    glEnable(GL_POINT_SMOOTH)
    glPointSize(15)
    glBegin(GL_POINTS)

    for i in range(len(point)):
        x, y, color, x1 , y1 = point[i]

        if spacebar:
            x1 = 0
            y1 = 0
            left_mouse = False  
       
        if left_mouse and not spacebar:
            diff = (glutGet(GLUT_ELAPSED_TIME) - time) % 600

            if diff < 100:
                color = (0.0, 0.0, 0.0)
            else:
                original_color = colors[i]
                color = original_color

        glColor3f(color[0],color[1],color[2])
        glVertex2f(x, y)
        x += 0.07 * x1
        y += 0.07 * y1
        if x < 15 :
            x = 15
            x1 = - x1
        if x > 500-15 :
            x = 500-15
            x1 = - x1
        if y < 15 :
            y = 15
            y1 = - y1
        if y > 800 - 15 :
            y = 500-15
            y1 = - y1

        point[i] = (x, y, color, x1 , y1)

    glEnd()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500,800)
glutCreateWindow(b"task 2 ")
glutDisplayFunc(display)
glutMouseFunc(click_mouse)
glutSpecialFunc(arrow_key)
glutKeyboardFunc(click_keyboard)
glutIdleFunc(display)
glutMainLoop()















