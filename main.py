import os
import re
import shutil
import tkinter as tk
from datetime import datetime

import pandas as pd
import wget
from PIL import Image as im, ImageTk as imtk

DISEASE = 'Alzheimer'  # choose disease
FILE = 'Genes_list_all'  # choose input file name
URL = 'https://pubmed.ncbi.nlm.nih.gov/?term='
GENE = 'gene'
WIDTH = 900
HEIGHT = 600


def initialize():
    """Create or remove folders and files"""
    if os.path.exists('local'):
        shutil.rmtree('local')
    os.mkdir('local')
    if os.path.exists('results.csv'):
        os.remove('results.csv')
    if os.path.exists('failed.txt'):
        os.remove('failed.txt')


def read_elements():
    """Read list of elements, replace each space with a plus"""
    elements = []
    for line in open(FILE + '.txt', 'r'):
        elements += [line.strip().replace(' ', '+')]
    return elements


def search2(element, option):
    """Find number of results of a PubMed search, use quotes in the search"""
    title = element + '' + DISEASE + '' + option
    wget.download(URL + '"' + element + '+' + 'gene' + '"+' + option + '+"' + DISEASE + '"', 'local/' + title + '.html')
    os.system('find "Quoted phrase not found" local/' + title + '.html >local/file')
    f = open('local/file', 'r')
    f.readline()
    f.readline()
    line_check_not_found = f.readline()
    if line_check_not_found == '':  # no results found
        os.system('find "data-results-amount" local/' + title + '.html >local/file')
        f = open('local/file', 'r')
        f.readline()
        f.readline()
        line = f.readline()
        if line == '':  # no results found
            result = '0'
        else:
            result = line.split('=')[1].replace(',', '').replace('"', '')[:-1]
    else:
        result = '0'
    f.close()
    return result


def search(element, option):
    """Find number of results of a PubMed search, use quotes in the search"""
    title = element + '_' + DISEASE + '_' + option
    wget.download(URL + '"' + element + '"+' + option + '+"' + DISEASE + '"', 'local/' + title + '.html')
    os.system('find "Quoted phrase not found" local/' + title + '.html >local/file')
    f = open('local/file', 'r')
    f.readline()
    f.readline()
    line_check_not_found = f.readline()
    if line_check_not_found == '':  # no results found
        os.system('find "data-results-amount" local/' + title + '.html >local/file')
        f = open('local/file', 'r')
        f.readline()
        f.readline()
        line = f.readline()
        if line == '':  # no results found
            result = '0'
        else:
            result = line.split('=')[1].replace(',', '').replace('"', '')[:-1]
    else:
        result = '0'

    f.close()
    return result


def sortExel():
    pass
    # DataFrame to read our input CS file
    dataFrame = pd.read_csv("results.csv")
    # print("\nInput CSV file = \n", dataFrame)

    # sorting according to multiple columns
    dataFrame.sort_values(" Association", axis=0, ascending=False, inplace=True, na_position='first')
    x = DISEASE.replace("+", " ")
    print(
        "\nSorted CSV file (according to multiple columns) =\n(For Analysis Of Association between  \"" + x +
        "\" Disease to Genes.)\n\n",
        dataFrame)
    dataFrame.to_csv('results.csv', index=False)


def main():
    global DISEASE
    x1 = entry1.get()
    if x1:
        DISEASE = x1.replace(" ", "+")
    else:
        pass
    genesFromBox = box.get(1.0, "end-1c")
    element = re.split(',|, | |\n', genesFromBox)
    # save time
    start = datetime.now()
    # create folders
    initialize()

    if genesFromBox:
        elements = element
    else:
        elements = read_elements()

    counter = 0  # count number of elements for terminal print
    file_out = open('results.csv', 'a')
    file_out.write('Gene, AND, OR, Association\n')  # print titles to Excel
    failed = open('failed.txt', 'a')

    for element in elements:
        counter += 1
        try:
            and_result = search2(element, 'AND')

            if and_result != '0':
                or_result = search2(element, 'OR')
                association = str((int(and_result) / int(or_result)) * 100)

            else:  # no need to count or_result if and_result is zero because association is zero anyway
                or_result = '-'
                association = '0'

            file_out.write(element + ',' + and_result + ',' + or_result + ',' + association + '\n')  # print to Excel
            print('\n' + str(counter) + ': ' + element + '\nAND = %-*s OR = %s' % (
                7, and_result, or_result))  # print to terminal

        except:  # save failed elements - need to run them again
            failed.write(element + '\n')
            print('\n' + str(counter) + ': ' + element + '\nfailed')  # print to terminal
            pass

    print('\nRun Time:', datetime.now() - start)

    file_out.close()
    failed.close()
    sortExel()

    # label1 = tk.Label(window, text="DONE! you can see the output in the excel result")
    # canvas1.create_window(WIDTH / 2, HEIGHT / 1.4, window=label1)

    load1 = im.open("./pic/Untitled_Artwork_1.png")
    resize1 = load1.resize((int(89 * 2.5), int(32 * 2.5)), im.ANTIALIAS)
    img1 = imtk.PhotoImage(resize1)
    label1 = tk.Label(window, image=img1, borderwidth=0, compound="center", highlightthickness=0)
    label1.anchor = img1
    canvas1.create_window(WIDTH / 1.18, HEIGHT / 1.4, window=label1)


