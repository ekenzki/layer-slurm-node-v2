import subprocess
import sys

#Returns the ammount of memory in MB that slurm can allocate
def _get_mem():
    percent = 0.93 #Percent of total memory SLURM is able to allocate
    mem =  int(subprocess.check_output("cat /proc/meminfo | grep MemTotal | awk '{print $2}'", shell=True))
    mem = mem / 1024 * percent
    return int(mem)

#Returns the number of NVIDIA GPUS inside the node.
def _get_gpus():
    gpus = int(subprocess.check_output("lspci | grep -i nvidia | awk '{print $1}' | cut -d : -f 1 | sort -u | wc -l", shell=True))
    return gpus

#Returns a list of cpuaffinity for each GPU. Example list: "0-11", "12-23"
def _get_cpuaffinity():
    cpuaffinity=[]
    gpu_id = subprocess.check_output("lspci | grep -i nvidia | awk '{print $1}' | cut -d : -f 1 | sort -u",
                                        shell=True).strip().decode('ascii')

    if not gpu_id:
        return cpuaffinity

    gpu_id_list = gpu_id.split()
    for i in gpu_id_list:
        tmp = subprocess.check_output("cat /sys/class/pci_bus/0000\\:{0}/cpulistaffinity".format(i),
                                        shell=True).strip().decode('ascii')
        cpuaffinity.append(tmp)
    return cpuaffinity

#Returns number of CPU sockets
def _get_sockets():
    sockets = int(subprocess.check_output("lscpu | grep 'Socket(s):'  | cut -d : -f 2 | awk '{print $1}'", shell=True))
    return sockets

def _get_threadspercore():
    threadspercore = int(subprocess.check_output("lscpu | grep 'Thread(s) per core:' | cut -d : -f 2 | awk '{print $1}'", shell=True))
    return threadspercore

def _get_corespersocket():
    corespersocket = int(subprocess.check_output("lscpu | grep 'Core(s) per socket:' | cut -d : -f 2 | awk '{print $1}'", shell=True))
    return corespersocket

def get_inventory():
    inv = {}
    inv['memory'] = _get_mem()
    inv['gpus'] = _get_gpus()
    inv['cpuaffinity'] = _get_cpuaffinity()
    inv['sockets'] = _get_sockets()
    inv['threadspercore'] = _get_threadspercore()
    inv['corespersocket'] = _get_corespersocket()
    return inv

