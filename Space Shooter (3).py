from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random

# Game flags
x_r,y_r,z_r = False,False,False
start_game = False
wlc = True
over = False
fpview = False
scaling  = True
scaling2 = True
sheild = False
Bomb  = False
bonus_pos = None       
cube = False 
#arrays
enim = []
bullets = []
bombarr = []


#variables
time_1 = time.time()
time_2 = time_1
sheild_on = 0 

camera_pos = (0,5, 500)
fovY = 120  
p_x,p_y, p_z= 0, 0, 0
angle  = 0
bonus_s_time = 0   
bonus_e_time = 0 
gr_len = 90
enemy = 6

#game variables
life_r = 10
bullet_r = 40
score = 0
bomb_r = 10

def space():
    global gr_len
    for r in range(12):
        begin_y =gr_len*6 - r*gr_len
        for j in range(12):
            begin_x = gr_len*6 - j*gr_len
            glBegin(GL_QUADS)
            glColor3f(0.4, 0.4, 0.95)
            glVertex3f(begin_x,begin_y,0)
            glVertex3f(begin_x - gr_len, begin_y, 0)
            glVertex3f(begin_x - gr_len, begin_y - gr_len, 0)
            glVertex3f(begin_x, begin_y - gr_len, 0)
            glEnd()


def draw_star():
    global scaling2
    for x in range(-500, 501, 100): 
        for y in range(-500, 501, 100): 
            if scaling2:
                glPointSize(3)
                glColor3f(1.0, 1.0, 1.0)
            else:
                glPointSize(1.5)
                glColor3f(0, 0, 0)
            glBegin(GL_POINTS)

            glVertex3f(x , y , 2) 
            glEnd()


def space_boarder():
    global gr_len
    ht = 7

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glVertex3f(-540, -540, 0)
    glVertex3f(-540,  540, 0)
    glVertex3f(-540,  540, ht)
    glVertex3f(-540, -540, ht)

    glColor3f(1, 1, 1)
    glVertex3f(540, -540, 0)
    glVertex3f(540,  540, 0)
    glVertex3f(540,  540, ht)
    glVertex3f(540, -540, ht)

    glColor3f(1, 1, 1)
    glVertex3f(-540, -540, 0)
    glVertex3f( 540, -540, 0)
    glVertex3f( 540, -540, ht)
    glVertex3f(-540, -540, ht)

    glColor3f(1, 1, 1)
    glVertex3f(-540, 540, 0)
    glVertex3f( 540, 540, 0)
    glVertex3f( 540, 540, ht)
    glVertex3f(-540, 540, ht)

    glEnd()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1280, 0, 720) 
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def game_begin():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1280, 0, 720)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    box_x, box_y = 530, 400
    box_width, box_height = 330, 70

    glColor3f(1,1,1) 
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex2f(box_x, box_y)
    glVertex2f(box_x + box_width, box_y)
    glVertex2f(box_x + box_width, box_y + box_height)
    glVertex2f(box_x, box_y + box_height)
    glVertex2f(box_x, box_y)
    glVertex2f(box_x, box_y + box_height)
    glVertex2f(box_x + box_width, box_y)
    glVertex2f(box_x + box_width, box_y + box_height)
    
    glEnd()

    
    draw_text(box_x + 100, box_y + 25, "Start Game", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(box_x+15 , box_y - 25, "Welcome to Space Shooter!", GLUT_BITMAP_HELVETICA_18)
    draw_text(box_x + 105, box_y - 50, "Press 'g' to Start", GLUT_BITMAP_HELVETICA_12)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def fighter_spaceship():
    global over,p_x,p_y,angle,x_r,y_r,z_r,scaling,sheild

    glPushMatrix()
    glTranslatef(p_x, p_y, 0)
    
    
    if scaling:
        glScalef (.9, .9, 1) 
    else:
        glScalef (.8, .8, 1) 

    if x_r:
        glRotatef(angle, 1, 0, 0)
    elif z_r:
        glRotatef(angle, 0, 1, 0)
    else:
        glRotatef(angle, 0, 0, 1)

    if sheild:
        gluSphere(gluNewQuadric(), 100, 21, 21)

    # Ship body
    glPushMatrix()
    glColor3f(1, .4, .4)
    glScalef (1, 1, .5)
    glutSolidCube(70)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 0, 0)
    glScalef (1, 1.6, .5)
    glutSolidCube(30)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -95, 5)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.7, 0.8, 0.8)
    gluCylinder(gluNewQuadric(), 3, 13, 60, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-45, 5, 5)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 15, 60, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(45, 5, 5)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 15, 60, 10, 10)
    glPopMatrix()

    glPopMatrix()



def draw_enemy(e):
    global scaling
    x,y,z = e[0],e[1],e[2]
    glPushMatrix()
    glTranslatef(x, y, z)
    
    if scaling: 
        glScalef (1, 1, 1) 
    else:
        glScalef (.8, .8, .8) 

    glColor3f(.7, .6, .6)
    glTranslatef(0, 0, 0)
    glutSolidCube(40)
    
    glColor3f(0.4,0,0.5)
    glTranslatef(0, 0, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 2, 40, 10, 10)
    glPopMatrix()

