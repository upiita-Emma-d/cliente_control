from nptdms import TdmsFile
from numpy.testing._private.utils import tempdir
def LecturaTDMS():
    tdms_file = TdmsFile.read("D:/repositorios/python-labview/Practica_1_remaster/pruebas.tdms")
    group = tdms_file['Datos ADC']
    ADC_p = []
    try:
        for numero in range(1,8000):
            channel = group[str(numero)]
            channel_data = channel[:]
            ADC_p.append(float(channel_data))
    except:
        pass
    return ADC_p