from tkinter import messagebox
import os
from model import vehiculo
from conexionBD import *
os.system("cls")

def registrar_vehiculo(marca, modelo, color, placa, anio, id_usuario):
    vehiculo.Consultas.registrar_vehiculo(marca, modelo, color, placa, anio, id_usuario)
    