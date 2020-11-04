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
try:
    import FSMSignal as FSMS
    import CMap as CM
except:
    print("Falta el archivo FSMSignal o CMap...")
    sys.exit(0)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#-----------------------------------------------------------------------------------------
#
#   @parameters
#
#-----------------------------------------------------------------------------------------
try:
    param = open(os.path.join(THIS_FOLDER,'PARAMETERS.txt'),"r")
    param.readline()
    device = ((param.readline()).split())[2]
    srate = int(((param.readline()).split())[4])
    bsize = int(((param.readline()).split())[4])
    dict_path = ((param.readline()).split())[4]
    core_mode = int(((param.readline()).split())[4])
    force_command = int(((param.readline()).split())[5])
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
#   @function       __wordHandler()
#
#-----------------------------------------------------------------------------------------
def __wordHandler( word ):
    # Lower.
    h_word = word.lower()
    h_word = elimina_tildes(h_word.decode('utf-8'))
    # HASHMAP
    #
    HMAP = CM.HMAP
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
        dict_file = open(os.path.join(THIS_FOLDER,dict_path), "r")
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
                if((raspi == True) and (force_command == 0)):
                    [state, number] = FSMS.__FSMSignalRPI(mysignal, state, number)
                else:
                    [state, number] = FSMS.__FSMSignal(mysignal, state, number)
                if state == -1:
                    exit_handler()
#-----------------------------------------------------------------------------------------
#
#   @endfile
#
#-----------------------------------------------------------------------------------------
