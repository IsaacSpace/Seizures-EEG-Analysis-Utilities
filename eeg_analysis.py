import numpy
import pyedflib 
import scipy.signal as sp
import matplotlib.pyplot as plt

def read_edf(filename):
    """
    La función read_edf utiliza la biblioteca pyedflib para leer los datos de un 
    archivo EDF (European Data Format) que se encuentra en la ruta especificada.

    Parámetros:
        filename: el nombre del archivo EDF que se desea leer.
    Salida:
        eeg_data: una matriz numpy de datos EEG con forma (rows, columns), 
        donde rows es el número de muestras en el archivo EDF y 
        columns es el número de electrodos en el archivo EDF.
        electrodes_names: una lista de cadenas que contiene los 
        nombres de los electrodos en el archivo EDF. La longitud
        de esta lista es igual a columns.
    """
    f = pyedflib.EdfReader(filename)
    electrodes_names = f.getSignalLabels()
    rows = f.getNSamples()[0]
    columns = len(f.getSignalLabels())
    eeg_data = numpy.zeros(shape=(rows, columns))
    for j in range(0, columns, 1):
        eeg_data[:, j] = f.readSignal(j)
    return eeg_data, electrodes_names


def butterworth_filter(eeg_signal, low_freq, high_freq, sampling_freq, order):
    """
    Aplica un filtro Butterworth de orden N a una señal EEG multi-entrada dada.

    Parameters:
        eeg_signal: una matriz numpy que representa los datos de señal EEG que se desean filtrar.
        low_freq: la frecuencia de corte inferior (en Hz) para el filtro Butterworth.
        high_freq: la frecuencia de corte superior (en Hz) para el filtro Butterworth.
        sampling_freq: la frecuencia de muestreo (en Hz) de la señal EEG.
        order: el orden del filtro Butterworth.
    Returns:
        filtered_signal: una matriz numpy que representa los datos de 
        señal EEG filtrados con el filtro Butterworth especificado.
    """
    b, a = sp.butter(N=order, Wn= [low_freq, high_freq], btype="band", fs=sampling_freq)
    return sp.filtfilt(b, a, eeg_signal)

def plot_all_electrodes(eeg_signal, sampling_freq, savefig = True, fname="electrodes"):
    """
    Traza los datos de señal EEG de todos los electrodos utilizando la paquetería
    matplotlib.

    Parameters:
        eeg_signal: una matriz numpy que representa los datos de señal EEG que se desean trazar.
        sampling_freq: la frecuencia de muestreo (en Hz) de la señal EEG.
        savefig: un indicador booleano que indica si se debe guardar la figura 
        trazada en un archivo (valor predeterminado: True).
        fname: una cadena que representa el nombre del archivo en el que se 
        debe guardar la figura trazada (valor predeterminado: "electrodes").
    """
    fig = plt.figure(figsize=(10,10))
    gs = fig.add_gridspec(23, hspace=0)
    axs = gs.subplots(sharex=True, sharey=True)
    samples, electrodes = eeg_signal.shape
    time = numpy.arange(0, samples, 1) * (1/sampling_freq)
    for i in range(0, electrodes, 1):
        axs[i].plot(time, eeg_signal[:, i], color="black")
    if(savefig == True):
        plt.savefig("{}.pdf".format(fname))
    plt.show()

def correlation_matrix(eeg_signal):
    """
    Calcula la matriz de correlación entre los electrodos de los datos de 
    señal EEG dados como entrada.

    Parámetros:
        eeg_signal: una matriz numpy que representa los datos de señal 
        EEG para los cuales se desea calcular la matriz de correlación.
    Returns:
        Una matriz numpy que representa la matriz de correlación entre los electrodos.
        La matriz de correlación es una matriz cuadrada, en la que la entrada [i,j] es 
        la correlación entre los electrodos i y j. Cada fila y columna de la matriz 
        representa un electrodo. La diagonal de la matriz se establece en cero, ya que 
        la correlación de un electrodo consigo mismo siempre es 1 y, por lo tanto, 
        no es útil en la matriz de correlación.
    """
    rows, columns = eeg_signal.shape 
    cor_matrix = numpy.zeros(shape=(columns, columns))
    for i in range(0, columns, 1):
        for j in range(0, columns, 1):
            cor_matrix[i, j] = numpy.correlate(eeg_signal[:, i], eeg_signal[:, j])
            if(i == j):
                cor_matrix[i, j] = 0
    return cor_matrix

def generate_seizures_phases(eeg_signal, start_seizure_time, end_seizure_time, sampling_freq):
    """
    Devuelve tres secciones de la señal EEG que corresponden a las fases 
    preictal, ictal y postictal de la convulsión.

    Parameters:
        eeg_signal: una señal EEG (electroencefalograma), que se espera que sea un arreglo numpy.
        start_seizure_time: el tiempo (en segundos) en el que comienza la convulsión.
        end_seizure_time: el tiempo (en segundos) en el que termina la convulsión.
        sampling_freq: la frecuencia de muestreo de la señal EEG, en Hz.
    Returns:
        preictal: una sección de la señal EEG que se registra antes del inicio de la convulsión. 
        La duración de la sección es igual a la duración de la convulsión. La forma de onda 
        EEG durante esta fase es generalmente similar a la que se observa durante la fase interictal.
        ictal: la sección de la señal EEG que se registra durante la convulsión. Esta sección 
        generalmente tiene una forma de onda distintiva y anormal que es característica 
        de la actividad epiléptica.
        postictal: una sección de la señal EEG que se registra después del final de la convulsión. 
        La duración de la sección es igual a la duración de la convulsión. 
        La forma de onda EEG durante esta fase es generalmente similar a la que 
        se observa durante la fase interictal, pero puede haber un período de 
        recuperación anormal.
    """
    seizure_duration = end_seizure_time - start_seizure_time
    preictal = eeg_signal[int(sampling_freq * start_seizure_time - sampling_freq *  seizure_duration):int(sampling_freq * start_seizure_time), :]
    ictal = eeg_signal[int(sampling_freq * start_seizure_time):int(sampling_freq*end_seizure_time), :]
    postictal = eeg_signal[int(sampling_freq*end_seizure_time):int(sampling_freq * end_seizure_time + sampling_freq * seizure_duration), :]
    return preictal, ictal, postictal

