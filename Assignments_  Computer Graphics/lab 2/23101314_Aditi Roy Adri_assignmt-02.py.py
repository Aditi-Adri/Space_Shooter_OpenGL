from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

x1 = 30
x3 = 250
x4 = 10
x5 = 270
x6 = 31  
y1 = 10
y2 = 50  

bc = False
cnt = 0 

score = 0 
dc = False
pausee = False
start = False
over = False


dx = random.randint(50, 770)
dy = 600
velocity = 1.4
k = 1.4
a , b , c = random.uniform(0.6, 1.0) , random.uniform(0.6, 1.0) , random.uniform(0.6, 1.0)

######################################################################################################

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            return 0  
        elif dx < 0 and dy >= 0:
            return 3  
        elif dx < 0 and dy < 0: 
            return 4  
        elif dx > 0 and dy < 0: 
            return 7  
    else:
        if dx >= 0 and dy > 0: 
            return 1  
        elif dx < 0 and dy > 0: 
            return 2  
        elif dx < 0 and dy < 0: 
            return 5  
        elif dx >= 0 and dy < 0: 
            return 6  

def zero_to_main(zone, x, y):
    if zone == 0: 
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2: 
        return -y, x
    elif zone == 3: 
        return -x, y
    elif zone == 4: 
        return -x, -y
    elif zone == 5: 
        return -y, -x
    elif zone == 6: 
        return y, -x
    elif zone == 7: 
        return x, -y

def main_to_zero(zone, x, y):
    if zone == 0: 
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2: 
        return y, -x  
    elif zone == 3: 
        return -x, y
    elif zone == 4: 
        return -x, -y
    elif zone == 5: 
        return -y, -x
    elif zone == 6: 
        return -y, x  
    elif zone == 7:
        return x, -y

def mid_point_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)

    x1, y1 = main_to_zero(zone, x1, y1)
    x2, y2 = main_to_zero(zone, x2, y2)

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)

    x, y = x1, y1

    glBegin(GL_POINTS)
    while x <= x2:
        px, py = zero_to_main(zone, x, y)
        glVertex2f(px, py)

        if d <= 0:
            d += dE
        else:
            d += dNE
            y += 1
        x += 1
    glEnd()

##################################################################################################

def resume():
    glColor3f(1.0, 1.0, 0.0)  
    mid_point_line(400, 550, 400, 595)  
    mid_point_line(425, 550, 425, 595)  

def pause():
    glColor3f(1.0, 1.0, 0.0)
    mid_point_line(400, 595, 400, 550)  
    mid_point_line(405, 595, 425, 572)  
    mid_point_line(400, 550, 425, 572)  


def basket():
    global x1, x3, x5, x4, x6, y1, y2, bc, over
    if bc or over :  
        glColor3f(1.0, 0.0, 0.0)  
    else:
        glColor3f(1.0, 1.0, 1.0)  
    
    mid_point_line(x1, y1, x3, y1)     
    mid_point_line(x1, y1, x4, y2)     
    mid_point_line(x3, y1, x5, y2)     
    mid_point_line(x4, y2, x5, y2)   


def cross():
    glColor3f(1.0, 0.0, 0.0)  
    mid_point_line(650, 595, 675, 550) 
    mid_point_line(650, 550, 675, 595)  


def restart():
    glColor3f(0.0, 1.0, 1.0)  
    mid_point_line(150, 575, 200, 575)  
    mid_point_line(150, 575, 170, 585)  
    mid_point_line(150, 575, 170, 565)  


def move_basket(key, x, y):
    global x1, x6, x3, x4, x5
    if over:  
        return
    
    if (pausee == False):
        if (key == GLUT_KEY_RIGHT):
            if (x1 < 800) and (x6 < 800) and (x3 < 800) and (x4 < 800) and (x5 < 800):
                x1 += 10
                x6 += 10
                x3 += 10
                x4 += 10
                x5 += 10

        if (key == GLUT_KEY_LEFT):
            if (x1 > 0) and (x6 > 0) and (x3 > 0) and (x4 > 0) and (x5 > 0):
                x1 -= 10
                x6 -= 10
                x3 -= 10
                x4 -= 10
                x5 -= 10

    glutPostRedisplay()



def collision(xd, yd):
    global x1, x3, y1, y2, score, over, dc

    dl = xd - 30
    dr = xd + 30
    db = yd
    dt = yd + 60

    bl = x1
    br = x3
    bb = y1
    bt = y2

    if (dr > bl and dl < br and dt > bb and db < bt):
        score += 1
        print(f"YOUR SCORE : {score}")
        dc = True
        return True

    if dt < bb and not over:
        print(f"GAME OVER !! YOUR FINAL SCORE : {score}")
        over = True  
        return False

    return False



def diamond():
    global dx, dy, velocity, a, b, c, dc, over
    if over:  
        return

    dy -= velocity

    if dc: 
        a, b, c = random.uniform(0.3, 1.0), random.uniform(0.3, 1.0) , random.uniform(0.3, 1.0)
        dc = False
    glColor3f(a, b, c)

    mid_point_line(dx, dy, dx + 30, dy + 30)
    mid_point_line(dx + 30, dy + 30, dx, dy + 60)
    mid_point_line(dx, dy + 60, dx - 30, dy + 30)
    mid_point_line(dx - 30, dy + 30, dx, dy)


    if collision(dx, dy):
        dy = 600  
        dx = random.randint(50, 770)  
        velocity += 0.2  

    elif dy < 0 and over == False :  
        print(f"SORRY ! GAME OVER !! YOUR SCORE : {score}")
        over = True  


def what_to_do(button, state, x, y):
    global x1, x2, x3, x4, x5, x6, score, over, pausee, start, dx, dy, velocity, k, dc
    y = 600 - y  

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN :
        if 150 <= x <= 200 and 565 <= y <= 585:
            over = False
            pausee = False
            dx = random.randint(50, 770)
            dy = 600
            velocity = 1.4
            start = True
            score = 0
            cnt = 0
            dc = True
            print("Hi ! GAME STARTING OVER !")
            return

        if 640 <= x <= 685 and 540 <= y <= 600:
            print(f"GOODBYE !! YOUR SCORE : {score}")
            glutLeaveMainLoop()
            return

        if not over and 400 <= x <= 425 and 550 <= y <= 595:
            if pausee: 
                pausee = False
                velocity = k
                print("RESUME THE GAME")
            else:  
                pausee = True
                k = velocity
                velocity = 0
                print("PAUSED THE GAME")
            return

    glutPostRedisplay()




def control():
    global dx, dy, pausee, over , bc

    if not pausee and over == False :
        if dy < 0:
            over = True
            pausee = True
            bc = True
            print(f"SORRY ! GAME OVER !! YOUR SCORE : {score}")
        collision(dx, dy)

    time.sleep(0.01)
    glutPostRedisplay()



def pr():
    global pausee
    if pausee:
        pause()
    else:
        resume()


def iterate():
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    basket()
    restart()
    cross()
    pr()    
    diamond()  
    glutSwapBuffers()
    


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 600)
glutInitWindowPosition(400, 50)
wind = glutCreateWindow(b"Catch your diamond")
glutDisplayFunc(showScreen)
glutIdleFunc(control)
glutSpecialFunc(move_basket)
glutMouseFunc(what_to_do)
glutMainLoop()
