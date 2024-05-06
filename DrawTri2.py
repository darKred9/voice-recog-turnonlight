#using single triangle method detects unlock zone
import serial
from time import sleep
import math
import turtle

int_a = 0
int_b = 0

ser1 = serial.Serial(port='COM3', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS, timeout=0)
ser1.flush()
print("connected to: " + ser1.portstr)

ser2 = serial.Serial(port='COM5', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS, timeout=0)
ser2.flush()
print("connected to: " + ser2.portstr)

distance_a1_a2 = 3.0
meter2pixel = 100
range_offset = 0.9

def screen_init(width=5000, height=1000, t=turtle):
    t.setup(width, height)
    t.tracer(False)
    t.hideturtle()
    t.speed(0)


def turtle_init(t=turtle):
    t.hideturtle()
    t.speed(0)


def draw_line(x0, y0, x1, y1, color="black", t=turtle):
    t.pencolor(color)
    t.up()
    t.goto(x0, y0)
    t.down()
    t.goto(x1, y1)
    t.up()
    t.hideturtle()

def draw_fastU(x, y, length, color="black", t=turtle):
    draw_line(x, y, x, y + length, color, t)


def draw_fastV(x, y, length, color="black", t=turtle):
    draw_line(x, y, x + length, y, color, t)


def draw_cycle(x, y, r, color="black", t=turtle):
    t.pencolor(color)

    t.up()
    t.goto(x, y - r)
    t.setheading(0)
    t.down()
    t.circle(r)
    t.up()


def fill_cycle(x, y, r, color="black", t=turtle):
    t.up()
    t.goto(x, y)
    t.down()
    t.dot(r, color)
    t.up()


def write_txt(x, y, txt, color="black", t=turtle, f=('Arial', 12, 'normal')):

    t.pencolor(color)
    t.up()
    t.goto(x, y)
    t.down()
    t.write(txt, move=False, align='left', font=f)
    t.up()


# def draw_rect(x, y, w, h, color="black", t=turtle):
#     t.pencolor(color)
#
#     t.up()
#     t.goto(x, y)
#     t.down()
#     t.goto(x + w, y)
#     t.goto(x + w, y + h)
#     t.goto(x, y + h)
#     t.goto(x, y)
#     t.up()


def fill_rect(x, y, w, h, color=("black", "black"), t=turtle):
    t.begin_fill()
    # draw_rect(x, y, w, h, color, t)
    t.end_fill()
    pass


def clean(t=turtle):
    t.clear()


def draw_ui(t):
    write_txt(-300, 250, "Localization by triangulation", "black",  t, f=('Arial', 32, 'normal'))
    draw_line(-400, 0, 800, 0) #for X-axis
    draw_line(0, -400, 0, 400)  # for X-axis
    # fill_rect(-400, 200, 800, 40, "black", t)
    # write_txt(-50, 205, "WALL", "yellow",  t, f=('Arial', 24, 'normal'))


def draw_uwb_anchor1(x, y, txt, range, t):
    r = 20
    fill_cycle(x, y, r, "green", t)
    write_txt(x-150, y-20, txt + ": " + str(range) + "cm",
              "green",  t, f=('Arial', 16, 'normal'))

def draw_uwb_anchor2(x, y, txt, range, t):
    r = 20
    fill_cycle(x, y, r, "green", t)
    write_txt(x + r, y-20, txt + ": " + str(range) + "cm",
              "black",  t, f=('Arial', 16, 'normal'))

def draw_uwb_tag(x, y, txt, range, t):
    r = 20
    fill_cycle(x, y, r, "red", t)
    write_txt(x + r, y, txt + ": " + str(range) + "cm",
              "red",  t, f=('Arial', 16, 'normal'))

def main():
    int_a = 0
    int_b = 0
    t_ui = turtle.Turtle()
    t_a1 = turtle.Turtle()
    t_a2 = turtle.Turtle()
    t_a3 = turtle.Turtle()

    turtle_init(t_ui)
    turtle_init(t_a1)
    turtle_init(t_a2)
    turtle_init(t_a3)

    a1_range = 0.0
    a2_range = 0.0
    int_c = 195  # length of triangle base (cm)
    doorUnLock = 0
    draw_ui(t_ui)
    # draw_rect(-20, -180, 220, 480, "aquamarine4")  # rectangle to draw car boundaries
    # draw_rect(-50, -200, 400, 600, "DarkMagenta")  # rectangle to draw unlock boundaries
    draw_uwb_anchor1(0, 0, "A1(0,0)", a1_range, t_a1)
    draw_uwb_anchor2(int_c, 0, "A2("+str(int_c)+",0)", a2_range, t_a2)

    while True:
        byte_b = ser1.readline()
        str_b = byte_b.decode().rstrip()
        byte_a = ser2.readline()
        str_a = byte_a.decode().rstrip()
        
        ser1.flush()
        #ser2.flushOutput()
        # ser2.flushInput()
        ser2.flush()
        print("a: " + str_a)
        print("b: " + str_b)
        if str_a != '':
            int_a = int(float(str_a))
        if str_b != '':
            int_b = int(float(str_b))
        print("a: " + str(int_a))
        print("b: " + str(int_b))
        
        try:
            #ser1.flushOutput()
            # ser1.flushInput()
                # ser1.flush()
                # #ser2.flushOutput()
                # # ser2.flushInput()
                # ser2.flush()
                # int_a = int(float(str_a))
                # print("a: " + str(int_a))
                # int_b = int(float(str_b))
                # print("b: " + str(int_b))
            # # Lock conditions
            # if (int_a < 300):
            #     print("Right Side Door Unlock")
            #     if (doorUnLock == 1):
            #         ser1.write(b'0')
            #         print("Lock Command sent")
            #         doorUnLock = 0
            # elif (int_a > 300):
            #     print("Outside Unlock zone")
            #     if (doorUnLock == 0):
            #         ser1.write(b'1')
            #         print("UnLock Command sent")
            #         doorUnLock = 1
            cos_a = (int_b * int_b + int_c * int_c - int_a * int_a) / (2 * int_b * int_c)
            sin_a = math.sqrt(1 - cos_a * cos_a)
            x = int_b * cos_a
            print("X: " + str(x))
            y = int_b * sin_a
            print("Y: " + str(y))
            with open("E:\PyCharmProject\pythonProject\coords.txt", "w") as file:
                file.write(f"{int(x) * 3},{600-int(y) * 3}\n")
            if (x >= 0 and y >= 0):
                angle = math.asin(sin_a) * (180.0 / math.pi)
            if (x <= 0 and y >= 0):
                angle = 90 + (90 - math.asin(sin_a) * (180.0 / math.pi))
            print("Angle: " + str(angle) + "\n")
            # clean(t_a1)
            # clean(t_a2)
            clean(t_a3)
            # draw_uwb_anchor1(0, 0, "A1(0,0)", int_b, t_a1)
            # draw_uwb_anchor2(int_c, 0, "A2("+str(int_c)+",0)", int_a, t_a2)
            # draw_uwb_tag(x, y, "TAG("+str(round(x))+","+str(round(y))+", A:"+str(round(angle))+")", int_b, t_a3)
            draw_uwb_tag(x, y, "TAG(" + str(round(x)) + "," + str(round(y)) + "), ∠" + str(round(angle)) + ", A1 ", int_b, t_a3)
            draw_line(0, 0, x, y, color="yellow")
            draw_line(100, 0, x, y, color="yellow")
        except:
            print("not able to form Triangle \n")
            sleep(1)

        #sleep(0.1)
    #turtle.mainloop()

if __name__ == '__main__':
    main()


