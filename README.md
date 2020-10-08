# Map Tile Api

## Purpose

The purpose of this repository is to facilitate the use of custom layers on map application. It allows you to create tiles from an image. 
These tiles can then be used in the map application. They are caracterised by a level of zoom, and by x and y which represents the coordinates of the tile on the map.

## Configuration

To customize the app, you can specify the path to the image to transform into a map layer, the size of each tile, the output directory, etc.
All the configuration variables are present in the file `.env`.

## Installation

To run the application, you can use python virtual environments, which allows you to have specific version of python and specific packages dedicated to this project. 
This prevents conflicts if this version and packages are different than those presents globally on your system. 
This application uses Python 3. In order to start the project, you can run the following commands in the root of the project : 
```sh
python3 -m venv venv
source venv/bin/activate
```
The first command creates a directory `venv` that will contains version of python and all the packages and the second activates it. 
From there, you can install all the dependencies with :
```sh
pip install -r requirements.txt
```
