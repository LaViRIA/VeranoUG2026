# Simulación de dron Crazyflie con controlador en Python

Para inicio del Verano de la Ciencia UG 2026
Asesor: Dr. JP Ramírez Paredes


#------------------------------------------------------------
Es  necesario ajustar rutas de carpetas en "Controlador principal", al igual que en "Optimizador en la variable llamada comando poner ruta de mundo en webots,al igual que en yolo_detector hay que ajustar la ruta 

Se integro el uso de YOLO leyendo las fotos sacadas en cada waypoint propuesto, se cambio en la funcion de costo el tiempo por la distanica teorica que es la suma de las lineas que conectan los puntosd de los waypoints que froman la trayectoria, porque el tiempo le metia aletoriedad al sistema. 

Para correr el programa es necesario ejecutar el script llamado "Optimizador", ya sea desde la terminal o desde editor de codigo dandole play.

Se corrigieron algunos bugs relacionados con la optimizacion y la trayectoria
#------------------------------------------------------------
