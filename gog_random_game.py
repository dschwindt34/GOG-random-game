# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 19:25:40 2020

@author: Doug
"""
import sqlite3
import random
from PIL import Image
import requests
import PySimpleGUI as sg
import sys


sg.theme('DarkPurple6')

def fixTupleList(l):
    newl = []
    for row in l:
        newl.append(row[0])
    return newl


def getGameList():
    conn = sqlite3.connect('C:\ProgramData\GOG.com\Galaxy\storage\galaxy-2.0.db')
    cursor = conn.execute('''SELECT trim(trim(GamePieces.value,'{"title":"'),'"}')
                            FROM GamePieces
                            WHERE gamePieceTypeId = 42
                            AND releaseKey NOT LIKE '%generic%' ''')
    cursor2 = conn.execute('''SELECT GamePieces.value
                            FROM GamePieces
                            WHERE gamePieceTypeId = 40
                            AND releaseKey NOT LIKE '%generic%' ''')
    list1 = cursor.fetchall()
    newList1 = fixTupleList(list1)
    list2 = cursor2.fetchall()
    newList2 = fixTupleList(list2)
    combinedList = list(zip(newList1, newList2))
    conn.close()
    return combinedList


def convertToPngFromUrl(url):
    r = requests.get(url)
    with open('icon.webp', 'wb') as f:
        f.write(r.content)
    img = Image.open('icon.webp').convert('RGB')
    img.save('icon.png', 'png')


def trimIconUrl(raw):
    url = raw[165:297]
    url = url.replace('\\', '')
    return url


def printResult(res, size):
    convertToPngFromUrl(trimIconUrl(res[1]))
    str1 = "Randomly choosing from " + str(size) + " games..."
    reslayout = [[sg.Text(str1, font=('Gill Sans MT', 18))],
                 [sg.Image('icon.png'), sg.Text(res[0], font=('Gill Sans MT', 18))],
                 [sg.Exit(font=('Gill Sans MT', 14))]]
    window = sg.Window('Random Game Picker', reslayout, finalize=True,
                       element_justification='center', no_titlebar=True,
                       element_padding=(40, 20))
    window.BringToFront()
    event, values = window.read()
    if event == 'Exit':
        window.close()


def trimIconUrlCover(raw):
    url = raw[316:-2]
    url = url.replace('\\', '')
    return url


def printResultCover(res, size):
    convertToPngFromUrl(trimIconUrlCover(res[1]))
    str1 = "Randomly choosing from " + str(size) + " games..."
    reslayout = [[sg.Text(str1, font=('Gill Sans MT', 14))],
                 [sg.Text(res[0], font=('Gill Sans MT', 24))],
                 [sg.Image('icon.png')],
                 [sg.Exit(font=('Gill Sans MT', 14))]]
    window = sg.Window('Random Game Picker', reslayout, finalize=True,
                       element_justification='center', no_titlebar=True,
                       element_padding=(80, 20))
    window.BringToFront()
    event, values = window.read()
    if event == 'Exit':
        window.close()


def launchWindow():
    layout = [[sg.Text('Spin the wheel for a random game!', font=('Gill Sans MT', 18))],
              [sg.OK(font=('Gill Sans MT', 14)), sg.Cancel(font=('Gill Sans MT', 14))]]
    return sg.Window('Random Game Picker', layout, finalize=True,
                     element_justification='center', no_titlebar=True,
                     element_padding=(80, 20))


def main():
    window = launchWindow()
    window.BringToFront()
    event, values = window.read()
    window.close()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        sys.exit()
    gameList = getGameList()
    listSize = len(gameList)
    result = gameList[random.randrange(0, listSize-1)]
    printResultCover(result, listSize)


if __name__ == "__main__":
    main()
