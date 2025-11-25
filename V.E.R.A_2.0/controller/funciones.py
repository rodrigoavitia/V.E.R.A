from tkinter import messagebox
import os
from model import consultas
from conexionBD import *
os.system("cls")




def registrar_admin(nombre, apellido_paterno, apellido_materno, mail, password, estado):
    consultas.Consultas.registrar_admin(nombre, apellido_paterno, apellido_materno, mail, password, estado)


def registrar_usuario(nombre, apellido_paterno, apellido_materno, tipo,estado):
    consultas.Consultas.registrar_usuario(nombre, apellido_paterno, apellido_materno, tipo,estado)

def registrar_vehiculo(marca, modelo, color, placa, anio, id_usuario):
    consultas.Consultas.registrar_vehiculo(marca, modelo, color, placa, anio, id_usuario)

def registrar_imagenes(imagen, tipo, fecha, hora):
    consultas.Consultas.registrar_imagenes(imagen, tipo, fecha, hora)
