import matplotlib.pyplot as plt

# values found earlier
RTT = [15.904, 16.651, 16.925, 16.993, 17.895, 19.456]  
RTT2 = [122.608, 129.094, 148.981, 149.932, 151.483, 152.194]  
RTT3 = [584.077, 584.920, 585.345, 587.834, 588.678, 594.089]

sizes = [1, 100, 200, 400, 800, 1000]  

# plot creation
plt.figure(figsize=(8, 5))
plt.plot(sizes, RTT, marker='o', linestyle='-', color='b', label="RTT vs Message Size")
plt.plot(sizes, RTT2, marker='s', linestyle='--', color='r', label="RTT vs Message Size (Server delay=0.1s)")
plt.plot(sizes, RTT3, marker='^', linestyle='-.', color='g', label="RTT vs Message Size (Server delay=0.5s)")


# labels
plt.xlabel("Message Size (Bytes)")
plt.ylabel("RTT (ms)")
plt.title("RTT vs Message Size")
#plt.title("RTT vs Message Size (Server delay=0.1s)")
#plt.title("RTT vs Message Size (Server delay=0.5s)")
plt.legend()
plt.grid(True)

# show
plt.show()