import subprocess
import sys

def _get_mem():
    mem =  int(subprocess.check_output("cat /proc/meminfo | grep MemTotal | awk '{print $2}'", shell=True))
    mem = mem / 1024 * 0.93
    return int(mem)

def _get_gpus():
    gpus = int(subprocess.check_output("lspci | grep -i nvidia | awk '{print $1}' | cut -d : -f 1 | sort -u | wc -l", shell=True))
    return gpus

def _get_cpuaffinity():
    cpuaffinity=[]
    gpu_id = subprocess.check_output("lspci | grep -i nvidia | awk '{print $1}' | cut -d : -f 1 | sort -u",
                                        shell=True).strip().decode('ascii')
    if not gpu_id:
        return cpuaffinity
    if isinstance(gpu_id,list):
        for i in gpu_id:
            tmp = subprocess.check_output("cat /sys/class/pci_bus/0000\\:{0}/cpulistaffinity".format(i),
                                        shell=True).strip().decode('ascii')
            cpuaffinity.append(tmp)
    else:
        tmp = subprocess.check_output("cat /sys/class/pci_bus/0000\\:{0}/cpulistaffinity".format(gpu_id),
                                        shell=True).strip().decode('ascii')
        cpuaffinity.append(tmp)
    return cpuaffinity

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

