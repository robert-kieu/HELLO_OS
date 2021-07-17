# 0 -> children
# 1 -> parent
# -1 -> error

import time
import threading
import datetime
import os
from tkinter import*
from PIL import Image, ImageTk

#global variable
end_system = False
time_remaining = 0
flag_count = False
scr = Tk()
#=================

# store duration time of kid
class Duration:
    def __init__(self, F = 0, T = 0, D = 0, I = 0, S = 0):
        self.F = F
        self.T = T
        self.D = D
        self.I = I
        self.S = S

#call keylogger file
def key_logger():
    os.system('python keylog.pyw')

#read duration time from file
def read_duration(file_name):
    durations = []
    path = read_file(file_name)
    path = path.split('\n')
    #print(path)
    for element in path:
        duration = Duration()
        time = element.split(' ')
        for i in time:
            if i[0] == 'F':
                duration.F = i[1:]
            elif i[0] == 'T':
                duration.T = i[1:]
            elif i[0] == 'D':
                duration.D = i[1:]
            elif i[0] == 'I':
                duration.I = i[1:]
            elif i[0] == 'S':
                duration.S = i[1:]
        durations.append(duration)
    return durations

# define the countdown func.
# https://www.geeksforgeeks.org/how-to-create-a-countdown-timer-using-python/
def countdown(t): 
    timer = ""
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:03d}:{:02d}'.format(mins, secs)
        # print(timer, end="\r")
        time.sleep(1)
        t -= 1
    return timer

#read file
def read_file(file_name):
    file = open(file_name, 'r')
    path = ''
    for line in file:
        path += line
    file.close()
    return path

def write_file():
    file = open('time.txt', 'w')
    INPUT = box_left.get(1.0, END)
    INPUT = INPUT.strip()
    file.write(INPUT)
    file.close()

def read_children_his():
    path = read_file('log.txt')
    print(path)
    box_right.delete(1.0, END)
    box_right.insert(END, path)

#function check pwrd ( 1 paremt, 0 children, -1 aother)
def checkPassword(password):
    parent_password = read_file("parent.txt")
    if parent_password == password:
        return 1
    children_password = read_file("children.txt")
    if children_password == password:
        return 0
    else:
        return -1

def wrong_sys():
    warn = Label(scr, text = 'Wrong password', fg = '#73110a', bd = 0, bg = '#F7F7F7')
    warn.config(font = ('Arial', 8))
    warn.place(x = 360, y = 350)
    #===============================


#input function
def inputPassword():
    password = box_psw.get(1.0, END)
    password = password.rstrip()
    user = checkPassword(password)
    if user == 1:
        parent_sys()
    elif user == 0:
        child_sys()      
    else:
        wrong_sys()
        print("Password error")

#global var to storage duration
durations = read_duration('time.txt')

#trans 'hh:mm' to int(m) use for compare under
def hour_to_minute(time):
    return time.hour * 60 + time.minute

#function check what time kid can access (now or when?)
def is_in_time_active():
    active = False
    time_c = datetime.datetime.now()
    current_time = hour_to_minute(time_c)
    next_time = ''

    for i in range(len(durations)):
        time_f = datetime.datetime.strptime(durations[i].F, '%H:%M')
        time_t = datetime.datetime.strptime(durations[i].T, '%H:%M')
        time_d = durations[i].D
        time_i = durations[i].I
        time_s = durations[i].S
        time_from = hour_to_minute(time_f)
        time_to = hour_to_minute(time_t)
        if current_time >= time_from and current_time <= time_to:
            active = True
            if i < len(durations) - 1:
                t = datetime.datetime.strptime(durations[i + 1].F, '%H:%M')
                next_time = '{:02d}:{:02d}'.format(t.hour, t.minute)
            else:
                t = datetime.datetime.strptime(durations[0].F, '%H:%M')
                next_time = '{:02d}:{:02d}'.format(t.hour, t.minute)
            break
        elif current_time < time_from:
            t = datetime.datetime.strptime(durations[i].F, '%H:%M')
            next_time = '{:02d}:{:02d}'.format(t.hour, t.minute)
            break
    if next_time == '':
        t = datetime.datetime.strptime(durations[0].F, '%H:%M')
        next_time = '{:02d}:{:02d}'.format(t.hour, t.minute)

    return active, next_time, time_f, time_t, time_c, time_d, time_i, time_s

def donothing():
    pass

