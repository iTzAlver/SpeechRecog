#-----------------------------------------------------------------------------------------
#
#   @author         Alberto Palomo Alonso
#   @date           28/10/2020
#   @file           .py
#
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#
#   @libraries
#
#-----------------------------------------------------------------------------------------
try:
    import os
    import sys
    import signal
    import unicodedata
    import re
except:
    print("Error al importar librerias del sistema.")
    sys.exit(0)
try:
    from pocketsphinx import LiveSpeech, get_model_path
except:
    print("Error al importar liberias de pocketsphinx.")
    sys.exit(0)

raspi = False
try:
    import RPi.GPIO as GPIO
    raspi = True
except:
    print("Warning: No hay interfaz GPIO, se senaliza por consola.")
#-----------------------------------------------------------------------------------------
#
#   @parameters
#
#-----------------------------------------------------------------------------------------
try:
    param = open("PARAMETERS.txt","r")
    param.readline()
    device = ((param.readline()).split())[2]
    srate = int(((param.readline()).split())[4])
    bsize = int(((param.readline()).split())[4])
    dict_path = ((param.readline()).split())[4]
    core_mode = int(((param.readline()).split())[4])
    param.close()
except:
    print("Error al acceder al archivo PARAMETERS.txt")
    sys.exit(0)
#-----------------------------------------------------------------------------------------
#
#   @handler        ctrlc_handler()
#
#-----------------------------------------------------------------------------------------
def ctrlc_handler( signal , frame ):
    print("")
    print("\033[1;35;40m ==============================================================")
    print("\033[1;35;40m = Se ha finalizado el programa por medio de una interrupcion.=")
    print("\033[1;35;40m ==============================================================")
    print("\033[1;0;0m")
    dict_file.close()
    sys.exit(0)
    return

signal.signal(signal.SIGTSTP, ctrlc_handler)
#-----------------------------------------------------------------------------------------
#
#   @handler        exit_handler()
#
#-----------------------------------------------------------------------------------------
def exit_handler():
    print("")
    print("\033[1;35;40m ==============================================================")
    print("\033[1;35;40m = Se ha finalizado el programa por medio de un comando.      =")
    print("\033[1;35;40m ==============================================================")
    print("\033[1;0;0m")
    dict_file.close()
    sys.exit(0)
    return

signal.signal(signal.SIGTSTP, ctrlc_handler)
#-----------------------------------------------------------------------------------------
#
#   @function       elimina_tildes()
#   @ref            https://gist.github.com/victorono/7633010
#
#-----------------------------------------------------------------------------------------
def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()
#-----------------------------------------------------------------------------------------
#
#   @function       __setup()
#
#-----------------------------------------------------------------------------------------
def __setup( rate , size ):
    model_path = get_model_path()
    try:
        if(core_mode == 0):
            speech = LiveSpeech(
                verbose=False,
                sampling_rate=rate,
                buffer_size=size,
                no_search=False,
                full_utt=False,
                hmm=os.path.join(model_path, 'es-es'),
                lm=os.path.join(model_path, 'es-20k.lm.bin'),
                dic=os.path.join(model_path, 'es.dict')
                )
        else:
            speech = LiveSpeech(
                audio_device = device,
                verbose=False,
                sampling_rate=rate,
                buffer_size=size,
                no_search=False,
                full_utt=False,
                hmm=os.path.join(model_path, 'es-es'),
                lm=os.path.join(model_path, 'es-20k.lm.bin'),
                dic=os.path.join(model_path, 'es.dict')
                )
    except:
        print('Error al importar el disposivo de audio o modelos: ', device,' ', model_path)
        sys.exit(0)
    return speech
#-----------------------------------------------------------------------------------------
#
#   @function       __dicrSearch()
#
#-----------------------------------------------------------------------------------------
def __dictSearch( word , file ):
    signal_number = 1
    file.seek(0)
    for line in file:
        if(line[:-1] == word):
            return signal_number
        else:
            signal_number = signal_number + 1
    return 0
#-----------------------------------------------------------------------------------------
#
#   @function       __FSMSignal/RPI/()
#
#-----------------------------------------------------------------------------------------
def __FSMSignalRPI( signal , state , number):
    #Manejador GPIO
    return 0

