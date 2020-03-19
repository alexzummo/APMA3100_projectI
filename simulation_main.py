import monte_carlo_simulation as mcs

n = 1000
data = mcs.run_mcs(n)
f = open("simulation_times.txt", "w")
[print(time, file=f) for time in data]
f.close()
stats = mcs.parse_times(data)
print("Ran simulation", n, "times \nStatistics: ")
print("mean:\t\t\t", stats[0])
print("min:\t\t\t", stats[1])
print("1st quartile:\t", stats[2])
print("median:\t\t\t", stats[3])
print("3rd quartile:\t", stats[4])
print("min:\t\t\t", stats[5])





