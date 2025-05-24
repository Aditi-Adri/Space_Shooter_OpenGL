from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# chk = True  --> will alternate white purple

camera_pos = (0,290,500)

position_pl = [0, 0, 0]
player_angle = 0
bullets = []  
opponent_count = []  
what_person = "third"  
over = False

live = 5
score = 0
bullet = 0               

cht = False
gun = False
but = False 
cht_round = 1.0


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////


def drawing():
   # board
    for i in range(13):
        for j in range(13):
            x_s = (j * 98) - ( 13/2 ) * 100  
            y_s = (i * 98) - ( 13/2 ) * 100  

            
            if (i + j ) % 2 == 0 :
                glColor3f(0.7, 0.5, 0.95)   # beguni
            else:
                glColor3f(1,1,1)            # shada

            
            glBegin(GL_QUADS)
            glVertex3f(x_s, y_s, 0)           # niche bam
            glVertex3f(x_s + 98, y_s, 0)      # niche dan
            glVertex3f(x_s + 98, y_s + 98, 0) # upor dan
            glVertex3f(x_s, y_s + 98, 0)      # upor bam
        
            glEnd()


    # wall 
    glBegin(GL_QUADS)

    # niche
    glColor3f(1, 1, 1)
    glVertex3f(-98 * 13 // 2, -98 * 13 // 2, 0)
    glVertex3f(98 * 13 // 2, -98 * 13 // 2, 0)
    glVertex3f(98 * 13 // 2, -98 * 13 // 2, 200)
    glVertex3f(-98 * 13 // 2, -98 * 13 // 2, 200)

    # upore
    glColor3f(0.01, 0.9, 1)
    glVertex3f(-98 * 13 // 2, 98 * 13 // 2, 0)
    glVertex3f(98 * 13 // 2, 98 * 13 // 2, 0)
    glVertex3f(98 * 13 // 2, 98 * 13 // 2, 200)
    glVertex3f(-98 * 13 // 2, 98 * 13 // 2, 200)

    # bam
    glColor3f(0, 0, 1)
    glVertex3f(-98 * 13 // 2  + 8, -98 * 13 // 2, 0)
    glVertex3f(-98 * 13 // 2+50 + 8 , 98 * 13 // 2, 0)
    glVertex3f(-98 * 13 // 2  + 8 , 98 * 13 // 2, 200)
    glVertex3f(-98 * 13 // 2  + 8, -98 * 13 // 2, 200)

    # dan
    glColor3f(0.01, 0.9, 0.01)
    glVertex3f(98 * 13 // 2 - 14 , -98 * 13 // 2, 0)
    glVertex3f(98 * 13 // 2 - 14 , 98 * 13 // 2, 0)
    glVertex3f(98 * 13 // 2 - 14 , 98 * 13 // 2, 200)
    glVertex3f(98 * 13 // 2 - 14 , -98 * 13 // 2, 200)

    glEnd()


def player():
    glPushMatrix()
    glTranslatef(position_pl[0], position_pl[1], position_pl[2])
    glRotatef(player_angle, 0, 0, 1)  
    if over:
        glRotatef(90,0,1,0)
    
    # pa - # gluCylinder(quadric, base radius, top radius, height, slices, stacks)
    glColor3f(0, 0, 1)
    glTranslatef(0,-23,-95)
    glRotatef(180, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 14, 9, 102, 15, 10) 
    glColor3f(0, 0, 1)
    glTranslatef(0,-80,0)
    gluCylinder(gluNewQuadric(), 14, 9, 102, 15, 10) 

    # Body
    glColor3f(0.4, 0.5, 0)
    glTranslatef(0, 48, -40)
    glutSolidCube(75)

    # Gun
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0, 0, 48)
    glTranslatef(30, 0, -90) 
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 17, 7, 120, 15, 10) 

    # Hand
    glColor3f(1, 0.7, 0.6)
    glTranslatef(0, -28, 0)
    gluCylinder(gluNewQuadric(), 13, 7, 77, 15, 10) 
    glColor3f(1, 0.7, 0.6)
    glTranslatef(0, 53, 0)
    gluCylinder(gluNewQuadric(), 13, 6, 77, 15, 10) 

    # Head
    glColor3f(0, 0, 0)
    glTranslatef(40,-25, -25)
    gluSphere(gluNewQuadric(), 33, 15, 10)
    glPopMatrix()
    

def opponent(i):
    glPushMatrix()
    glTranslatef(i[0], i[1], i[2])
    glScalef(i[3], i[3], i[3])
    glColor3f(1, 0, 0)
    glTranslatef(0, 0, 37)
    gluSphere(gluNewQuadric(), 40, 30, 21)
    glColor3f(0,0,0)
    glTranslatef(0, 0, 45)
    gluSphere(gluNewQuadric(), 29, 15, 10)
    glPopMatrix()


def bulletss():
    glColor3f(1, 0, 0)
    for j in bullets:
        glPushMatrix()
        glTranslatef(j[0], j[1],j[2])
        glutSolidCube(16)
        glPopMatrix()


def where_opponent_come():
    while True:
        x = random.randint((-13 * 100 // 2)-50, (13 * 100 // 2)-100)
        y = random.randint((-13 * 100 // 2)-50, (13 * 100 // 2)-100)
        if abs(x) > 188 or abs(y) > 188:
            break
    return [x, y, 0, 1.0, 0.003]      # [pos , pos, 0 , scale , timtim]


def player_hitted():
    global live, over
    for i in opponent_count :
        p = position_pl[0] - i[0]
        q = position_pl[1] - i[1]
        d = math.sqrt(p**2 + q**2)   # pythagorus
        if d > 1:
            i[0] += (p / d) * 0.04
            i[1] += (q / d) * 0.04

        i[3] += i[4]
        if i[3] >= 1.3 or i[3] <= 0.6:
            i[4] *= -1

    # collision check box ? 
    if not over :
        for j in opponent_count:
            if abs(position_pl[0] - j[0]) < 100 and abs(position_pl[1] - j[1]) < 100 and abs(position_pl[2] - j[2]) < 100 :
                if live > 0:
                    opponent_count.remove(j)
                    opponent_count.append(where_opponent_come())
                    live -= 1
                else:
                    opponent_count.clear()
                    over = True
                break


def kill():
    global bullets, bullet, over, cht, gun
    for j in bullets:
        j[0] += j[3] * 10
        j[1] += j[4] * 10
    
    i = 0
    while i < len(bullets) :
        pos_x, pos_y, pos_z = bullets[i][0], bullets[i][1], bullets[i][2]
        if abs(pos_x) >= 600 or abs(pos_y) >= 600:
            bullets.pop(i)
            if not cht and not gun:
                bullet += 1
        else:
            i += 1
       
    if bullet >= 10 or live == 0:
        over = True
        opponent_count.clear()


def enemy_hitted():
    global bullets, score, opponent_count, live, over

    b_r = []
    n_en = []

    for j in opponent_count:
        kill = False
        for b in bullets:
            bx, by, bz = b[0], b[1], b[2]
            ex, ey, ez = j[0], j[1], j[2]

            if abs(bx - ex) < 30 and abs(by - ey) < 30 and abs(bz - ez) < 30:
                kill = True
                score += 1
                b_r.append(b)
                break

        if kill :
            n_en.append(where_opponent_come())
        else:
            n_en.append(j)

        for i in b_r:          # jesob ber hoise tara remove from list
            if i in bullets:
                bullets.remove(i)

    opponent_count[:] = n_en       # no of ene goes to oppo count



def do_cheat_in_game():
    global player_angle, position_pl, score, bullets, opponent_count, bullet
    if cht and not over:
        player_angle += 0.8
        player_angle %= 360
        kon = math.radians(player_angle)
        # position in front of the player to opponent
        bigx = position_pl[0] + 50 * math.sin(kon) + (-math.cos(kon)) * 142
        bigy = position_pl[1] - 50 * math.cos(kon) + ( -math.sin(kon)) * 142
        bigz = position_pl[2] + 10

        for j in list(opponent_count) :
            span = math.sqrt((j[0] - bigx)**2 + (j[1] - bigy)**2)   # distance between enemy and hero
            if span == 0:
                continue
            multiply = (-math.cos(kon)) * (j[0] - bigx) / span + (-math.sin(kon)) * (j[1] - bigy) / span   # dot product for calculating opponents position , got from google 

            if multiply > 0.995 and span <= 450 :   #opponent in our range 
                dx, dy, dz = j[0] - bigx, j[1] - bigy, j[2] - bigz
                len = math.sqrt(dx**2 + dy**2 + dz**2)  # pythagorus distance of opponent
                if len == 0:
                    continue

                dir_to_enemy = (dx / len, dy / len, dz / len)
                x = [bigx, bigy, bigz, dir_to_enemy[0], dir_to_enemy[1], dir_to_enemy[2]]
                bullets.append(x)

                score += 1
                opponent_count.remove(j)
                opponent_count.append(where_opponent_come())   # old one removed , should be replaced with new one
                break
    glutPostRedisplay()


seen_last_cam = [0, 0, 0]
def cam_setter():
    global seen_last_cam, camera_pos, position_pl, player_angle
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(120, 1.25, 0.1, 1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if what_person == "third":
        a,b,c = camera_pos
        gluLookAt(a,b,c, 0, 0, 0, 0, 0, 1)

    elif what_person == "first":
        my_face = math.radians(player_angle)

        eyex = position_pl[0] + 30 * math.sin(my_face) - math.cos(my_face) * 50
        eyey = position_pl[1] - 30 * math.cos(my_face) - math.sin(my_face) * 50
        eyez = position_pl[2] + 40

        if cht and gun:
            seex = eyex + (-math.cos(my_face)) * 100
            seey = eyey + (-math.sin(my_face)) * 100
            seez = eyez

            seen_last_cam = [seex, seey, seez]

        elif cht:
            seex, seey, seez = 30, 10, 5
            seex, seey, seez = seen_last_cam

        else:
            seex = eyex + (-math.cos(my_face)) * 100
            seey = eyey + (-math.sin(my_face)) * 100
            seez = eyez

        gluLookAt(eyex, eyey, eyez, seex, seey, seez, 0, 0, 1)
        

def listen_to_Keyboard(key, x, y):
    global position_pl, player_angle, what_person, min_bound, max_bound, live, bullet, score, over,cht,gun
   
    if not over:
        if key == b'w':  
            r = -math.cos(math.radians(player_angle)) * 18
            s = -math.sin(math.radians(player_angle)) * 18

            p = position_pl[0] + r
            q = position_pl[1] + s

            if -13 * 100 / 2 <= p <= 13 * 100 / 2 and -13 * 100 / 2 <= q <= 13 * 100 / 2 :
                position_pl[0] = p
                position_pl[1] = q

        elif key == b's':  
            r = math.cos(math.radians(player_angle)) * 18
            s = math.sin(math.radians(player_angle)) * 18

            p = position_pl[0] + r
            q = position_pl[1] + s

            if -13 * 100 / 2 <= p <= 13 * 100 / 2 and -13 * 100 / 2 <= q <= 13 * 100 / 2 :
                position_pl[0] = p
                position_pl[1] = q

        elif key == b'a':  
            player_angle += 5

        elif key == b'd':
            player_angle -= 5

        elif key == b"c": 
            cht = not cht
            if cht:
                do_cheat_in_game()
            else:
                gun = False
        
        elif key == b"v":
            if cht  :
                if what_person == "third":
                    what_person = "first"
                else:
                    what_person = "third"
            glutPostRedisplay()


    if key == b'r' and over: 
        for i in range(5):
            enemy = where_opponent_come()
            opponent_count.append(enemy)
        bullets.clear()
        opponent_count.clear()
        score = 0
        position_pl[:] = [0, 0, 0]
        bullet = 0
        live = 5
        over = False
        player_angle = 0
        print("Your Game Restarted Successfully !") 
        glutPostRedisplay()





def specialKeyListener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    if not over:
        if key == GLUT_KEY_DOWN : # zoom out
            y += 5
            z += 5 

        if key == GLUT_KEY_UP and z > 10  : # zoom in               # problem ase 
            y *= 0.98
            z *= 0.98

        if key == GLUT_KEY_LEFT: #  left
            x -= 5

        if key == GLUT_KEY_RIGHT:  # right 
            x += 5

    camera_pos = (x, y, z)



def mouseListener(button, state, x, y) :
    global what_person, over, player_angle
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not over :
        kon = math.radians(player_angle)
        bigx = position_pl[0] + 50 * math.sin(kon) + (-math.cos(kon)) * 142
        bigy = position_pl[1] - 50 * math.cos(kon) + (-math.sin(kon)) * 142
        bigz = position_pl[2] + 10
        bullets.append([bigx, bigy, bigz, (-math.cos(kon)), (-math.sin(kon)), 0])

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN  :
        if what_person == "third":
            what_person = "first"
        else:
            what_person = "third"
        glutPostRedisplay()



def idle():
    kill()
    enemy_hitted()
    player_hitted()
    do_cheat_in_game()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)  
    cam_setter()  
    drawing()

    if not over:
            draw_text(10, 770, f"Player Life Remaining: {live}")
            draw_text(10, 740, f"Game Score: {score}")
            draw_text(10, 710, f"Bullet Missed: {bullet}")
    else:
        draw_text(10, 740, f"Game Over. Your total score is {score}.")
        draw_text(10, 710, f'Please Press "R" to RESTART the Game.')

    player()
    bulletss()
    for i in opponent_count:
        opponent(i)
    glutSwapBuffers()


# text drawing , copied from Template
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):    
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)  
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



for j in range(5):
        opponent_count.append(where_opponent_come())

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) 
    glutInitWindowSize(1000, 800)  
    glutInitWindowPosition(0, 0)  
    wind = glutCreateWindow(b"3D OpenGL Intro")  
    glutDisplayFunc(showScreen)  # others drawing showing
    glutKeyboardFunc(listen_to_Keyboard)  # keybo
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # it will throw guli auto
    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()