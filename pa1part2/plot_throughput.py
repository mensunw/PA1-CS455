import matplotlib.pyplot as plt

# values found earlier
throughput = [1, 2, 3, 4, 5, 6]  
# throughput = [1, 2, 3, 4, 5, 6]  
# throughput = [1, 2, 3, 4, 5, 6]  
# throughput = [1, 2, 3, 4, 5, 6]  

sizes = [1000, 2000, 4000, 8000, 16000, 32000] 

# plot creation
plt.figure(figsize=(8, 5))
plt.plot(sizes, throughput, marker='o', linestyle='-', color='b', label="Throughput vs Message Size")
# label="Throughput vs Message Size"
# label="Throughput vs Message Size (Server delay=0.5s)"
# label="Throughput vs Message Size (Server delay=1s)"

# labels
plt.xlabel("Message Size (Bytes)")
plt.ylabel("Throughput (mbps)")
plt.title("Throughput vs Message Size")
plt.legend()
plt.grid(True)

# show
plt.show()