#-----------------------------------------------------------------------------------------
#
#   @function       __FSMSignal/RPI/()
#
#-----------------------------------------------------------------------------------------
def __FSMSignalRPI( signal , state , number):
    #Manejador GPIO
    return [0, number]

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
        return [-1,number]
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

