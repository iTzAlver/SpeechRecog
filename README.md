#	RECONOCIMIENTO DE COMANDOS

Este repositorio contiene un programa capaz de realizar señales al sistema operativo a partir de comandos mediante voz. Ha sido diseñado con objetivo de controlar un robot, manteniendo una ejecución en paralelo.  
Este modelo ha sido diseñado para Python 2.7.  

>Autor: Alberto Palomo Alonso.  
>Tutor: Saturnino Maldonado Bascón.  
>Universidad de Alcalá de Hernares. Escuela Politécnica Superior.  


###	1.- INSTALACIÓN DEL MODELO

	1.- Instalación:		$	git clone https://github.com/iTzAlver/SpeechRecog
					$	cd SpeechRecog/install/
					$	./installer.sh
					$	source /.bashrc

	2.- Eliminar residuos:		$	rm -r SpeechRecog

	3.- Reiniciar el sistema:	$	sudo reboot

###	2.- EJECUCIÓN DE DEMO:

	- Ejecución simple:		$	Lola

	- Ejecución de archivo:		$	python ~/sphinx/SpeechRecog/SCRIPTS/sampler.py

Si el programa no ha recibido errores, como la detección de micrófono u otros errores posibles, recibirá el siguiente mensaje en la línea de comandos:

>	Ejecutando programa...         
>	Cancele la ejecucion en cualquier momento con ctrl+Z.      

### 3.- USO DE LA DEMO:

Durante la demo, todas las palabras que el sistema reconozca serán devueltas a la línea de comandos en forma de eco. Si el sistema no devuelve las palabras que usted ha pronunciado, compruebe el micrófono o refiérase a la documentación del proyecto para más información.  
Pruebe a pronunciar el siguiente conjunto de palabras:

>	-	Hola  
		     Respuesta: Hola, buenas, soy Lola.  
>	-	Uno  
		     Respuesta: Numero : 1  
>	-	Tres  
		     Respuesta: Numero : 13  
>	-	Nueve  
		     Respuesta: Numero: 139  
>	-	Llama  
		     Respuesta: Llamando a : 139  
>	-	Richard  
		     Respuesta: [Numero de Richard]  
>	-	Ve  
		     Cambio de estado de la máquina de estados.  
>	-	Cocina  
		     Respuesta: Me estoy moviendo a la cocina.  
>	-	Adiós  
		     Fin del programa.  

Decir números consecutivos provoca que se almacenen en el buffer, decir las palabras ‘no’ o ‘cancelar’ eliminan el número del buffer.
Si las respuestas han sido las adecuadas, significa que el sistema está listo para ser adaptado a su proyecto y utilizarse.

### 4.- ADAPTACIÓN DEL SISTEMA:

Como usuario, deberá modificar los siguientes ficheros:

	1.- Fichero de diccionario de usuario:	~/sphinx/SpeechRecog/SCRIPTS/DICT.txt
	2.- Fichero de parámetros del sistema:	~/sphinx/SpeechRecog/SCRIPTS/PARAMETERS.txt
	3.- Fichero de manejador de señales:	~/sphinx/SpeechRecog/SCRIPTS/FSMSignal.py

Como programador, deberá modificar, adicionalmente, los siguientes ficheros:

	4.- Fichero de corrección de errores:	~/sphinx/SpeechRecog/SCRIPTS/CMap.py
	5.- Fichero de diccionario del modelo:	~/.local/lib/python2.7/site-packages/pocketsphinx/models/es.dict

#### 4.1.- Fichero de diccionario de usuario:

Existen dos tipos de señales:  

-	**Señales internas:** Son las señales que genera el sistema (sampler.py) hacia el manejador de señales en función de la palabra reconocida.  
-	**Señales del sistema:** Son las señales que genera el manejador de señal hacia el sistema operativo en función de la acción asociada.  

En este fichero debemos de introducir las palabras que queremos que se traduzcan a señales internas. Por lo que todas las palabras que queremos reconocer deben de estar incluidas en este diccionario con el siguiente formato:

	*	Sin acento.
	*	En minúsculas.
	*	Sin espacios.
	*	Sin ningún tipo de carácter que no sea una letra.
	*	Con retorno de carro al final de cada línea.

