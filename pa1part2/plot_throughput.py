import matplotlib.pyplot as plt

# values found earlier
throughput = [0.048, 0.069, 0.157, 0.316, 0.497, 0.645]  
throughput2 = [0.007, 0.014, 0.022, 0.050, 0.076, 0.162]  
throughput3 = [0.002, 0.003, 0.006, 0.014, 0.025, 0.047]

sizes = [1000, 2000, 4000, 8000, 16000, 32000] 

# plot creation
plt.figure(figsize=(8, 5))
plt.plot(sizes, throughput, marker='o', linestyle='-', color='b', label="Throughput vs Message Size")
plt.plot(sizes, throughput2, marker='s', linestyle='--', color='r', label="Throughput vs Message Size (Server delay=0.1s)")
plt.plot(sizes, throughput3, marker='^', linestyle='-.', color='g', label="Throughput vs Message Size (Server delay=0.5s)")

# labels
plt.xlabel("Message Size (Bytes)")
plt.ylabel("Throughput (mbps)")
plt.title("Throughput vs Message Size")
#plt.title("Throughput vs Message Size (Server delay=0.1s)")
#plt.title("Throughput vs Message Size (Server delay=0.5s)")
plt.legend()
plt.grid(True)

# show
plt.show()