def __FSMSignal( signal , state , number):
    #Manejador de estado:
    if(signal == 1 or signal==25):
        print('=== > Hola, buenas, soy Lola.')
    if(signal == 2):
        return [1, number]
    if(signal == 3):
        print('=== > Llamando a : ' + number)
    if(signal == 5):
        number = '[Numero de bernardo]'
    if(signal == 6):
        number = '[Numero de luisa]'
    if(signal == 7):
        number = '[Numero de juana]'
    if(signal == 8):
        number = '[Numero de richard]'
    if(signal == 9):
        print('=== > Que pase un buen dia.')
        exit_handler()
    if(signal >= 10 and signal <= 19):
        number = number + str(signal-10)
        print('=== > Numero : ' + number)
    if(signal == 20 or signal == 22):
        number = ''
    if(signal == 21):
        print("=== > Si?")
    if(signal == 23):
        return [2,number]
    if(signal == 24):
        return [3,number]
    # - - - - - - - - - - - - - - - - - - - - - - - -
    if(state == 1):
        if(signal == 4):
            print("=== > Me estoy moviendo a la cocina.")
    if(state == 2):
        if(signal == 4):
            print(" === > Encendiendo cocina.")
    if(state == 3):
        if(signal == 4):
            print(" === > Apagando cocina.")

    return [0, number]
#-----------------------------------------------------------------------------------------
#
#   @function       __wordHandler()
#
#-----------------------------------------------------------------------------------------
def __wordHandler( word ):
    # Lower.
    h_word = word.lower()
    h_word = elimina_tildes(h_word.decode('utf-8'))
    # HASHMAP
    #
    HMAP = {
    'buenas' : 'hola',
    'chao' : 'adios',
    'siente' : 'siete',
    'pero' : 'cero',
    'hare' : 'nueve',
    'pico' : 'cinco',
    'unos' : 'uno',
    'cinico' : 'cinco',
    'diana' : 'llama',
    'mueren' : 'nueve',
    'bernard' : 'bernardo',
    'muere' : 'nueve',
    'acaba' : 'apaga',
    'muevete' : 've',
    'cortina' : 'cocina',
    'acabar' : 'apagar'
    }
    #
    #
    h_word = HMAP.get(h_word, h_word)
    return h_word
#-----------------------------------------------------------------------------------------
#
#   @main
#
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    #   Console interface.
    print("\033[1;33;40m")
    print("\033[1;33;40m ==============================================================")
    print("\033[1;33;40m = Ejecutando LOLA speech recognition.                        =")
    print("\033[1;33;40m = Autor: Alberto Palomo Alonso.                              =")
    print("\033[1;33;40m ==============================================================")
    print("\033[1;33;40m")
    print("\033[1;31;40m ==============================================================")
    print("\033[1;31;40m = Cargando modelo ...                                        =")
    speech = __setup(srate, bsize)
    print("\033[1;31;40m = Cargado el modelo.                                         =")
    print("\033[1;31;40m ==============================================================")
    print("\033[1;33;40m")
    print("\033[1;33;40m ==============================================================")
    print("\033[1;33;40m = Abriendo diccionario...                                    =")
    try:
        dict_file = open(dict_path, "r")
    except:
        print("Error al abrir el archivo DICT.txt")
        sys.exit(0)
    print("\033[1;33;40m = Diccionario abierto.                                       =")
    print("\033[1;33;40m ==============================================================")
    print("\033[1;33;40m")
    print("\033[1;33;40m ==============================================================")
    print("\033[1;33;40m = Ejecutando programa...                                     =")
    print("\033[1;33;40m = Cancele la ejecucion en cualquier comento con ctrl+Z.      =")
    print("\033[1;33;40m ==============================================================")
    print("\033[1;31;40m")
    #   Computing loop:
    state = 0
    number = ''
    for phrase in speech:
        print(phrase)
        words = str(phrase).split()
        for word in words:
            mysignal = __dictSearch(__wordHandler(word), dict_file)
            if(mysignal > 0):
                if(raspi == True):
                    [state, number] = __FSMSignalRPI(mysignal, state, number)
                else:
                    [state, number] = __FSMSignal(mysignal, state, number)
#-----------------------------------------------------------------------------------------
#
#   @endfile
#
#-----------------------------------------------------------------------------------------
