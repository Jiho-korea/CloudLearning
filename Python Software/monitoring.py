import psutil
# gives a single float value
print("cpu percent: ", psutil.cpu_percent(interval=1))
# gives an object with many fields
print("virtual_memory", psutil.virtual_memory())
# you can convert that object to a dictionary
print("dict", dict(psutil.virtual_memory()._asdict()))
# you can have the percentage of used RAM
print("memory percent: ", psutil.virtual_memory().percent)

# you can calculate percentage of available memory
print("available memory percent", psutil.virtual_memory(
).available * 100 / psutil.virtual_memory().total)
