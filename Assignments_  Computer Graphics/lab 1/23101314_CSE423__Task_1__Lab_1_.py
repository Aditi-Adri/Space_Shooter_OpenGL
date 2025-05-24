from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random 

bg = (245/255, 182/255, 66/255, 0)  
cnt = 0  
angle = 0.01
raindrop_arr = []
for i in range(50):
    x2 = random.uniform(100, 600)
    y2 = random.uniform(100, 600)
    length = random.uniform(5, 15) 
    raindrop_arr.append((x2, y2, length))


def showScreen():
    glClearColor(bg[0], bg[1], bg[2], bg[3])
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_trees()
    draw_house()
    draw_rain()
    glutSwapBuffers()


def iterate():
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 600, 0, 1.0) 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw_trees():
    glColor3f(23/255, 84/255, 6/255)
    for i in range(0, 800, 50):
        glBegin(GL_TRIANGLES)
        glVertex2f(i + 20, 250)
        glVertex2f(i + 50, 250)
        glVertex2f(i + 35, 285)
        glEnd()


def draw_house():
    # roof
    glColor3f(153/255, 76/255, 0)
    glBegin(GL_TRIANGLES)
    glVertex2d(200, 400)  
    glVertex2d(600, 400)  
    glVertex2d(400, 550)  
    glEnd()
    
    # body
    
    glColor3f(1, 1, 1)
    glBegin(GL_TRIANGLES)
    glVertex2d(200, 400)
    glVertex2d(600, 400)
    glVertex2d(200, 250)
    glVertex2d(200, 250)
    glVertex2d(600, 400)
    glVertex2d(600, 250)
    glEnd()


    # stair
    glColor3f(51/255, 0/255, 25/255)
    glBegin(GL_TRIANGLES)
    glVertex2d(150, 250)
    glVertex2d(650, 250)
    glVertex2d(150, 200)
    glVertex2d(650, 250)
    glVertex2d(650, 200)
    glVertex2d(150, 200)
    glEnd()


    # door
    glColor3f(102/255, 0/255, 0/255)
    glBegin(GL_TRIANGLES)
    glVertex2d(375, 375)
    glVertex2d(425, 375)
    glVertex2d(375, 250)
    glVertex2d(375, 250)
    glVertex2d(425, 375)
    glVertex2d(425, 250)
    glEnd()

        
    # window 
    glColor3f(153/255, 0/255, 0/255)
    glBegin(GL_TRIANGLES)
    glVertex2d(250, 350)
    glVertex2d(300, 350)
    glVertex2d(250, 300)
    glVertex2d(250, 300)
    glVertex2d(300, 350)
    glVertex2d(300, 300)
    glEnd()

    
    glColor3f(153/255, 0/255, 0/255)
    glBegin(GL_TRIANGLES)
    glVertex2d(500, 350)
    glVertex2d(550, 350)
    glVertex2d(500, 300)
    glVertex2d(500, 300)
    glVertex2d(550, 350)
    glVertex2d(550, 300)
    glEnd()



def click_keyboard(key, x, y):
    global bg
    global cnt
    ar = [(245/255, 182/255, 66/255, 0),(135/255, 206/255, 235/255, 0),(100/255, 149/255, 237/255, 0),(255/255, 140/255, 0/255, 0),(75/255, 77/255, 75/255, 0),(0.0, 0.0, 0.0, 0.0)]

    if key == b'n':  
        if cnt < 5:
            cnt += 1
        else:
            cnt = 5  
        bg = ar[cnt]
        print("Transitioning to night")
    if key == b'm':  
        if cnt > 0:
            cnt -= 1
        else:
            cnt = 0 
        bg = ar[cnt]
        print("Transitioning to morning")
    glutPostRedisplay()



def click_arrow(key, x, y):
    global angle
    if key == GLUT_KEY_RIGHT:
        angle += 0.5
        print("Tilt Right")
    if key == GLUT_KEY_LEFT:		
        angle -= 0.5
        print("Tilt Left")
    glutPostRedisplay()



def draw_rain():
    for i in raindrop_arr:
        x, y,z = i
        glColor3f(28/255,5/255,97/255)  
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2d(x, y+z)
        glVertex2d(x + angle, y - z)  
        glEnd()


def rain_drops():
    global angle 
    for i in range(0, len(raindrop_arr)-1):
        update_x, update_y,length = raindrop_arr[i] 
        update_x += angle 
        update_y -= length
        
        update_x = random.uniform(0, 800)
        update_y = random.uniform(0, 800)
        raindrop_arr[i] = (update_x, update_y,length)



def animation():
    rain_drops()
    glutPostRedisplay()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 600)  
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Task 1: Building a House in Rainfall")  
glutDisplayFunc(showScreen) 
glutKeyboardFunc(click_keyboard)
glutIdleFunc(animation)
glutSpecialFunc(click_arrow)
glutMainLoop()




