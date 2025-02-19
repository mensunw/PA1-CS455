import matplotlib.pyplot as plt

# values found earlier
RTT = [1, 2, 3, 4, 5, 6]  
# RTT = [1, 2, 3, 4, 5, 6] 
# RTT = [1, 2, 3, 4, 5, 6] 
# RTT = [1, 2, 3, 4, 5, 6] 

sizes = [1, 100, 200, 400, 800, 1000]  

# plot creation
plt.figure(figsize=(8, 5))
plt.plot(sizes, RTT, marker='o', linestyle='-', color='b', label="RTT vs Message Size")
# label="RTT vs Message Size"
# label="RTT vs Message Size (Server delay=0.5s)"
# label="RTT vs Message Size (Server delay=1s)"

# labels
plt.xlabel("Message Size (Bytes)")
plt.ylabel("RTT (ms)")
plt.title("RTT vs Message Size")
plt.legend()
plt.grid(True)

# show
plt.show()