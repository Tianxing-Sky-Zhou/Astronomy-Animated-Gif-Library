# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 16:21:32 2024

@author: Daniel
"""
import numpy as np
import pandas as pd
import os
import shutil
import math
from os import listdir
from os.path import isfile, join

PATH = "./"
NAME_COL = 0
DIS_NAME_COL = 1
CH_COL = 2
SRC_COL = 3
IMAGES_COL = 4
SUP_COL = 5
TAG_START = 6
N_CHAPTERS = 30;

def readDataFile():
    dataFileName = 'gif_data.csv'
    file = pd.read_csv(dataFileName, keep_default_na=False)
    file['chapter(int)'] = pd.to_numeric(file['chapter(int)'], errors='coerce').fillna(0).astype(int)
    return file.values.tolist()

def listChapterGifs(data):
    content = '<ul> \n'
    
    for i in range(len(data)):
        name = data[i][NAME_COL]
        disName = data[i][DIS_NAME_COL]
        chapter = data[i][CH_COL]
        
        content = content + '<li> \n'
        content = content + '<a href="../animations/' + name + '.gif" target="_blank"> \n'
        content = content + '<img src="../animations/' + name + '.gif" alt="clickableimage" width="124" height="70">\n'
        content = content + '</a>  <span style="font-weight:normal">' + disName + '</span> \n </li> \n'
    
    content = content + '</ul> \n'
                    
    return content

def updateChapters(data):
    
    dataByChapter = []
    
    for i in range(N_CHAPTERS):
        gifsForChapter = []
        
        for j in range(len(data)):
            if data[j][CH_COL] == (i +1):
                gifsForChapter.append(data[j])
        
        dataByChapter.append(gifsForChapter)
    
    for i in range(N_CHAPTERS):
        content = listChapterGifs(dataByChapter[i])
        
        
        fileName = PATH + 'gifs_chapter/chapter_' + str(i+1) + '.html' 
        htmlFile = ('<!DOCTYPE html> \n <html lang="en"> \n <head> \n <title>AAGL-Ch.' + str(i+1) + '</title>\n' 
        +'<meta charset="utf-8"> \n <meta name="viewport" content="width=device-width, initial-scale=1"> \n' + 
            '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> \n' +
            '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script> \n' + 
            '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> \n' + 
            '<style> \n .navbar { \n margin-bottom: 0; \n border-radius: 0; \n } \n /* Set height of the grid so .sidenav can be 100% (adjust as needed) */ \n' + 
            '.row.content { \n height: 850px \n } \n' + 
            '.sidenav { \n padding-top: 20px; \n background-color: #f1f1f1; \n height: 100%; \n } \n' + 
            'footer { \n background-color: #555; \n color: white; \n padding: 15px; \n } \n' + 
            '/* On small screens, set height to ''auto'' for sidenav and grid */ \n @media screen and (max-width: 767px) { \n' +
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
            '<li> \n' +
            '<a class="btn btn-secondary dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> \n' +
            'Gif Library \n' +
            '</a> \n' +
            '<ul class="dropdown-menu"> \n' +
            '<li><a href="chapter_1.html">Chapter 1: Science and the Universe</a></li> \n' +
            '<li><a href="chapter_2.html">Chapter 2: Observing the Sky</a></li> \n' +
            '<li><a href="chapter_3.html">Chapter 3: Orbits & Gravity</a></li> \n' +
            '<li><a href="chapter_4.html">Chapter 4: Earth, Moon, & Sky</a></li> \n' +
            '<li><a href="chapter_5.html">Chapter 5: Radiation & Spectra</a></li> \n' +
            '<li><a href="chapter_6.html">Chapter 6: Astronomical Instraments</a></li> \n' +
            '<li><a href="chapter_7.html">Chapter 7: Other Worlds</a></li> \n' +
            '<li><a href="chapter_8.html">Chapter 8: Earth</a></li> \n' +
            '<li><a href="chapter_9.html">Chapter 9: Cratered Worlds</a></li> \n' +
            '<li><a href="chapter_10.html">Chapter 10: Venus & Mars</a></li> \n' +
            '<li><a href="chapter_11.html">Chapter 11: Giant Planets</a></li> \n' +
            '<li><a href="chapter_12.html">Chapter 12: Rings, Moons, & Pluto</a></li> \n' +
            '<li><a href="chapter_13.html">Chapter 13: Coments & Asteroids</a></li> \n' +
            '<li><a href="chapter_14.html">Chapter 14: Solar System Origins</a></li> \n' +
            '<li><a href="chapter_15.html">Chapter 15: The Sun - Classification</a></li> \n' +
            '<li><a href="chapter_16.html">Chapter 16: The Sun - Energy</a></li> \n' +
            '<li><a href="chapter_17.html">Chapter 17: Starlight</a></li> \n' +
            '<li><a href="chapter_18.html">Chapter 18: The Stars</a></li> \n' +
            '<li><a href="chapter_19.html">Chapter 19: Distances</a></li> \n' +
            '<li><a href="chapter_20.html">Chapter 20: Gas & Dust</a></li> \n' +
            '<li><a href="chapter_21.html">Chapter 21: Exoplanets</a></li> \n' +
            '<li><a href="chapter_22.html">Chapter 22: Lifecycle of Stars</a></li> \n' +
            '<li><a href="chapter_23.html">Chapter 23: Death of Stars</a></li> \n' +
            '<li><a href="chapter_24.html">Chapter 24: Black Holes</a></li> \n' +
            '<li><a href="chapter_25.html">Chapter 25: The Milky Way</a></li> \n' +
            '<li><a href="chapter_26.html">Chapter 26: Galaxies</a></li> \n' +
            '<li><a href="chapter_27.html">Chapter 27: Active Galaxies</a></li> \n' +
            '<li><a href="chapter_28.html">Chapter 28: Galactic Evolution</a></li> \n' +
            '<li><a href="chapter_29.html">Chapter 29: The Big Bang</a></li> \n' +
            '<li><a href="chapter_30.html">Chapter 30: Life in the Univers</a></li> \n' +
    
            '</ul> \n' +
            '</li> \n' +
            '<li><a href="../gif_index.html">Index</a></li> \n' +
            '<li><a href="../file_list.html">File List</a></li> \n' +
            '</ul> \n' +
    
            '</div> \n' +
            '</div> \n' +
            '</nav> \n' +
    
            '<div class="container-fluid text-center"> \n' +
            '<div class="row content"> \n' +
            '<div class="col-sm-2 sidenav"> \n' +
            '<p><a href="#">Link</a></p> \n' +
            '<p><a href="#">Link</a></p> \n' +
            '<p><a href="#">Link</a></p> \n' +
            '</div> \n' +
            '<div class="col-sm-8 text-left"> \n' +
            
            ###Body of page
            '<h1>Chapter ' + str(i+1) + ' Gifs</h1> \n' + content + 
    
            '</div> \n' +
            '<div class="col-sm-2 sidenav"> \n' +
            '<div class="well"> \n' +
            '<p>ADS</p> \n' +
            '</div> \n' +
            '<div class="well"> \n' +
            '<p>ADS</p> \n' +
            '</div> \n' +
            '</div> \n' +
            '</div> \n' +
            '</div> \n' +
    
            '<footer class="container-fluid text-center"> \n' +
            '<p>Footer Text</p> \n' +
            '</footer> \n' +
    
            '</body> \n' +
            '</html> \n')
        
        print(fileName)
        file = open(fileName,'w+')
        file.write(htmlFile)
        file.close()

def makeIndex(data):
    index = dict()
    
    for i in range(len(data)):
        line = data[i]
        
        for j in range(TAG_START,len(line)):
            tag = line[j]
            tag = str(tag).strip()
            if not tag:
                continue
            tag = tag.capitalize()
            
            if tag not in index.keys():
                tagInstances = [i]
            else:
                tagInstances = index.get(tag)
                tagInstances.append(i)
            
            index.update({tag:tagInstances})
    
    index = dict(sorted(index.items()))
    content = '<ul> \n'
    
    for key in index:
        lineNumbers = index.get(key)
        
        sortedLineNumbers = []
        
        for lineNumber in lineNumbers:
            name = data[lineNumber][NAME_COL]
            sortedLineNumbers.append([name,lineNumber])
        
        sortedLineNumbers = sorted(sortedLineNumbers)
        
        content = content + '<li>' + key + '\n' + '<ul> \n'
        
        for i in range(len(sortedLineNumbers)):
            lineNumber = sortedLineNumbers[i][1]
            row = data[lineNumber]
            name = row[NAME_COL]
            disName = row[DIS_NAME_COL]
            chapter = row[CH_COL]
            
            content = content + '<li>\n'
            content = content + '<a href="gifs_chapter/chapter_' + str(chapter) + '/' + name + '/' + name + '.gif" target="_blank">' + disName + '</a> \n' 
            content = content + '</li>\n'
        
        content = content + '</ul>\n </li> \n'
    
    
    content = content + '</ul> \n'
    
    return content

def updateIndex(data):
        
    fileName = PATH + 'gif_index' + '.html' 
    content = makeIndex(data)
    
    htmlFile = ('<!DOCTYPE html> \n <html lang="en"> \n <head> \n <title>AAGL-Index' + '</title>\n' 
    +'<meta charset="utf-8"> \n <meta name="viewport" content="width=device-width, initial-scale=1"> \n' + 
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> \n' +
        '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script> \n' + 
        '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> \n' + 
        '<style> \n .navbar { \n margin-bottom: 0; \n border-radius: 0; \n } \n /* Set height of the grid so .sidenav can be 100% (adjust as needed) */ \n' + 
        '.row.content { \n height: 850px \n } \n' + 
        '.sidenav { \n padding-top: 20px; \n background-color: #f1f1f1; \n height: 100%; \n } \n' + 
        'footer { \n background-color: #555; \n color: white; \n padding: 15px; \n } \n' + 
        '/* On small screens, set height to ''auto'' for sidenav and grid */ \n @media screen and (max-width: 767px) { \n' +
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
        '<img src="images/haumea.jpg" class="rounded float-left" alt="haumea" height="50" width="50"> \n' +
        '</div> \n' +
        '<div class="collapse navbar-collapse" id="myNavbar"> \n' +
        '<ul class="nav navbar-nav"> \n' +
        '<li><a href="index.html">Home</a></li> \n' +
        '<li> \n' +
        '<a class="btn btn-secondary dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> \n' +
        'Gif Library \n' +
        '</a> \n' +
        '<ul class="dropdown-menu"> \n' +
        '<li><a href="gifs_chapter/chapter_1.html">Chapter 1: Science and the Universe</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_2.html">Chapter 2: Observing the Sky</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_3.html">Chapter 3: Orbits & Gravity</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_4.html">Chapter 4: Earth, Moon, & Sky</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_5.html">Chapter 5: Radiation & Spectra</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_6.html">Chapter 6: Astronomical Instraments</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_7.html">Chapter 7: Other Worlds</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_8.html">Chapter 8: Earth</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_9.html">Chapter 9: Cratered Worlds</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_10.html">Chapter 10: Venus & Mars</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_11.html">Chapter 11: Giant Planets</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_12.html">Chapter 12: Rings, Moons, & Pluto</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_13.html">Chapter 13: Coments & Asteroids</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_14.html">Chapter 14: Solar System Origins</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_15.html">Chapter 15: The Sun - Classification</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_16.html">Chapter 16: The Sun - Energy</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_17.html">Chapter 17: Starlight</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_18.html">Chapter 18: The Stars</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_19.html">Chapter 19: Distances</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_20.html">Chapter 20: Gas & Dust</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_21.html">Chapter 21: Exoplanets</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_22.html">Chapter 22: Lifecycle of Stars</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_23.html">Chapter 23: Death of Stars</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_24.html">Chapter 24: Black Holes</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_25.html">Chapter 25: The Milky Way</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_26.html">Chapter 26: Galaxies</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_27.html">Chapter 27: Active Galaxies</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_28.html">Chapter 28: Galactic Evolution</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_29.html">Chapter 29: The Big Bang</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_30.html">Chapter 30: Life in the Univers</a></li> \n' +

        '</ul> \n' +
        '</li> \n' +
        '<li class="active"><a href="gif_index.html">Index</a></li> \n' +
        '<li><a href="file_list.html">File List</a></li> \n' +
        '</ul> \n' +

        '</div> \n' +
        '</div> \n' +
        '</nav> \n' +

        '<div class="container-fluid text-center"> \n' +
        '<div class="row content"> \n' +
        '<div class="col-sm-2 sidenav"> \n' +
        '<p><a href="#">Link</a></p> \n' +
        '<p><a href="#">Link</a></p> \n' +
        '<p><a href="#">Link</a></p> \n' +
        '</div> \n' +
        '<div class="col-sm-8 text-left"> \n' +
        
        ###Body of page
        '<h1>Gif Index</h1> \n' + content + 

        '</div> \n' +
        '<div class="col-sm-2 sidenav"> \n' +
        '<div class="well"> \n' +
        '<p>ADS</p> \n' +
        '</div> \n' +
        '<div class="well"> \n' +
        '<p>ADS</p> \n' +
        '</div> \n' +
        '</div> \n' +
        '</div> \n' +
        '</div> \n' +

        '<footer class="container-fluid text-center"> \n' +
        '<p>Footer Text</p> \n' +
        '</footer> \n' +

        '</body> \n' +
        '</html> \n')
        
    file = open(fileName,'w+')
    file.write(htmlFile)
    file.close()

def makeFileStructure(data):
    fileListByChapters = []
    
    for i in range(N_CHAPTERS):
        chapterData = []
        for j in range(len(data)):
            if data[j][CH_COL] == i + 1:
                name = data[j][NAME_COL]
                chapterData.append([name,j])
        
        chapterData = sorted(chapterData)
        fileListByChapters.append(chapterData)

    content = '<ul> \n'
    for i in range(N_CHAPTERS):
        content = content + '<li>' + 'Chapter ' + str(i+1) + '\n'
        content = content + '<ul> \n'
        chapterData = fileListByChapters[i]
        
        for j in range(len(chapterData)):
            row = data[chapterData[j][1]]
            name = row[NAME_COL]
            disName = row[DIS_NAME_COL]
            chapter = row[CH_COL]
            sourceCode = row[SRC_COL]
            images = row[IMAGES_COL]
            additional = row[SUP_COL]
            tags = []
            for k in range(TAG_START, len(row)):
                tag = str(row[k]).strip()
                if not tag:
                    continue
                tags.append(tag.capitalize())
            
            tags = sorted(tags)
            
            content = content + '<li>' + disName + '\n'
            content = content + '<ul>\n'
            
            content = content + '<li>\n'
            content = content + '<a href="animations/' + name + '.gif" target="_blank">' + name + '.gif</a> \n'
            content = content + '</li>\n'
            
            if sourceCode == 'y':
                content = content + '<li>\n'
                content = content + '<a href="gifs_chapter/chapter_' + str(chapter) + '/' + name + '/' + name + '_src.py" target="_blank">' + 'Source Code' + '</a> \n'
                content = content + '</li>\n'
            
            if images == 'y':
                content = content + '<li>\n'
                content = content + '<a href="https://github.com/danielkj28/Astronomy-Animated-Gif-Library/tree/main/gifs_chapter/chapter_' + str(chapter) + '/' + name + '/' + name + '_images/" target="_blank">' + 'Generating Images' + '</a> \n'
                content = content + '</li>\n'
            
            if additional == 'y':
                content = content + '<li>\n'
                content = content + '<a href="https://github.com/danielkj28/Astronomy-Animated-Gif-Library/tree/main/gifs_chapter/chapter_' + str(chapter) + '/' + name + '/' + name + '_additional/" target="_blank">' + 'Additional Materials' + '</a> \n'
                content = content + '</li>\n'
            
            content = content + '<li>\n'
            content = content + 'Tags: '
            for k in range(len(tags)-1):
                content = content + tags[k] + ', '
            
            content = content + tags[-1] + '\n'
            content = content + '</li>\n'
            
            content = content + '</ul>\n'
            content = content + '</li> \n'
        
        content = content + '</ul> \n'
        content = content + '</li> \n'
    
    content = content + '</ul> \n'
    
    return content
    

def updateFileList(data):
    fileName = PATH + 'file_list' + '.html' 
    content = makeFileStructure(data)
    
    htmlFile = ('<!DOCTYPE html> \n <html lang="en"> \n <head> \n <title>AAGL-Files' + '</title>\n' 
    +'<meta charset="utf-8"> \n <meta name="viewport" content="width=device-width, initial-scale=1"> \n' + 
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> \n' +
        '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script> \n' + 
        '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> \n' + 
        '<style> \n .navbar { \n margin-bottom: 0; \n border-radius: 0; \n } \n /* Set height of the grid so .sidenav can be 100% (adjust as needed) */ \n' + 
        '.row.content { \n height: 850px \n } \n' + 
        '.sidenav { \n padding-top: 20px; \n background-color: #f1f1f1; \n height: 100%; \n } \n' + 
        'footer { \n background-color: #555; \n color: white; \n padding: 15px; \n } \n' + 
        '/* On small screens, set height to ''auto'' for sidenav and grid */ \n @media screen and (max-width: 767px) { \n' +
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
        '<img src="images/haumea.jpg" class="rounded float-left" alt="haumea" height="50" width="50"> \n' +
        '</div> \n' +
        '<div class="collapse navbar-collapse" id="myNavbar"> \n' +
        '<ul class="nav navbar-nav"> \n' +
        '<li><a href="index.html">Home</a></li> \n' +
        '<li> \n' +
        '<a class="btn btn-secondary dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> \n' +
        'Gif Library \n' +
        '</a> \n' +
        '<ul class="dropdown-menu"> \n' +
        '<li><a href="gifs_chapter/chapter_1.html">Chapter 1: Science and the Universe</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_2.html">Chapter 2: Observing the Sky</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_3.html">Chapter 3: Orbits & Gravity</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_4.html">Chapter 4: Earth, Moon, & Sky</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_5.html">Chapter 5: Radiation & Spectra</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_6.html">Chapter 6: Astronomical Instraments</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_7.html">Chapter 7: Other Worlds</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_8.html">Chapter 8: Earth</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_9.html">Chapter 9: Cratered Worlds</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_10.html">Chapter 10: Venus & Mars</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_11.html">Chapter 11: Giant Planets</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_12.html">Chapter 12: Rings, Moons, & Pluto</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_13.html">Chapter 13: Coments & Asteroids</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_14.html">Chapter 14: Solar System Origins</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_15.html">Chapter 15: The Sun - Classification</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_16.html">Chapter 16: The Sun - Energy</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_17.html">Chapter 17: Starlight</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_18.html">Chapter 18: The Stars</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_19.html">Chapter 19: Distances</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_20.html">Chapter 20: Gas & Dust</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_21.html">Chapter 21: Exoplanets</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_22.html">Chapter 22: Lifecycle of Stars</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_23.html">Chapter 23: Death of Stars</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_24.html">Chapter 24: Black Holes</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_25.html">Chapter 25: The Milky Way</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_26.html">Chapter 26: Galaxies</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_27.html">Chapter 27: Active Galaxies</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_28.html">Chapter 28: Galactic Evolution</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_29.html">Chapter 29: The Big Bang</a></li> \n' +
        '<li><a href="gifs_chapter/chapter_30.html">Chapter 30: Life in the Univers</a></li> \n' +

        '</ul> \n' +
        '</li> \n' +
        '<li><a href="gif_index.html">Index</a></li> \n' +
        '<li class="active"><a href="file_list.html">File List</a></li> \n' +
        '</ul> \n' +

        '</div> \n' +
        '</div> \n' +
        '</nav> \n' +

        '<div class="container-fluid text-center"> \n' +
        '<div class="row content"> \n' +
        '<div class="col-sm-2 sidenav"> \n' +
        '<p><a href="#">Link</a></p> \n' +
        '<p><a href="#">Link</a></p> \n' +
        '<p><a href="#">Link</a></p> \n' +
        '</div> \n' +
        '<div class="col-sm-8 text-left"> \n' +
        
        ###Body of page
        '<h1>All Files</h1> \n' + content + 

        '</div> \n' +
        '<div class="col-sm-2 sidenav"> \n' +
        '<div class="well"> \n' +
        '<p>ADS</p> \n' +
        '</div> \n' +
        '<div class="well"> \n' +
        '<p>ADS</p> \n' +
        '</div> \n' +
        '</div> \n' +
        '</div> \n' +
        '</div> \n' +

        '<footer class="container-fluid text-center"> \n' +
        '<p>Footer Text</p> \n' +
        '</footer> \n' +

        '</body> \n' +
        '</html> \n')
        
    file = open(fileName,'w+')
    file.write(htmlFile)
    file.close()

def main():
    print('main')
    gif_data = readDataFile()
    updateChapters(gif_data)
    updateIndex(gif_data)
    updateFileList(gif_data)


if __name__ == "__main__":
    main()