#parent system(when parent access system)
def parent_sys():
    global box_left
    global box_right
    global flag_count

    # while thread_countdown.is_alive():
    scr.title('Parent Program')
    scr.geometry('800x533')
    scr.iconbitmap('logo.ico')
    load = Image.open('prbkgr.png')
    render =ImageTk.PhotoImage(load)
    img = Label(scr, image = render)
    img.place(x = 0, y = 0)
    #===============================
    thread_countdown = threading.Thread(
        target=countdown,
        args=(3600, )
    )
    if flag_count == False:
        thread_countdown.start()
        flag_count = True
    print(flag_count)
    #===============================
    box_left = Text(scr, width = 30, height = 12, font = ('Arial', 16))
    box_left.place(x = 10, y = 170)
    box_right = Text(scr, width = 30, height = 12, font = ('Arial', 16))
    box_right.place(x = 425, y = 170)
    #===============================
    file = read_file('log.txt')
    box_right.insert(END, file)
    #===============================
    path = read_file('time.txt')
    box_left.insert(END, path)
    button_frame = Frame(scr).pack(side = BOTTOM)
    save_button = Button(button_frame, text = '     Save     ', font = (('Arial'),10,'bold'), bg = '#303030', fg = '#FFFFFF', command = write_file)
    save_button.place(x = 140, y = 480)
    child_his_update_button = Button(button_frame, text = '    Update    ', font = (('Arial'),10,'bold'), bg = '#303030', fg = '#FFFFFF', command = read_children_his)
    child_his_update_button.place(x = 570, y = 480)
    #===============================
    if thread_countdown.is_alive():
        mainloop()

def check_count():
    # delay in I minute
    if not thread_countdown.is_alive():
        t = time_i/60
        warn = Label(scr, text = '\nTime to relax is: %s minute' %(t), fg = '#000000', bd = 0, bg = '#FFDB83')
        warn.config(font = ('Arial', 40))
        warn.pack(fill = 'both', expand = True)

#children system
def child_sys():
    global end_system
    global time_remaining
    global thread_countdown
    global time_i

    scr.title('Children Program')
    scr.geometry('800x533')
    scr.iconbitmap('logo.ico')
    load = Image.open('cbkgr.png')
    render =ImageTk.PhotoImage(load)
    img = Label(scr, image = render)
    img.place(x = 0, y = 0)
    #===============================
    box_search = Text(scr, width = 30, height = 1, font = ('Arial', 16))
    box_search.place(x = 220, y = 319)
    #===============================
    in_active_time, next_time, time_from, time_to, current_time, time_d, time_i, time_s = is_in_time_active()
    time_remaining = int(time_s)
    time_s = int(time_s)*60
    time_i = int(time_i)*60
    time_d = int(time_d)*60
    if in_active_time:
        print("Hello children")
        time_can_access = hour_to_minute(time_to)*60 - hour_to_minute(current_time)*60
        if time_can_access > time_s and time_s != 0: time_can_access = time_s
        if time_d < time_s: time_can_access = time_d

        thread_countdown = threading.Thread(
            target=countdown,
            args=(time_can_access, )
        )
        #call keylogger
        keylog_thread = threading.Thread(target=key_logger)

        
        thread_countdown.start()
        keylog_thread.start()
        #===============================
        button_frame = Frame(scr).pack(side = BOTTOM)
        search_button = Button(button_frame, text = '   Go   ', font = (('Arial'),10,'bold'), bg = '#303030', fg = '#FFFFFF', command = check_count)
        search_button.place(x = 580, y = 319)
        #===============================
        if thread_countdown.is_alive():
            mainloop()     
        # ============================
        # count = 0
        # while count < 3 and not end_system:
        #     password_input = inputPassword()
        #     user = checkPassword(password_input)
        #     if user == 0:
        #         end_system = False
        #         time_remaining -= time_d/60
        #         print('Time remaining to access is: ', time_remaining, 'minute')
        #         print('Time to active again is: ', next_time)
        #         break
        #     count += 1
        # if time_remaining <= 0: end_system = True
        # if count >= 3:
        #     t = 600
        #     while t > 0:
        #         mins, secs = divmod(t, 60)
        #         timer = '{:02d}:{:02d}'.format(mins, secs)
        #         print('Sleeping: ', timer, end="\r")
        #         time.sleep(1)
        #         t -= 1

    else:
        warn = Label(scr, text = '\nTime to active is: %s' %(next_time), fg = '#000000', bd = 0, bg = '#FFDB83')
        warn.config(font = ('Arial', 40))
        warn.pack(fill = 'both', expand = True)
        #print('\nTime to active is: ', next_time)
        t = 15
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        warn2 = Label(scr, text = '\nTime to close is: %s' %(timer), fg = '#000000', bd = 0, bg = '#FFDB83')
        warn2.config(font = ('Arial', 20))
        warn2.place(x = 250, y = 320)
        mainloop()
        return

#main function
if __name__ == "__main__":


    scr.title('Hello OS')
    scr.geometry('800x533')
    scr.iconbitmap('logo.ico')
    load = Image.open('bkgr.png')
    render =ImageTk.PhotoImage(load)
    img = Label(scr, image = render)
    img.place(x = 0, y = 0)

    box_psw = Text(scr, width = 20, height = 1, font = ('Arial', 16))
    box_psw.place(x = 280, y = 319)
    button_frame = Frame(scr).pack(side = BOTTOM)

    login_button = Button(button_frame, text = '   Go   ', font = (('Arial'),10,'bold'), bg = '#303030', fg = '#FFFFFF', command = inputPassword)
    login_button.place(x = 500, y = 319)

mainloop()