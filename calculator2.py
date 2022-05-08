import tkinter as tk
import tkinter.messagebox as mb
import speech_recognition as sr
import re
from decimal import *
from tkinter import *


r = sr.Recognizer()
finish = False  # переменная окончания действия

window = tk.Tk()
window.title('calculator with \N{MICROPHONE}')
window.geometry("400x400")

'''Голосовое управление при нажатии на микрофон'''
def microphone():
    lbl_sign["text"] = "Say"
    with sr.Microphone() as source:
        print("Say")
        audio = r.listen(source)
    try:
        screen_clear()
        frm_enter.insert(tk.END, r.recognize_google(audio, language="ru-RU"))
        print(r.recognize_google(audio, language="ru-RU"))
    except sr.UnknownValueError:
        frm_enter.insert(tk.END, "Don't understand")
        print("Don't understand")
    except sr.RequestError as e:
        frm_enter.insert(tk.END, f"Mistake {e}")
        print(f"Mistake {e}")
    finally:
        calculate()
        clear()

'''Очистка экрана перед вводом новых вычислений'''
def screen_clear():
    if cb.get() == 1:
        frm_enter.delete(0, tk.END)

'''Очистка стикера справа от экрана, показывающего значки'''
def clear():
    lbl_sign["text"] = ""

'''Сообщение с выполняемыми действиями для длинных выражений, не вмещающихся в окно'''
def show_info():
    mb.showinfo("Выражение", frm_enter.get())

def sqr():
    cal = frm_enter.get()
    result = float(cal) ** 0.5
    result = round(result, 7)
    frm_enter.delete(0, tk.END)
    frm_enter.insert(tk.END, str(result))

def sqr3():
    cal = frm_enter.get()
    result = float(cal) ** (1/3)
    result = round(result, 7)
    frm_enter.delete(0, tk.END)
    frm_enter.insert(tk.END, str(result))

def x2():
    cal = frm_enter.get()
    result = float(cal) ** 2
    result = round(result, 7)
    frm_enter.delete(0, tk.END)
    frm_enter.insert(tk.END, str(result))

def convert_C_to_F():
    result = (5 / 9) * (float(frm_enter.get()) - 32)
    frm_enter.delete(0, tk.END)
    frm_enter.insert(tk.END, str(round(result, 7)))
    lbl_sign["text"] = "\N{DEGREE CELSIUS}"

def calculate():
    cal = frm_enter.get()
    if "корень из" in cal or "корень квадратный из" in cal:
        cal = cal.replace("корень из", "")
        cal = cal.replace("корень квадратный из", "")
        frm_enter.delete(0, tk.END)
        frm_enter.insert(tk.END, cal)
        sqr()
    elif "корень кубический из" in cal:
        cal = cal.replace("корень кубический из", "")
        frm_enter.delete(0, tk.END)
        frm_enter.insert(tk.END, cal)
        sqr3()
    elif "в квадрате" in cal or "во второй степени" in cal:
        cal = cal.replace("в квадрате", "")
        cal = cal.replace("во второй степени", "")
        frm_enter.delete(0, tk.END)
        frm_enter.insert(tk.END, cal)
        x2()
    elif "остаток от деления" in cal and "на" in cal:
        cal = cal.replace("остаток от деления", "")
        cal = cal.replace("на", "%")
        frm_enter.delete(0, tk.END)
        frm_enter.insert(tk.END, cal)
        return calculate()
    else:
        cal = cal.replace("х", "*")  # замена, т.к. рекогнайзер некорректно выводит знаки некоторых функций
        cal = cal.replace("Х", "*")
        cal = cal.replace("x", "*")
        cal = cal.replace(",", ".")
        cal = cal.replace("плюс", "+")
        cal = cal.replace("дробью", "/")
        frm_enter.delete(0, tk.END)
        frm_enter.insert(tk.END, cal)
        if len(cal) > 13:
            show_info()
        frm_enter.delete(0, tk.END)
        pattern = r"\b[\d]+[\.]?\d*\b|//|[+-/*%]"
        result = 0
        d = re.findall(pattern, cal)  # добавляем в список операции
        print(d)
        if len(d) > 3:  # для длинных операций используется eval. Можно и для состоящих из одной операции, но на всякий случай)
            try:
                d = " ".join(d)
                result = eval(d)
            except ZeroDivisionError:
                frm_enter.delete(0, tk.END)
                frm_enter.insert(tk.END, "/ на 0 нельзя!")
            except Exception:
                frm_enter.delete(0, tk.END)
                frm_enter.insert(tk.END, "Что-то не так!")
        else:
            operand2 = Decimal(d.pop())
            operation = d.pop()
            operand1 = Decimal(d.pop())
            if operation == '+':
                result = operand1 + operand2
            if operation == '-':
                result = operand1 - operand2
            if operation == '/':
                if operand2 == 0:
                    frm_enter.delete(0, tk.END)
                    frm_enter.insert(tk.END, "/ на 0 нельзя!")
                else:
                    result = operand1 / operand2
            if operation == '*':
                result = operand1 * operand2
            if operation == '%':
                if operand2 == 0:
                    frm_enter.delete(0, tk.END)
                    frm_enter.insert(tk.END, "/ на 0 нельзя!")
                else:
                    result = operand1 % operand2
            if operation == '//':
                if operand2 == 0:
                    frm_enter.delete(0, tk.END)
                    frm_enter.insert(tk.END, "/ на 0 нельзя!")
                else:
                    result = operand1 // operand2
        if result - int(result) > 0:
            frm_enter.insert(tk.END, str(round(result, 7)))
        else:
            frm_enter.insert(tk.END, str(int(result)))
    global finish
    finish = True

