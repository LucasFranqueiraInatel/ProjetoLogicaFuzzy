import numpy as np
import skfuzzy as fuzz
import paho.mqtt.client as mqtt
from skfuzzy import control as ctrl
import time

mqttBroker = "test.mosquitto.org"
client = mqtt.Client("C213_fuzzy")
client.connect(mqttBroker)

# New Antecedent/Consequent objects hold universe variables and membership
# functions
errotemp = ctrl.Antecedent(np.arange(-45, 46, 1), 'errotemp')
varerrotemp = ctrl.Antecedent(np.arange(-2, 2.01, 0.01), 'varerrotemp')
aquecedor = ctrl.Consequent(np.arange(0, 100, 1), 'aquecedor')

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
errotemp['MN'] = fuzz.trapmf(errotemp.universe, [-45, -45, -2, -1])
errotemp['PN'] = fuzz.trimf(errotemp.universe, [-2, -1, 0])
errotemp['ZE'] = fuzz.trimf(errotemp.universe, [-1, 0, 1])
errotemp['PP'] = fuzz.trimf(errotemp.universe, [0, 1, 2])
errotemp['MP'] = fuzz.trapmf(errotemp.universe, [1, 2, 45, 45])
# You can see how these look with .view()
errotemp.view()
varerrotemp['MN'] = fuzz.trapmf(varerrotemp.universe, [-2, -2, -0.2, -0.1])
varerrotemp['PN'] = fuzz.trimf(varerrotemp.universe, [-0.2, -0.1, 0])
varerrotemp['ZE'] = fuzz.trimf(varerrotemp.universe, [-0.1, 0, 0.1])
varerrotemp['PP'] = fuzz.trimf(varerrotemp.universe, [0, 0.1, 0.2])
varerrotemp['MP'] = fuzz.trapmf(varerrotemp.universe, [0.1, 0.2, 2, 2])
# You can see how these look with .view()
varerrotemp.view()
aquecedor['MB'] = fuzz.trimf(aquecedor.universe, [0, 0, 25])
aquecedor['B'] = fuzz.trimf(aquecedor.universe, [0, 25, 50])
aquecedor['M'] = fuzz.trimf(aquecedor.universe, [25, 50, 75])
aquecedor['A'] = fuzz.trimf(aquecedor.universe, [50, 75, 100])
aquecedor['MA'] = fuzz.trimf(aquecedor.universe, [75, 100, 100])
aquecedor.view()
regra1 = ctrl.Rule(errotemp['MN'] & varerrotemp['MN'], aquecedor['M'])
regra2 = ctrl.Rule(errotemp['PN'] & varerrotemp['MN'], aquecedor['M'])
regra3 = ctrl.Rule(errotemp['ZE'] & varerrotemp['MN'], aquecedor['M'])
regra4 = ctrl.Rule(errotemp['PP'] & varerrotemp['MN'], aquecedor['M'])
regra5 = ctrl.Rule(errotemp['MP'] & varerrotemp['MN'], aquecedor['M'])
regra6 = ctrl.Rule(errotemp['MN'] & varerrotemp['PN'], aquecedor['M'])
regra7 = ctrl.Rule(errotemp['PN'] & varerrotemp['PN'], aquecedor['M'])
regra8 = ctrl.Rule(errotemp['ZE'] & varerrotemp['PN'], aquecedor['M'])
regra9 = ctrl.Rule(errotemp['PP'] & varerrotemp['PN'], aquecedor['M'])
regra10 = ctrl.Rule(errotemp['MP'] & varerrotemp['PN'], aquecedor['M'])
regra11 = ctrl.Rule(errotemp['MN'] & varerrotemp['ZE'], aquecedor['M'])
regra12 = ctrl.Rule(errotemp['PN'] & varerrotemp['ZE'], aquecedor['M'])
regra13 = ctrl.Rule(errotemp['ZE'] & varerrotemp['ZE'], aquecedor['M'])
regra14 = ctrl.Rule(errotemp['PP'] & varerrotemp['ZE'], aquecedor['M'])
regra15 = ctrl.Rule(errotemp['MP'] & varerrotemp['ZE'], aquecedor['M'])
regra16 = ctrl.Rule(errotemp['MN'] & varerrotemp['PP'], aquecedor['M'])
regra17 = ctrl.Rule(errotemp['PN'] & varerrotemp['PP'], aquecedor['M'])
regra18 = ctrl.Rule(errotemp['ZE'] & varerrotemp['PP'], aquecedor['M'])
regra19 = ctrl.Rule(errotemp['PP'] & varerrotemp['PP'], aquecedor['M'])
regra20 = ctrl.Rule(errotemp['MP'] & varerrotemp['PP'], aquecedor['M'])
regra21 = ctrl.Rule(errotemp['MN'] & varerrotemp['MP'], aquecedor['M'])
regra22 = ctrl.Rule(errotemp['PN'] & varerrotemp['MP'], aquecedor['M'])
regra23 = ctrl.Rule(errotemp['ZE'] & varerrotemp['MP'], aquecedor['M'])
regra24 = ctrl.Rule(errotemp['PP'] & varerrotemp['MP'], aquecedor['M'])
regra25 = ctrl.Rule(errotemp['MP'] & varerrotemp['MP'], aquecedor['M'])
aquecedor_ctrl = ctrl.ControlSystem(
    [regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9, regra10, regra11, regra12, regra13,
     regra14, regra15, regra16, regra17, regra18, regra19, regra20, regra21, regra22, regra23, regra24, regra25])
potencia = ctrl.ControlSystemSimulation(aquecedor_ctrl)
sp = 30
tempatual = 32
print(tempatual)
erroatual = 0
while True:
    erroanterior = erroatual
    erroatual = tempatual - sp
    varerroTemp = erroatual - erroanterior
    potencia.input['errotemp'] = erroatual
    potencia.input['varerrotemp'] = varerroTemp
    potencia.compute()
    i = 0
    while (i < 10):
        tempatual = tempatual * 0.9954 + potencia.output['aquecedor'] * 0.002763
        time.sleep(1)
        i += 1
    print(tempatual)
    client.publish("Aquecedor/Temperatura", tempatual)
    client.publish("Aquecedor/erro", erroatual)
