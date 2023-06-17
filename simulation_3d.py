
# The code for running the simulation
# Parameters are described in appropriate python files
# look into the files for parameter descriptions


from elecmarket_3d import *
import os as os
scenario_name = "test" # this will be the name of the output file & folder

cp = getpar("common_params_3d.py")

# list of conventional agents; modify this to add / remove agent types
cagents = [Conventional('Coal_3d',cp,getpar('coal_3d.py')),
          Conventional('Gas_3d',cp,getpar('gas_3d.py'))]

# list of renewable agents; modify this to add / remove agent types
ragents = [Renewable('Renewable_3d',cp,getpar('renewable_3d.py'))]

Niter = cp['iterations']
tol = cp['tolerance']
sim = Simulation(cagents,ragents,cp)
conv, elapsed, Nit = sim.run(Niter, tol, cp['power'], cp['offset'])
print('Elapsed time: ', elapsed)
out = sim.write(scenario_name)
try:
    os.mkdir(scenario_name)
except FileExistsError:
    print('Directory already exists')
#os.system("cp common_params.py "+scenario_name+"/common_params.py")

# parameter files are copied to output directory; change this if you change agent types
#os.system("cp coal.py "+scenario_name+"/coal.py")
#os.system("cp gas.py "+scenario_name+"/gas.py")
#os.system("cp renewable.py "+scenario_name+"/renewable.py")

#os.system("cp "+scenario_name+'.csv '+scenario_name+"/"+scenario_name+".csv")


plt.figure(figsize=(14,5))
plt.subplot(121)
plt.plot(2018+out['time'], out['peak price'], label='peak price')
plt.plot(2018+out['time'], out['offpeak price'], label='offpeak price')
plt.legend()
plt.title('Electricity price')
plt.subplot(122)

# Plotting the capacity for each agent type; modify this if you change agent types
plt.plot(2018+out['time'], out['Coal_3d capacity'], label='Coal capacity')
plt.plot(2018+out['time'], out['Gas_3d capacity'],label='Gas capacity')
plt.plot(2018+out['time'], out['Renewable_3d capacity'], label='Renewable capacity')
plt.legend()
plt.title('Installed capacity')
plt.savefig(scenario_name+"/"+'price_capacity.pdf', format='pdf')

plt.figure(figsize=(14, 5))
plt.subplot(121)
plt.plot(2018+out['time'], sim.pdemand, label='peak demand')
plt.plot(2018+out['time'], sim.opdemand, label='offpeak demand')
plt.legend()
plt.title('Electricity demand')
plt.subplot(122)

# Plotting the fuel prices; modify this if you change fuel types
plt.plot(2018+out['time'], out['Fuel 0'], label='Coal price')
plt.plot(2018+out['time'], out['Fuel 1'], label='Gas price')
plt.legend()
plt.title('Fuel price')
#plt.plot(2018+out['time'],np.interp(out['time'],cp["carbon tax"][0],cp["carbon tax"][1]))
plt.savefig(scenario_name+"/"+'demand_fuelprice.pdf',format='pdf')


plt.figure(figsize=(14,5))
plt.subplot(121)

# Plotting the supply for each agent; modify this if you change agent types
plt.bar(2018+out['time'],out['Coal_3d peak supply'],width=0.25,label='Coal supply')
plt.bar(2018+out['time'],out['Gas_3d peak supply'],width=0.25,
        bottom=out['Coal_3d peak supply'],label='Gas supply')
plt.bar(2018+out['time'],out['Renewable_3d peak supply'],width=0.25,
        bottom=out['Gas_3d peak supply']+out['Coal_3d peak supply'],label='Renewable supply')
#plt.ylim([0,80])
plt.title('Conventional/ renewable peak supply, GW')
plt.legend()
plt.subplot(122)
plt.bar(2018+out['time'],out['Coal_3d offpeak supply'],width=0.5,label='Coal supply')
plt.bar(2018+out['time'],out['Gas_3d offpeak supply'],width=0.25,
        bottom=out['Coal_3d offpeak supply'],label='Gas supply')
plt.bar(2018+out['time'],out['Renewable_3d offpeak supply'],width=0.25,
        bottom=out['Gas_3d offpeak supply']+out['Coal_3d offpeak supply'],label='Renewable supply')

plt.title('Conventional/ renewable off-peak supply, GW')

#plt.ylim([0,80])


plt.legend()
plt.savefig(scenario_name+"/"+'supply.pdf',format='pdf')
plt.show()



print('Elapsed time: ', elapsed)