window = tk.Tk()
window.title('G.D')
# Add icon:
bg = tk.PhotoImage(file="./pic/new icon.png")
window.iconphoto(False, bg)
# continue with the rest of the labels:
greeting = tk.Label(text="Hello, Welcome to Genes Vs Disease ", font=('Gautami', 10))
greeting.pack()
canvas1 = tk.Canvas(window, width=WIDTH, height=HEIGHT)
canvas1.pack(fill="both", expand=True)
# set background color !
canvas1.configure(bg='#060020')
# Display image
# canvas1.create_image(0, 0, image=bg,
# anchor="nw")
# add a photo:
load_big_logo = im.open("./pic/logo_good.jpg")
# resize the size of the photo
resizeP = load_big_logo.resize((int(410 * 1.3), int(190 * 1.3)), im.ANTIALIAS)
img_big_logo = imtk.PhotoImage(resizeP)
label = tk.Label(image=img_big_logo, borderwidth=0, compound="center", highlightthickness=0)
label.image = img_big_logo
# place of the photo
label.place(x=40, y=27)

load2 = im.open("./pic/Untitled_Artwork_3.png")
resizeP = load2.resize((int(360 / 1.8), int(40 / 1.8)), im.ANTIALIAS)
img2 = imtk.PhotoImage(resizeP)
label2 = tk.Label(image=img2, borderwidth=0, compound="center", highlightthickness=0)
label2.place(x=WIDTH / 3.15, y=HEIGHT / 2.4)

entry1 = tk.Entry(window, width=30, font=('Gill Sans MT', 14))
canvas1.create_window(WIDTH / 2, HEIGHT / 2.2, window=entry1)

load3 = im.open("./pic/Untitled_Artwork_2.png")
resizeP = load3.resize((int(390 * 1.4), int(40 * 1.4)), im.ANTIALIAS)
img3 = imtk.PhotoImage(resizeP)
label3 = tk.Label(image=img3, borderwidth=0, compound="center", highlightthickness=0)
canvas1.create_window(WIDTH / 2, HEIGHT / 1.78, window=label3)

box = tk.Text(window, width=35, height=4, font=('Gill Sans MT', 14))
canvas1.create_window(WIDTH / 2, HEIGHT / 1.4, window=box)
# box.pack()
# Import the image using PhotoImage function

# Import the image using PhotoImage function
load_b = im.open("./pic/analyze.jpeg")
resizeP_b = load_b.resize((int(145 * 0.9), int(40 * 0.9)), im.ANTIALIAS)
click_btn = imtk.PhotoImage(resizeP_b)
# Let us create a dummy button and pass the image
button = tk.Button(window, image=click_btn, command=main,
                   borderwidth=0, compound="center", highlightthickness=0, highlightbackground="#060020",
                   activebackground='#060020')
canvas1.create_window(WIDTH / 2, HEIGHT / 1.15, window=button)

# Import the image using PhotoImage function
load_o = im.open("pic/new_quit.jpeg")
resizeP_o = load_o.resize((int(70 * 0.9), int(40 * 0.9)), im.ANTIALIAS)
qu = imtk.PhotoImage(resizeP_o)
# Let us create a dummy button and pass the image
buttonExit = tk.Button(window, image=qu, command=window.destroy,
                       borderwidth=0, compound="center", highlightthickness=0, highlightbackground="#060020",
                       activebackground='#060020')
canvas1.create_window(WIDTH / 2, HEIGHT / 1.07, window=buttonExit)

"""
# button1 = tk.Button(text='Analyze it', command=main, font=('Cambria', 14, 'bold' ))
# canvas1.create_window(WIDTH / 2, HEIGHT / 1.1, window=button1)
buttonExit = tk.Button(window, text="Quit", command=window.destroy, font=('Cambria', 13, 'bold'))
canvas1.create_window(WIDTH / 1.6, HEIGHT / 1.1, window=buttonExit)
"""
load3 = im.open("./pic/Untitled_Artwork_2.png")
resizeP = load3.resize((int(390 * 1.4), int(40 * 1.4)), im.ANTIALIAS)
img3 = imtk.PhotoImage(resizeP)
label3 = tk.Label(image=img3, borderwidth=0, compound="center", highlightthickness=0)
canvas1.create_window(WIDTH / 2, HEIGHT / 1.78, window=label3)

window.mainloop()

if __name__ == '__main__':
    main()
