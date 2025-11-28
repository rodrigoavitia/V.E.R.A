from tkinter import messagebox
import os
from model import admin
from conexionBD import *
os.system("cls")




def registrar_admin(nombre, apellido_paterno, apellido_materno, mail, password, estado):
    admin.Consultas.registrar_admin(nombre, apellido_paterno, apellido_materno, mail, password, estado)




def registrar_vehiculo(marca, modelo, color, placa, anio, id_usuario):
    admin.Consultas.registrar_vehiculo(marca, modelo, color, placa, anio, id_usuario)

def registrar_imagenes(imagen, tipo, fecha, hora):
    admin.Consultas.registrar_imagenes(imagen, tipo, fecha, hora)
