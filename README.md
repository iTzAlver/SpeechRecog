#	RECONOCIMIENTO DE COMANDOS

Este repositorio contiene un programa capaz de realizar señales al sistema operativo a partir de comandos mediante voz. Ha sido diseñado con objetivo de controlar un robot, manteniendo una ejecución en paralelo.  
Este modelo ha sido diseñado para Python 2.7.  

Autor: Alberto Palomo Alonso.  
Tutor: Saturnino Maldonado Bascón.  
Universidad de Alcalá de Hernares. Escuela Politécnica Superior.  


###	INSTALACIÓN DEL MODELO

	1.- Instalación:		$	git clone https://github.com/iTzAlver/SpeechRecog
					$	cd SpeechRecog/install/
					$	./installer.sh
					$	source /.bashrc

	2.- Eliminar residuos:		$	rm -r SpeechRecog

	3.- Reiniciar el sistema:	$	sudo reboot

###	EJECUCIÓN DE DEMO:

	- Ejecución simple:		$	Lola

	- Ejecución de archivo:		$	python ~/sphinx/SpeechRecog/SCRIPTS/sampler.py

Si el programa no ha recibido errores, como la detección de micrófono u otros errores posibles, recibirá el siguiente mensaje en la línea de comandos:
	==============================================================
	= Ejecutando programa...                                     =
	= Cancele la ejecucion en cualquier momento con ctrl+Z.      =
	==============================================================

### USO DE LA DEMO:

Durante la demo, todas las palabras que el sistema reconozca serán devueltas a la línea de comandos en forma de eco. Si el sistema no devuelve las palabras que usted ha pronunciado, compruebe el micrófono o refiérase a la documentación del proyecto para más información.  
Pruebe a pronunciar el siguiente conjunto de palabras:

>	Hola  
>		Respuesta: Hola, buenas, soy Lola.  
>	Uno  
>		Respuesta: Numero : 1  
>	Tres  
>		Respuesta: Numero : 13  
>	Nueve  
>		Respuesta: Numero: 139  
>	Llama  
>		Respuesta: Llamando a : 139  
>	Richard  
>		Respuesta: [Numero de Richard]  
>	Ve  
>		Cambio de estado de la máquina de estados.  
>	Cocina  
>		Respuesta: Me estoy moviendo a la cocina.  
>	Adiós  
>		Fin del programa.  

Decir números consecutivos provoca que se almacenen en el buffer, decir las palabras ‘no’ o ‘cancelar’ eliminan el número del buffer.
Si las respuestas han sido las adecuadas, significa que el sistema está listo para ser adaptado a su proyecto y utilizarse.

### ADAPTACIÓN DEL SISTEMA:

Como usuario, deberá modificar los siguientes ficheros:

	1.- Fichero de diccionario de usuario:	~/sphinx/SpeechRecog/SCRIPTS/DICT.txt
	2.- Fichero de parámetros del sistema:	~/sphinx/SpeechRecog/SCRIPTS/PARAMETERS.txt
	3.- Fichero de manejador de señales:	~/sphinx/SpeechRecog/SCRIPTS/FSMSignal.py

Como programador, deberá modificar, adicionalmente, los siguientes ficheros:

	4.- Fichero de corrección de errores:	~/sphinx/SpeechRecog/SCRIPTS/CMap.py
	5.- Fichero de diccionario del modelo:	~/.local/lib/python2.7/site-packages/pocketsphinx/models/es.dict

#### Fichero de diccionario de usuario:

En este fichero debemos de introducir las palabras [...]