import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Define input variables
soc = ctrl.Antecedent(np.arange(0, 101, 1), 'soc')  # State of Charge (0% to 100%)
temperature = ctrl.Antecedent(np.arange(0, 81, 1), 'temperature')  # Battery Temperature (0°C to 80°C)

# Define output variable
charging_current = ctrl.Consequent(np.arange(0, 101, 1), 'charging_current')  # Charging Current (0A to 100A)

# Membership functions for SoC
soc['low'] = fuzz.trimf(soc.universe, [0, 0, 30])
soc['medium'] = fuzz.trimf(soc.universe, [30, 50, 70])
soc['high'] = fuzz.trimf(soc.universe, [60, 99, 100])
soc['full'] = fuzz.trimf(soc.universe, [100, 100,100])
# Membership functions for Temperature
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 15])
temperature['normal'] = fuzz.trimf(temperature.universe, [15, 30, 45])
temperature['warm'] = fuzz.trimf(temperature.universe, [40, 60, 60])
temperature['hot'] = fuzz.trapmf(temperature.universe, [61, 61,80,80])

# Membership functions for Charging Current
charging_current['stop'] = fuzz.trimf(charging_current.universe, [0, 0,0])
charging_current['low'] = fuzz.trimf(charging_current.universe, [1, 1,30])
charging_current['medium'] = fuzz.trimf(charging_current.universe, [30, 50, 60])
charging_current['high'] = fuzz.trimf(charging_current.universe, [61, 100, 100])

# Plot the membership functions
""" soc.view()
temperature.view()
charging_current.view() """

# Define fuzzy rules
rule1 = ctrl.Rule(soc['low'] & temperature['normal'], charging_current['high'])
rule2 = ctrl.Rule(soc['medium'] & temperature['normal'], charging_current['medium'])
rule3 = ctrl.Rule(soc['high'] | temperature['warm'], charging_current['low'])
rule4 = ctrl.Rule(soc['low'] & temperature['cold'], charging_current['medium'])
rule5 = ctrl.Rule(soc['full'] | temperature['hot'], charging_current['stop'])

# Create control system

charging_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4,rule5])
charging_simulation = ctrl.ControlSystemSimulation(charging_ctrl)

Test_rule1 = [10,27]
Test_rule2 = [40,24]
Test_rule3_1 = [70,27]
Test_rule3_2 = [10,50]
Test_rule4 = [9,12]
Test_rule5_1 = [100,27]
Test_rule5_2 = [50,66]
# Input example values
charging_simulation.input['soc'] = Test_rule4[0]  # Example: 10% SoC
charging_simulation.input['temperature'] = Test_rule4[1]  # Example: 25°C temperature

# Compute the charging current
charging_simulation.compute()

#charging_simulation.output['charging_current']
#charging_current.view(sim=charging_simulation)
""" soc.view()s
temperature.view()
charging_current.view() """
soc.view(sim=charging_simulation)
temperature.view(sim=charging_simulation)
charging_current.view(sim=charging_simulation)

# Print the output
print(f"Charging Current: {charging_simulation.output['charging_current']} A")

# Show plots
#print(charging_simulation.output['charging_current'])
plt.show()
