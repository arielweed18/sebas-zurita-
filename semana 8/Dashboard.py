import threading
import time

def tarea_hilo(identificador, delay):
    for i in range(5):
        print(f'Hilo {identificador}: Realizando tarea {i}')
        time.sleep(delay)

hilo1 = threading.Thread(target=tarea_hilo, args=(1, 1))
hilo2 = threading.Thread(target=tarea_hilo, args=(2, 0.8))
hilo3 = threading.Thread(target=tarea_hilo, args=(3, 1.2))

hilo1.start()
hilo2.start()
hilo3.start()

hilo1.join()
hilo2.join()
hilo3.join()

print('Programa principal: Todas las tareas han sido completadas.')

# Mantener la ventana activa 10 segundos
time.sleep(10)