def click(text):
    if text == 'CE':
        clear()
        frm_enter.delete(0, tk.END)
    elif text in "0123456789/*-+%//.":
        global finish
        if finish:
            screen_clear()
            finish = False
        clear()
        frm_enter.insert(tk.END, text)
    elif text == '\N{MICROPHONE}':
        clear()
        microphone()
    elif text == '\N{SQUARE ROOT}':
        clear()
        sqr()
    elif text == '\N{CUBE ROOT}':
        clear()
        sqr3()
    elif text == 'x\N{Superscript Two}':
        clear()
        x2()
    elif text == '\N{Leftwards Arrow}':
        frm_enter.delete(len(frm_enter.get())-1)
    elif text == '\N{DEGREE FAHRENHEIT}-\N{DEGREE CELSIUS}':
        convert_C_to_F()
    elif text == "=":
        calculate()


buttons = (('\N{DEGREE FAHRENHEIT}-\N{DEGREE CELSIUS}', '//', '%', '\N{Leftwards Arrow}', 'CE'),
           ('7', '8', '9', '/', '\N{MICROPHONE}'),
           ('4', '5', '6', '*', 'x\N{Superscript Two}'),
           ('1', '2', '3', '-', '\N{SQUARE ROOT}'),
           ('0', '.', '=', '+', '\N{CUBE ROOT}'),
           )

frame_enter = tk.Frame()
lbl_sign = tk.Label(text='', anchor='center', font='Helvetica 20 bold', fg='red', bg='lavender', width=4)  # стикер справа от экрана, показывающий доп.инфу
frm_enter = tk.Entry(bd=4, justify='right', font='Helvetica 35 bold', )
frm_enter.grid(row=0, column=0, columnspan=5, sticky="nsew")
lbl_sign.grid(row=0, column=4, sticky="e")
frm_enter.grid(row=0, column=0, columnspan=4, sticky='nsew')

for column in range(4):
    window.columnconfigure(column, weight=1, minsize=50)
for row in range(6):
    window.rowconfigure(row, weight=1, minsize=30)

for row, line in enumerate(buttons):
    for col, button in enumerate(line):
        button = tk.Button(
            text=button,
            activebackground='yellow',
            font='Helvetica 30', width=3,
            relief='raised',
            bd=3,
            command=lambda \
                    x=button: click(x),
        )
        button.grid(row=row+1, column=col)
cb = IntVar()
check_clear = tk.Checkbutton(text='Очистка ввода',
                             font='Helvetica 12',
                             height=2, justify='right',
                             variable=cb, onvalue=1,
                             offvalue=0)  # флажок, при неактивном состоянии которого предыдущий результат остается во вводе,
                                          # при активации - результат в окне ввода обнуляется
check_clear.grid(row=6, column=3, columnspan=2)
check_clear.select()  # сразу отмечаем, чтобы меньше вопросов было)
info_lbl = tk.Label(text='Калькулятор с возможностью\nголосового ввода\n© Roman Paulouski', anchor='center', font='Helvetica 7')
info_lbl.grid(row=6, column=1, columnspan=2)
logo = tk.PhotoImage(file='calculator_icon.png')
info_lbl = tk.Label(image=logo, height=37, width=70)
info_lbl.grid(row=6, column=0)

window.mainloop()