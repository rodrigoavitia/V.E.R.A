from tkinter import messagebox
import os
from model import imagenes
from conexionBD import *
os.system("cls")


def registrar_imagenes(imagen, tipo, fecha, hora):
    imagenes.Consultas.registrar_imagenes(imagen, tipo, fecha, hora)