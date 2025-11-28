from tkinter import messagebox
import os
from model import usuario
from conexionBD import *
os.system("cls")


def registrar_usuario(nombre, apellido_paterno, apellido_materno, tipo,estado):
    usuario.Consultas.registrar_usuario(nombre, apellido_paterno, apellido_materno, tipo,estado)