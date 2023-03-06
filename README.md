# Seizures EEG Analysis Utilities

Esta librería contiene una serie de funciones que se pueden utilizar en el análisis básico de señales EEG. Fue diseñada específicamente para trabajar con la base de datos CHB-MIT Scalp EEG Database (https://physionet.org/content/chbmit/1.0.0/) la cual contiene EEG de pacientes con ataques epilépticos.

Las librerías que se requieren son:

- numpy
- scipy
- matplotlib
- pyedflib

Para instalarlas se puede utilizar los comandos:

`
pip install numpy
`
`
pip install scipy
`
`
pip install matplotlib
`
`
pip install pyedflib
`

## Descarga de los archivos EDF

Los archivos EDF de pacientes que tienen ataques epilépticos se muestran en el archivo de texto plano RECORDS-WITH-SEIZURES.txt. Para realizar la descarga de todos estos datos hay que ejecutar el script download_eeg_data.py con el comando

`
python download_eeg_data.py
`
