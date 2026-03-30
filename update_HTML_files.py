# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 16:21:32 2024

@author: Daniel
"""
import pandas as pd
from pathlib import Path

PATH = "./"
NAME_COL = 0
DIS_NAME_COL = 1
FILE_NAME_COL = 2
CH_COL = 3
SRC_COL = 4
IMAGES_COL = 5
SUP_COL = 6
TAG_START = 7
N_CHAPTERS = 30
ANIM_DIR = Path("animations")

def gif_exists(row):
    filename = str(row[FILE_NAME_COL]).strip()
    if not filename:
        return False
    return (ANIM_DIR / filename).exists()

def readDataFile():
    dataFileName = 'gif_data.csv'
    file = pd.read_csv(dataFileName, keep_default_na=False)
    file['chapter(int)'] = pd.to_numeric(file['chapter(int)'], errors='coerce').fillna(0).astype(int)
    return file.values.tolist()

def gif_filename(row):
    filename = str(row[FILE_NAME_COL]).strip()
    if filename:
        return filename
    return "__MISSING__.gif"

def source_folder_name(row):
    return str(row[NAME_COL]).strip()

def listChapterGifs(data):
    content = '<ul> \n'
    for row in data:
        disName = row[DIS_NAME_COL]
        filename = gif_filename(row)

        content += '<li> \n'
        if gif_exists(row):
            content += f'<a href="../animations/{filename}" target="_blank"> \n'
            content += f'<img src="../animations/{filename}" alt="clickableimage" width="124" height="70">\n'
            content += f'</a>  <span style="font-weight:normal">{disName}</span> \n'
        else:
            content += f'<span style="font-weight:normal">{disName} (GIF missing)</span> \n'
        content += '</li> \n'

    content += '</ul> \n'
    return content

def updateChapters(data):
    dataByChapter = [[] for _ in range(N_CHAPTERS)]
    for row in data:
        ch = row[CH_COL]
        if 1 <= ch <= N_CHAPTERS:
            dataByChapter[ch-1].append(row)

    for i in range(N_CHAPTERS):
        content = listChapterGifs(dataByChapter[i])
        fileName = PATH + f'gifs_chapter/chapter_{i+1}.html'
        htmlFile = ('<!DOCTYPE html> \n <html lang="en"> \n <head> \n <title>AAGL-Ch.' + str(i+1) + '</title>\n'
        +'<meta charset="utf-8"> \n <meta name="viewport" content="width=device-width, initial-scale=1"> \n' +
            '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> \n' +
            '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script> \n' +
            '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> \n' +
            '<style> \n .navbar { \n margin-bottom: 0; \n border-radius: 0; \n } \n' +
            '.row.content { \n height: 850px \n } \n' +
            '.sidenav { \n padding-top: 20px; \n background-color: #f1f1f1; \n height: 100%; \n } \n' +
            'footer { \n background-color: #555; \n color: white; \n padding: 15px; \n } \n' +
            '@media screen and (max-width: 767px) { \n' +
            '.sidenav { \n height: auto; \n padding: 15px; \n } \n' +
            '.row.content { \n height: auto; \n } \n .dropdown-toggle { \n text-align: left \n } \n} \n </style> \n </head> \n <body> \n' +
            '<nav class="navbar navbar-inverse"> \n' +
            '<div class="container-fluid"> \n' +
            '<div class="navbar-header"> \n' +
            '<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar"> \n' +
            '<span class="icon-bar"></span> \n' +
            '<span class="icon-bar"></span> \n' +
            '<span class="icon-bar"></span> \n' +
            '</button> \n' +
            '<img src="../images/haumea.jpg" class="rounded float-left" alt="haumea" height="50" width="50"> \n' +
            '</div> \n' +
            '<div class="collapse navbar-collapse" id="myNavbar"> \n' +
            '<ul class="nav navbar-nav"> \n' +
            '<li><a href="../index.html">Home</a></li> \n' +
            '<li><a href="../gif_index.html">Index</a></li> \n' +
            '<li><a href="../file_list.html">File List</a></li> \n' +
            '</ul> \n' +
            '</div> \n' +
            '</div> \n' +
            '</nav> \n' +
            '<div class="container-fluid text-center"> \n' +
            '<div class="row content"> \n' +
            '<div class="col-sm-2 sidenav"></div> \n' +
            '<div class="col-sm-8 text-left"> \n' +
            '<h1>Chapter ' + str(i+1) + ' Gifs</h1> \n' + content +
            '</div> \n' +
            '<div class="col-sm-2 sidenav"></div> \n' +
            '</div> \n' +
            '</div> \n' +
            '<footer class="container-fluid text-center"> \n' +
            '<p>Footer Text</p> \n' +
            '</footer> \n' +
            '</body> \n' +
            '</html> \n')
        with open(fileName, 'w+', encoding='utf-8') as file:
            file.write(htmlFile)

def makeIndex(data):
    index = {}
    for i, line in enumerate(data):
        for j in range(TAG_START, len(line)):
            tag = str(line[j]).strip()
            if not tag:
                continue
            tag = tag.capitalize()
            index.setdefault(tag, []).append(i)

    content = '<ul> \n'
    for key in sorted(index.keys()):
        lineNumbers = index[key]
        sortedLineNumbers = sorted(lineNumbers, key=lambda idx: gif_filename(data[idx]).lower())
        content += '<li>' + key + '\n<ul> \n'
        for lineNumber in sortedLineNumbers:
            row = data[lineNumber]
            disName = row[DIS_NAME_COL]
            filename = gif_filename(row)
            content += '<li>\n'
            if gif_exists(row):
                content += f'<a href="animations/{filename}" target="_blank">{disName}</a> \n'
            else:
                content += f'{disName} (GIF missing)\n'
            content += '</li>\n'
        content += '</ul>\n </li> \n'
    content += '</ul> \n'
    return content

def updateIndex(data):
    fileName = PATH + 'gif_index.html'
    content = makeIndex(data)
    htmlFile = ('<!DOCTYPE html> \n <html lang="en"> \n <head> \n <title>AAGL-Index</title>\n'
    +'<meta charset="utf-8"> \n <meta name="viewport" content="width=device-width, initial-scale=1"> \n' +
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> \n' +
        '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script> \n' +
        '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> \n' +
        '<style> \n .navbar { \n margin-bottom: 0; \n border-radius: 0; \n } \n .row.content { \n height: 850px \n } \n' +
        '.sidenav { \n padding-top: 20px; \n background-color: #f1f1f1; \n height: 100%; \n } \n' +
        'footer { \n background-color: #555; \n color: white; \n padding: 15px; \n } \n' +
        '@media screen and (max-width: 767px) { \n.sidenav { \n height: auto; \n padding: 15px; \n } \n.row.content { \n height: auto; \n } \n .dropdown-toggle { \n text-align: left \n } \n} \n </style> \n </head> \n <body> \n' +
        '<nav class="navbar navbar-inverse"> \n' +
        '<div class="container-fluid"> \n' +
        '<div class="navbar-header"> \n' +
        '<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar"> \n' +
        '<span class="icon-bar"></span> \n' +
        '<span class="icon-bar"></span> \n' +
        '<span class="icon-bar"></span> \n' +
        '</button> \n' +
        '<img src="images/haumea.jpg" class="rounded float-left" alt="haumea" height="50" width="50"> \n' +
        '</div> \n' +
        '<div class="collapse navbar-collapse" id="myNavbar"> \n' +
        '<ul class="nav navbar-nav"> \n' +
        '<li><a href="index.html">Home</a></li> \n' +
        '<li class="active"><a href="gif_index.html">Index</a></li> \n' +
        '<li><a href="file_list.html">File List</a></li> \n' +
        '</ul> \n' +
        '</div> \n' +
        '</div> \n' +
        '</nav> \n' +
        '<div class="container-fluid text-center"> \n' +
        '<div class="row content"> \n' +
        '<div class="col-sm-2 sidenav"></div> \n' +
        '<div class="col-sm-8 text-left"> \n' +
        '<h1>Gif Index</h1> \n' + content +
        '</div> \n' +
        '<div class="col-sm-2 sidenav"></div> \n' +
        '</div> \n' +
        '</div> \n' +
        '<footer class="container-fluid text-center"> \n' +
        '<p>Footer Text</p> \n' +
        '</footer> \n' +
        '</body> \n' +
        '</html> \n')
    with open(fileName, 'w+', encoding='utf-8') as file:
        file.write(htmlFile)

def makeFileStructure(data):
    fileListByChapters = [[] for _ in range(N_CHAPTERS)]
    for j, row in enumerate(data):
        if row[CH_COL] == 0:
            continue
        if 1 <= row[CH_COL] <= N_CHAPTERS:
            fileListByChapters[row[CH_COL]-1].append([gif_filename(row), j])

    content = '<ul> \n'
    for i in range(N_CHAPTERS):
        content += '<li>Chapter ' + str(i+1) + '\n'
        content += '<ul> \n'
        chapterData = sorted(fileListByChapters[i], key=lambda x: x[0].lower())

        for _, rowIndex in chapterData:
            row = data[rowIndex]
            name = source_folder_name(row)
            disName = row[DIS_NAME_COL]
            chapter = row[CH_COL]
            sourceCode = row[SRC_COL]
            images = row[IMAGES_COL]
            additional = row[SUP_COL]
            filename = gif_filename(row)

            tags = []
            for k in range(TAG_START, len(row)):
                tag = str(row[k]).strip()
                if tag:
                    tags.append(tag.capitalize())
            tags = sorted(tags)

            content += '<li>' + disName + '\n'
            content += '<ul>\n'
            content += '<li>\n'
            if gif_exists(row):
                content += f'<a href="animations/{filename}" target="_blank">{filename}</a> \n'
            else:
                content += f'{filename} (GIF missing)\n'
            content += '</li>\n'
            if sourceCode == 'y':
                content += f'<li>\n<a href="gifs_chapter/chapter_{chapter}/{name}/{name}_src.py" target="_blank">Source Code</a> \n</li>\n'
            if images == 'y':
                content += f'<li>\n<a href="gifs_chapter/chapter_{chapter}/{name}/{name}_images/" target="_blank">Generating Images</a> \n</li>\n'
            if additional == 'y':
                content += f'<li>\n<a href="gifs_chapter/chapter_{chapter}/{name}/{name}_additional/" target="_blank">Additional Materials</a> \n</li>\n'
            if tags:
                content += '<li>\nTags: ' + ', '.join(tags) + '\n</li>\n'

            content += '</ul>\n'
            content += '</li> \n'
        content += '</ul> \n'
        content += '</li> \n'
    content += '</ul> \n'
    return content

def updateFileList(data):
    fileName = PATH + 'file_list.html'
    content = makeFileStructure(data)
    htmlFile = ('<!DOCTYPE html> \n <html lang="en"> \n <head> \n <title>AAGL-Files</title>\n'
    +'<meta charset="utf-8"> \n <meta name="viewport" content="width=device-width, initial-scale=1"> \n' +
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> \n' +
        '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script> \n' +
        '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> \n' +
        '<style> \n .navbar { \n margin-bottom: 0; \n border-radius: 0; \n } \n .row.content { \n height: 850px \n } \n' +
        '.sidenav { \n padding-top: 20px; \n background-color: #f1f1f1; \n height: 100%; \n } \n' +
        'footer { \n background-color: #555; \n color: white; \n padding: 15px; \n } \n' +
        '@media screen and (max-width: 767px) { \n.sidenav { \n height: auto; \n padding: 15px; \n } \n.row.content { \n height: auto; \n } \n .dropdown-toggle { \n text-align: left \n } \n} \n </style> \n </head> \n <body> \n' +
        '<nav class="navbar navbar-inverse"> \n' +
        '<div class="container-fluid"> \n' +
        '<div class="navbar-header"> \n' +
        '<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar"> \n' +
        '<span class="icon-bar"></span> \n' +
        '<span class="icon-bar"></span> \n' +
        '<span class="icon-bar"></span> \n' +
        '</button> \n' +
        '<img src="images/haumea.jpg" class="rounded float-left" alt="haumea" height="50" width="50"> \n' +
        '</div> \n' +
        '<div class="collapse navbar-collapse" id="myNavbar"> \n' +
        '<ul class="nav navbar-nav"> \n' +
        '<li><a href="index.html">Home</a></li> \n' +
        '<li><a href="gif_index.html">Index</a></li> \n' +
        '<li class="active"><a href="file_list.html">File List</a></li> \n' +
        '</ul> \n' +
        '</div> \n' +
        '</div> \n' +
        '</nav> \n' +
        '<div class="container-fluid text-center"> \n' +
        '<div class="row content"> \n' +
        '<div class="col-sm-2 sidenav"></div> \n' +
        '<div class="col-sm-8 text-left"> \n' +
        '<h1>All Files</h1> \n' + content +
        '</div> \n' +
        '<div class="col-sm-2 sidenav"></div> \n' +
        '</div> \n' +
        '</div> \n' +
        '<footer class="container-fluid text-center"> \n' +
        '<p>Footer Text</p> \n' +
        '</footer> \n' +
        '</body> \n' +
        '</html> \n')
    with open(fileName, 'w+', encoding='utf-8') as file:
        file.write(htmlFile)

def main():
    gif_data = readDataFile()
    updateChapters(gif_data)
    updateIndex(gif_data)
    updateFileList(gif_data)

if __name__ == "__main__":
    main()