Cabe destacar que para que la palabra sea reconocida, debe de estar también incluida en el diccionario del modelo (contiene 20.000 palabras en castellano).

#### 4.2.- Fichero de parámetros del sistema:

El sistema tiene varios parámetros modificables y son los siguientes:

	1.- Dispositivo:		Es el micrófono a utilizar, esto es útil únicamente si existen varios micrófonos conectados al dispositivo. Sólo se tiene en cuenta si el modo del núcleo es 1.
	2.- Frecuencia de muestreo: 	Frecuencia a la que se extraen las muestras del audio. El valor óptimo en una Raspberry es de 3200.
	3.- Tamaño del buffer:		Tamaño del buffer de audio. El valor óptimo en una Raspberry es de 2048 ó 1024.
	4.- Path del diccionario:	Ubicación del diccionario de usuario en el sistema de archivos, puede modificarse la ruta del mismo, aunque no se recomienda.
	5.- Modo del núcleo:		Modo de reconocimiento de dispositivo en el kernel. Si si valor es 0, utilizará el dispositivo predeterminado por ALSA; si su valor es 1, utilizará el dispositivo con el índice del valor que esté puesto en 'Dispositivo'.
	6.- Forzar línea de comandos:	Escoge la función del manejador de señales.
		*	Si el valor es 1: El manejador de señales utilizará la función __FSMSignal() forzosamente. Además, se mostrarán las palabras que se reconozcan mediante la línea de comandos.  
					  **El valor 1 corresponde por defecto a la DEMO.**  
		*	Si el valor es 0: El manejador de señales escogería la función __FSMSignal() si el dispostivo NO es un Raspbian y usará la función __FSMSignalRPI() si SÍ nos econtramos en un Raspbian. Además, se desactivará el eco de las palabras reconocidas en la línea de comandos.

#### 4.3.- Fichero de manejador de señales:

El manejador de señales, traduce las señales recibidas por los scripts (señales internas) en señales al sistema operativo (señales del sistema). Estas funciones debe definirlas el usuario, dado que existe un amplio abanico de posibilidades al usuario de mandar señales, generar máquinas de estados y muchas más cosas que no dependen del sistema de reconocimiento de audio y sí dependen de parámetros como en qué lenguaje está escrito el programa principal o qué sistema operativo se está ejecutando.  
Existen dos funciones principales:

	*	__FSMSignalRPI():	Esta se ejecuta cuando estamos en Raspbian y el valor 'Forzar línea de comandos' del fichero de parámetros del sistema vale 0.
	*	__FSMSignal():		Esta se ejecuta cuando NO estamos en Raspbian y el valor 'Forzar línea de comandos' del fichero de parámetros del sistema vale 1.

Sea cual sea la función que querramos utilizar, aquí debe de ir el código que el usuario debe de desarollar. Las posibilidades que existen para mandar señales por el sistema operativo son las siguientes:

	*	Señales de procesos. (cualquier lenguaje)
	*	Tuberías del sistema operativo. (cualquier lenguaje)
	*	Librerías como 'multiprocessing', 'zmq' y otras. (python en cualquier versión)
	*	Cualquier comunicación manual desarollada por el usuario. (cualquier lenguaje)
	*	Implementación directa de código sobre la función. (sólo python 2.7)

Estas funciones contienen dos variables importantes, AMBAS DEBEN DE SER DEVUELTAS AL SCRIPT PRINCIPAL CON UN RETURN [state,number]:

	*	state:	Estado de la máquina de estados, en caso de que el usuario quiera desarollarla. Si se devuelve -1 al script principal, este termina la ejecución del programa.
	*	number:	Buffer en forma de string. En caso de que el usuario necesite un buffer.


__NOTA IMPORTANTE: Para determinar si estamos en Raspbian, se importa la librería RPiGPIO de Python, que viene por defecto instalada en Raspbian. Si esta se instala en otro sistema operativo, será evaluado como Raspbian.__

#### 4.4.- Fichero de corrección de errores:

