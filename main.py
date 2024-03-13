import numpy as np
from tkinter import *
from tkinter import messagebox

# Функция для вычисления критерия Хи-квадрат
def chi_squared_test(sequence):
    observed = np.array([len([bit for bit in sequence if bit == 0]), len([bit for bit in sequence if bit == 1])])
    expected = np.array([len(sequence) / 2, len(sequence) / 2])
    chi2 = sum((observed - expected)**2 / expected)
    return chi2

# Генерация псевдослучайной последовательности с использованием LFSR-генератора и комбинирования LFSR-генераторов
def lfsr_generator(seed, taps):
    state = seed
    while True:
        new_bit = state[0]
        for t in taps:
            new_bit ^= state[t]
        state = state[1:] + [new_bit]
        yield new_bit

# Полиномиальное комбинирование LFSR-генераторов
def polynomial_combination(x, polynomials):
    result = 0
    for polynomial in polynomials:
        result ^= polynomial(x)
    return result

# Полиномиалы для генераторов
def polynomial1(x):
    return x[6] ^ x[3] ^ 1

def polynomial2(x):
    return x[6] ^ x[2] ^ x[1] ^ 1

def polynomial3(x):
    return x[6] ^ x[1] ^ 1

# Функция для вставки данных из файла
def insert_data_from_file():
    try:
        with open('input.txt', 'r') as file:
            input_data = file.readlines()
            height_tf.insert(0, input_data[0].strip())
            weight_tf.insert(0, input_data[1].strip())
    except FileNotFoundError:
        messagebox.showerror('Error', 'File not found')

# Функция для вычисления и отображения результатов
def calculate_main():
    seed1 = int(height_tf.get())
    taps1 = int(weight_tf.get())
    seed = [int(x) for x in str(seed1)]  # Начальное состояние регистра
    taps = [int(x) for x in str(taps1)]  # Положение обратных связей

    lfsr = lfsr_generator(seed, taps)

    generated_sequence = [next(lfsr) for _ in range(10)]
    print("Сгенерированная последовательность:", generated_sequence)

    state_history = []
    while True:
        state = tuple(seed)
        if state in state_history:
            period = len(state_history) - state_history.index(state)
            break
        state_history.append(state)
        next_bit = next(lfsr)
        seed = seed[1:] + [next_bit]

    print("Период сгенерированной последовательности:", period)

    chi2_value = chi_squared_test(generated_sequence)
    print("Значение критерия χ²-Пирсона для сгенерированной последовательности:", chi2_value)

    messagebox.showinfo('output',f'Сгенерированная последовательность: {generated_sequence}\n Период: {period}\n Значение χ²-Пирсона: {chi2_value}')

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(f"Сгенерированная последовательность: {generated_sequence}\n")
        f.write(f"Период: {period}\n")
        f.write(f"Значение критерия χ²-Пирсона: {chi2_value}\n")

# Создание и настройка GUI
window = Tk()
window.title('Генератор чисел')
window.geometry('700x450')

frame = Frame(
    window,
    padx=10,
    pady=10
)
frame.pack(expand=True)

height_lb = Label(
    frame,
    text="Введите seed"
)
height_lb.grid(row=3, column=1)

weight_lb = Label(
    frame,
    text="Введите taps",
)
weight_lb.grid(row=4, column=1)

height_tf = Entry(
    frame,
)
height_tf.grid(row=3, column=2, pady=5)

weight_tf = Entry(
    frame,
)
weight_tf.grid(row=4, column=2, pady=5)

cal_btn = Button(
    frame,
    text='Сгенерировать последовательность',
    command=calculate_main
)
cal_btn.grid(row=5, column=2)

cal_btn = Button(
    frame,
    text='Вставить данные из файла',
    command=insert_data_from_file
)
cal_btn.grid(row=5, column=1)

window.mainloop()