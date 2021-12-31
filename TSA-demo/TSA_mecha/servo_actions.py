def initialAvaIntroServo(stop):
    # AVA moving head
    while True:
        lock.acquire()
        kit.servo[10].angle = 120
        time.sleep(3)
        if stop():
            lock.release()
            print('getting a stop thread for initialAvaIntroServo')
            break
        kit.servo[10].angle = 105
        time.sleep(3)
        if stop():
            lock.release()
            print('getting a stop thread for initialAvaIntroServo')
            break
        kit.servo[10].angle = 90
        time.sleep(3)
        if stop():
            lock.release()
            print('getting a stop thread for initialAvaIntroServo')
            break
        kit.servo[10].angle = 75
        time.sleep(3)
        if stop():
            lock.release()
            print('getting a stop thread for initialAvaIntroServo')
            break
        kit.servo[10].angle = 60
        time.sleep(3)
        if stop():
            lock.release()
            print('getting a stop thread for initialAvaIntroServo')
            break
        kit.servo[10].angle = 90
        time.sleep(3)
        lock.release()
        if stop():
            print('getting a stop thread for initialAvaIntroServo')
            break



def myNameisAvaServo(stop):
    #left hand hi movement
    lock.acquire()
    kit.servo[3].angle = 120
    time.sleep(0.2)
    kit.servo[3].angle = 90
    time.sleep(0.2)
    kit.servo[3].angle = 70
    time.sleep(0.2)
    kit.servo[3].angle = 40
    time.sleep(3)
    kit.servo[3].angle = 70
    time.sleep(0.2)
    kit.servo[3].angle = 90
    time.sleep(0.2)
    kit.servo[3].angle = 120
    time.sleep(0.2)
    kit.servo[3].angle = 180
    time.sleep(2)
    lock.release()
    if stop():
        print('getting a stop thread for myNameisAvaServo')

        
def Avadoyouhavequestion(stop):
    #eyemovement
    lock.acquire()
    kit.servo[8].angle = 120
    time.sleep(2)
    kit.servo[8].angle = 90
    time.sleep(2)
    lock.release()
    if stop():
        print('getting a stop thread for Avadoyouhavequestion')

def checkAgentontheright():
    #righthandmovement
    lock.acquire()
    kit.servo[13].angle = 90
    time.sleep(2)
    kit.servo[13].angle = 0
    time.sleep(2)
    lock.release()

def avagoodbye(stop):
    #left hand hi movement
    lock.acquire()
    kit.servo[13].angle = 120
    time.sleep(0.2)
    kit.servo[12].angle = 90
    time.sleep(0.2)
    kit.servo[3].angle = 70
    time.sleep(0.2)
    kit.servo[3].angle = 40
    time.sleep(3)
    kit.servo[3].angle = 70
    time.sleep(0.2)
    kit.servo[3].angle = 90
    time.sleep(0.2)
    kit.servo[3].angle = 120
    time.sleep(0.2)
    kit.servo[3].angle = 180
    time.sleep(2)
    lock.release()
    if stop():
        print('getting a stop thread for myNameisAvaServo')