def pos_maker():
    global gr_len,enemy
    min = int(12*gr_len/2) #to check if pos crosses boundary
    while True:
        x,y = random.randint(-(min-55),(min-55)),-500
        if abs(x) > 150 or abs(y) > 150: 
            break
    return [x,y,0,2]

#assigning x and y pos of enemies
for i in range(enemy):
    enim.append(pos_maker())

def draw_bullets():
    glColor3f(1, 0, 0)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet[0], bullet[1], bullet[2])
        glutSolidCube(10)
        glPopMatrix()


def draw_bomb():
    glColor3f(1, 1, 0)  # yellow bombs
    for bomb in bombarr:
        glPushMatrix()
        glTranslatef(bomb[0], bomb[1], bomb[2])
        glutSolidCube(20)
        glPopMatrix()

#bonus 
def draw_bonus():
    global cube, bonus_pos
    if cube and bonus_pos:
        glPushMatrix()
        glColor3f(0, 1, 1)  
        glTranslatef(bonus_pos[0], bonus_pos[1], bonus_pos[2])
        glutSolidCube(30)
        glPopMatrix()

def random_bonus():
    global bonus_pos, bonus_s_time, cube, bonus_e_time

    c_time = time.time()
    if not cube and c_time - bonus_s_time >= 30:
        bonus_pos = [random.randint(-50, 50), random.randint(-50, 500), 0]
        cube = True
        bonus_s_time = c_time
        bonus_e_time = c_time

    if cube and c_time - bonus_e_time >= 10:
        cube = False
        bonus_pos = None

def get_bonus():
    global cube, bonus_pos, bomb_r, life_r, bullet_r

    if cube and bonus_pos:
        if abs(p_x - bonus_pos[0]) < 35 and abs(p_y - bonus_pos[1]) < 35:
            bomb_r = 20
            life_r = 10
            bullet_r = 40
            print('Accessories Boosted')
            cube = False
            bonus_pos = None


def shottt():
    global bullets, bullet_r,over,life_r,sheild
    for t in bullets:
        t[0] += t[3] * 5
        t[1] += t[4] * 5
        t[3] += t[5] * 5
    if sheild:
        pos = 100
    else:
        pos = 540
    l = 0
    while l < len(bullets):
        pos_x, pos_y = bullets[l][0], bullets[l][1]
        if abs(pos_x) >= pos or abs(pos_y) >= pos:
            bullets.pop(l)
            bullet_r-=1   
        else:
            l += 1

    if bullet_r < 0 or life_r == 0:
        over = True
        enim.clear()


