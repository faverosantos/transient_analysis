import matplotlib.pyplot as plt
import numpy as np
#from scipy.fft import fft, fftfreq
import rflib as rf

class Defines:

    # Sampling frequency
    FS = 100*10E9

    # Sampling period
    TS = 1/FS

    # Number of samples
    N_SAMPLES = 1000



# Generates a sine wave
# Inputs: frequency (Hz), phase (rad/s), offset (V), amplitude (V), size (amount of samples)
def generate_sine_wave(frequency, phase, offset, amplitude, size):

    wa = 2 * np.pi * frequency
    wd = wa / Defines.FS

    n = np.arange(size)

    s_n = offset + amplitude*np.sin(wd * n + phase)

    return s_n

if __name__ == "__main__":

    print("Aloha!")


    # Generate the CW main signal .pwl file

    # pin in dBm
    PIN = 20

    #source resistance
    RSOURCE = 50

    mW = rf.dBm_2_mW(PIN)

    [amplitude_rms, amplitude_peak] = rf.mw_2_volts(mW, RSOURCE)

    CARRIER_FREQUENCY = 2.4E9
    PHASE = 0
    OFFSET = 0
    AMPLITUDE = amplitude_peak
    CYCLES = 40
    SIZE = int(CYCLES*np.ceil(Defines.FS/CARRIER_FREQUENCY))
    sine = generate_sine_wave(CARRIER_FREQUENCY, PHASE, OFFSET, AMPLITUDE, SIZE)

    n = np.arange(0, len(sine)) / Defines.FS
    rf.export_as_pwl("outputs/vin.pwl", n, sine)

    plt.plot(n, sine, label="vin")

    # Generate enables .pwl file

    ON = 4
    OFF = 0
    DURATION = 10

    counter = 2
    EN1 = np.zeros(len(sine))
    end = (CYCLES - counter*DURATION) * int(SIZE/CYCLES)
    init = end - DURATION * int(SIZE/CYCLES)
    EN1[init:end] = OFF
    rf.export_as_pwl("outputs/EN1.pwl", n, EN1)
    plt.plot(n, EN1, label="EN1")

    counter -= 1
    EN2 = np.zeros(len(sine))
    end = (CYCLES - counter*DURATION) * int(SIZE/CYCLES)
    init = end - DURATION * int(SIZE/CYCLES)
    EN2[init:end] = ON
    rf.export_as_pwl("outputs/EN2.pwl", n, EN2)
    plt.plot(n, EN2, label="EN2")

    counter -= 1
    EN3 = np.zeros(len(sine))
    end = (CYCLES - counter*DURATION) * int(SIZE/CYCLES)
    init = end - DURATION * int(SIZE/CYCLES)
    EN3[init:end] = ON
    rf.export_as_pwl("outputs/EN3.pwl", n, EN3)
    plt.plot(n, EN3, label="EN3")
    #plt.show()

    # Generate biasing and vdd .pwl files

    counter = 3
    VB1 = np.ones(len(sine))*0.52
    rf.export_as_pwl("outputs/VB1.pwl", n, VB1)
    plt.plot(n, VB1, label="VB1")

    counter -= 1
    VB2 = np.ones(len(sine))*4.8
    end = (CYCLES - counter*DURATION) * int(SIZE / CYCLES)
    init = end - DURATION * int(SIZE/CYCLES)
    VB2[init:] = 2
    rf.export_as_pwl("outputs/VB2.pwl", n, VB2)
    plt.plot(n, VB2, label="VB2")

    counter -= 1
    VB3 = np.ones(len(sine))*4.8
    end = (CYCLES - counter*DURATION) * int(SIZE / CYCLES)
    init = end - DURATION * int(SIZE/CYCLES)
    VB3[init:] = 2.4
    rf.export_as_pwl("outputs/VB3.pwl", n, VB3)
    plt.plot(n, VB3, label="VB3")

    counter -= 1
    VB4 = np.ones(len(sine))*4.8
    end = (CYCLES - counter*DURATION) * int(SIZE / CYCLES)
    init = end - DURATION * int(SIZE/CYCLES)
    VB4[init:] = 3.6
    rf.export_as_pwl("outputs/VB4.pwl", n, VB4)
    plt.plot(n, VB4, label="VB4")

    counter = 3
    VDD = np.ones(len(sine))*4.8
    end = (CYCLES - counter*DURATION) * int(SIZE / CYCLES)
    init = end - DURATION * int(SIZE/CYCLES)
    VDD[init:] = 2.0

    counter -= 1
    end = (CYCLES - counter*DURATION) * int(SIZE / CYCLES)
    init = end - DURATION * int(SIZE/CYCLES)
    VDD[init:] = 2.6

    counter -= 1
    end = (CYCLES - counter*DURATION) * int(SIZE / CYCLES)
    init = end - DURATION * int(SIZE/CYCLES)
    VDD[init:] = 3.2

    counter -= 1
    end = (CYCLES - counter*DURATION) * int(SIZE / CYCLES)
    init = end - DURATION * int(SIZE/CYCLES)
    VDD[init:] = 3.8
    rf.export_as_pwl("outputs/VDD.pwl", n, VDD)
    plt.plot(n, VDD, label="VDD")

    plt.legend(loc="lower right")
    plt.show()