def ship_crash():
    global bullets, over, p_y, p_x, score, life_r, bullet_r,sheild
    for y in enim:
        dx = p_x - y[0]
        dy = p_y - y[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 1:
            y[1] += (dy / distance) * 0.1

    if not over:
        for y in enim:
            if abs(p_x - y[0]) < 100 and abs(p_y - y[1]) < 100 :
                if life_r > 0 :
                    if  sheild==False:
                        life_r -= 1
                    else:
                        score+=1
                    enim.remove(y)
                    enim.append(pos_maker())
                else:
                    over = True
                    enim.clear()
                break


def kill_alliens():
    global bullets, score, enim, life_r, over

    a = [] #bullets_to_be_removed
    b = [] #updated enemies

    for y in enim:
        fired = False
        for t in bullets:
            bx, by = t[0], t[1]
            ex, ey = y[0], y[1]

            if abs(bx - ex) < 30 and abs(by - ey) < 30 :
                
                if y[3]==0:
                    fired = True
                    score += 1
                    a.append(t)
                    break
                else:
                    y[3]-=1
                    a.append(t)

        if fired==True:
            b.append(pos_maker())
        else:
            b.append(y)

    for e in a:
        if e in bullets:
            bullets.remove(e)

    enim[:] = b



def shot_bomb():
    global bombarr, enim, score
    for bomb in bombarr:
        bomb[0] += bomb[3] * 6
        bomb[1] += bomb[4] * 6
        bomb[2] += bomb[5] * 0.5  

    l = 0
    while l < len(bombarr):
        pos_x, pos_y = bombarr[l][0], bombarr[l][1]
        if abs(pos_x) >= 540 or abs(pos_y) >= 540:
            bombarr.pop(l)
        else:
            l += 1

    new_enemies = []
    for y in enim:
        hit = False
        for b in bombarr:
            if abs(b[0] - y[0]) < 30 and abs(b[1] - y[1]) < 30:
                score += 1
                hit = True
                break
        if not hit:
            new_enemies.append(y)
        else:
            new_enemies.append(pos_maker())

    enim[:] = new_enemies


def keyboardListener(key, x, y):
    global wlc,start_game,over,x_r,y_r,z_r,fpview,sheild,Bomb
    global p_x,p_y,angle,score,bullet_r,life_r,enemy,sheild_on
    
    if key == b'w' and not over:
        if p_y>-480:
            p_y-=5
        
    elif key == b's' and not over:
        if p_y<480:
            p_y+=5
    
    elif key == b'x' and not over:
        x_r = True
        angle+=5
        y_r,z_r = False,False

    elif key == b'y' and not over:
        y_r = True
        angle+=5
        x_r,z_r = False,False

    elif key == b'z' and not over:
        z_r = True
        angle+=5
        y_r,x_r = False,False

    elif key == b'd' and not over:
        if p_x>-500:
            p_x-=5
    
    elif key == b'a' and not over:
        if p_x<500:
            p_x+=5
    
    if key == b'g' and wlc:
        wlc = False
        start_game = True

    elif key == b'f':
        fpview = not fpview
        print('First Person View Is On')

    elif key == b' ':
        if not sheild:  
            sheild_on = time.time()
            score -= 3
        sheild = True
        print('Sheild Is On')

    if key == b'l' and not over:
        if bullet_r<20:
            score -= 5
            bullet_r = 20
        else:
            print('Bullet is Already Loaded')

    
    
    if key == b'r'and over: #restart
        bullets.clear()
        enim.clear()
        for l in range(enemy):
            e = pos_maker()
            enim.append(e)
            
        score = 0
        bullet_r = 40
        life_r = 10
        over = False
        sheild = False
        Bomb  = False
        p_x,p_y = 0, 0
        angle = 0
        print("Game restarted!")
            
        glutPostRedisplay()


    


def specialKeyListener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    if key == GLUT_KEY_LEFT:
        if x>-450:
            x -= 5
    elif key == GLUT_KEY_RIGHT:
        if x<450:
            x += 5
    elif key == GLUT_KEY_UP:
        if y<550:
            y += 5
    elif key == GLUT_KEY_DOWN:
        if y>5:
            y -= 5
    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    global p_x, p_y, angle, bullets, over,Bomb, bombarr, bomb_r
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not over :
            Bomb = False
            rad = math.radians(angle)
            dir_x = math.sin(rad)
            dir_y = -math.cos(rad)
            cannon_offset = 90  
            bx = p_x + cannon_offset * dir_x
            by = p_y + cannon_offset * dir_y
            bz = 10 

            bullets.append([bx, by, bz, dir_x, dir_y, 0])

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not over:
            if bomb_r>0:
                Bomb =True

                for y in enim:
                    dx = y[0] - p_x-10
                    dy = y[1] - p_y +95
                    dz = y[2] - 5
                    dist = math.sqrt(dx**2 + dy**2+5**2)
                    if dist == 0: 
                        continue
                    bombarr.append([p_x, p_y, 5, dx / dist, dy / dist, dz/dist])
            else:
                print('No Bomb Remaining')
            

    glutPostRedisplay()


def setupCamera():
    global fpview, p_x, p_y

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if fpview:
       
        cam_x = p_x
        cam_y = p_y + 20   
        cam_z = 70     

       
        look_x = p_x
        look_y = p_y
        look_z = 40

        gluLookAt(cam_x, cam_y, cam_z,
                  look_x, look_y, look_z,
                  0, 0, 1)  

    else:
        x, y, z = camera_pos
        gluLookAt(x, y, z, 
                  0, 0, 0, 
                  0, 0, 1)


def idle():

    global scaling,scaling2, time_1, time_2, sheild,sheild_on,Bomb

    ship_crash()
    if Bomb==False:
        shottt() 
    else:
        shot_bomb()
    kill_alliens()
    random_bonus()
    get_bonus()

    ftime = time.time()
    

    if ftime - time_1 >= .7:
        scaling = not scaling
        time_1 = ftime
    
    if ftime - time_2 >= .4:
        scaling2 = not scaling2
        time_2 = ftime

    if sheild and (time.time() - sheild_on >= 7):
        sheild = False

    glutPostRedisplay()

def showScreen():
    global start_game,wlc,over,life_r,bullet_r,score,Bomb, bullet_r

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(.1,.2,.3,.5)	
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
   
    if wlc:
        game_begin()
        
    else:
        space()
        space_boarder()
        draw_star()
        draw_bonus()
        fighter_spaceship()
        if Bomb==False:
            draw_bullets()
        else:
            draw_bomb()
        for i in enim:
            draw_enemy(i)
        if not over:
            draw_text(10, 690, f"Life Remainig: {life_r*'[]'}",GLUT_BITMAP_HELVETICA_12)
            draw_text(1110, 690, f"Match Score : {score} ",GLUT_BITMAP_HELVETICA_12)
            draw_text(10, 670, f"Bullets Remainig : {bullet_r} ",GLUT_BITMAP_HELVETICA_12)
            draw_text(10, 650, f"Bombs Remainig : {bomb_r} ",GLUT_BITMAP_HELVETICA_12)

        else:
            draw_text(450, 690, f"Game is Over. Score is {score}.",GLUT_BITMAP_TIMES_ROMAN_24)
            draw_text(480, 660, f'Press <r> to RESTART',GLUT_BITMAP_TIMES_ROMAN_24)


       
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800) 
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"3D Space Shooter")
     
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()
    

if __name__ == "__main__":
    main()
