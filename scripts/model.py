''' Copyright (c) 2017-2019 - Dumitrel Loghin (dumitrel@comp.nus.edu.sg) '''

''' Speedup and Energy Savings Laws - Common Function and Utilities -
see "The Energy Efficiency of Modern Multicore Systems", ICPPW 2018 '''

import sys, math, csv
from pprint import PrettyPrinter as pp

resolution = 9999

# stats columns for homogeneous systems
col_amdahl = 0
col_gustafson = 1

# stats columns for heterogeneous systems
col_amdahl_static = 0
col_amdahl_dynamic = 1
col_gustafson_static = 2
col_gustafson_dynamic = 3


''' Speedup Homogeneous '''
def speedup_amdahl(f, n):
    return 1.0 / (f + (1.0 - f) / n)

def speedup_gustafson(f, n):
    return f + (1.0 - f) * n

''' Speedup Heterogeneous '''
def speedup_amdahl_static(f, n, sigmas, j, k, l):
    return 1.0 / (f * sigmas[j][k] + (1.0 - f) / n * sigmas[j][l])

def speedup_gustafson_static(f, n, sigmas, j, k, l):
    return f * sigmas[k][j] + (1.0 - f) * n * sigmas[l][j]

def speedup_amdahl_dynamic(f, n, sigmas, j, k, l):
    ssum = sum(sigmas[i][0] for i in range(0,n))
    return 1.0 / (f * sigmas[j][k] + (1.0 - f) / ssum * sigmas[j][1])

def speedup_gustafson_dynamic(f, n, sigmas, j, k, l):
    ssum = sum(sigmas[i][0] for i in range(0,n))
    return f * sigmas[k][j] + (1.0 - f) * sigmas[0][j] * ssum


''' Time Homogeneous '''
def time_amdahl(f, n, seq_time):    
    return f * seq_time + (1 - f) / n * seq_time

def time_gustafson(f, n, seq_time):    
    return seq_time / (f + (1 - f) * n)

''' Time Heterogeneous '''
def time_amdahl_static(f, n, seq_times, sigmas, k, l):    
    return f * seq_times[k] + (1-f)/n * seq_times[l]

def time_amdahl_dynamic(f, n, seq_times, sigmas, k, l):
    tn = (1-f) * seq_times[0] / sum(sigmas[i][0] for i in range(0,n))
    return f * seq_times[k] + tn


''' Energy Homogeneous '''
def energy_homogeneous(f, n, t, p_sys, rho):    
    return f * t * (p_sys + rho * p_sys) + (1-f) / n * t * (p_sys + (n - 1) * rho * p_sys)

''' Energy Heterogeneous '''
def energy_amdahl_static(f, n, seq_times, sigmas, p_sys, rhos, k, l):
    esum = sum(seq_times[i] * rhos[i] for i in range(0,n))
    return f * seq_times[k] * p_sys * (1 + rhos[k]) + (1-f)/n * p_sys * (seq_times[l] + esum)

def energy_amdahl_dynamic(f, n, seq_times, sigmas, p_sys, rhos, k, l):
    rsum = sum(rhos[i] for i in range(0,n))
    tn = (1-f) * seq_times[0] / sum(sigmas[i][0] for i in range(0,n))
    return f * seq_times[k] * p_sys * (1 + rhos[k]) + tn * p_sys * (1 + rsum)


''' Energy Savings Homogeneous '''
def ensave_amdahl(f, n, rho):
    return (1 - f) * (1 - 1.0 / n - (n-1) * rho / (n * (rho+1)))

def ensave_gustafson(f, n, rho):
    return 1 - (f + (1 - f) * (n * rho + 1) / (rho + 1)) / (f + (1 - f) * n)

''' Energy Savings Heterogeneous '''
def ensave_amdahl_static(f, n, rhos, sigmas, j, k, l):
    srsum = sum(sigmas[j][i] * rhos[i] for i in range(0,n))
    return 1.0 - f * sigmas[j][k] * (rhos[k] + 1.0)/(rhos[j] + 1.0) - (1.0 - f) / n * (sigmas[j][l] + srsum) / (rhos[j] + 1.0) 

def ensave_amdahl_dynamic(f, n, rhos, sigmas, j, k, l):
    rsum = sum(rhos[i] for i in range(0,n))
    ssum = sum(sigmas[i][0] for i in range(0,n))
    return 1.0 - f * sigmas[j][k] * (rhos[k] + 1.0)/(rhos[j] + 1.0) - (1.0 - f) * sigmas[j][0] * (1.0 + rsum) / ((1 + rhos[j]) * ssum)

def ensave_gustafson_static(f, n, rhos, sigmas, j, k, l):
    srsum = sum(sigmas[l][i] * rhos[i] for i in range(0,n))
    return 1.0 - (f * (rhos[k] + 1.0) + (1.0 - f) * (1.0 + srsum)) / ((f * sigmas[k][j] + (1.0 - f) * n * sigmas[l][j]) * (rhos[j] + 1.0))

def ensave_gustafson_dynamic(f, n, rhos, sigmas, j, k, l):
    rsum = sum(rhos[i] for i in range(0,n))
    ssum = sum(sigmas[i][0] for i in range(0,n))
    return 1.0 - (f * (rhos[k] + 1.0) + (1.0 - f) * (1.0 + rsum)) / ((f * sigmas[k][j] + (1.0 - f) * sigmas[0][j] * ssum) * (rhos[j] + 1.0))


''' Utils '''
def fill_sigmas(n, nl, nb, s_lb, s_bl, l2b = False):
    sigmas = []
    if l2b:
        # little first, big after
        for i in range(nl):
            sigmas_row = []
            for j in range(nl):
                sigmas_row.append(1.0)
            for j in range(nb):
                sigmas_row.append(s_lb)            
            sigmas.append(sigmas_row)  
        for i in range(nb):
            sigmas_row = []
            for j in range(nl):
                sigmas_row.append(s_bl)
            for j in range(nb):
                sigmas_row.append(1.0)
            sigmas.append(sigmas_row)    
    else:
        # big first first, little after
        for i in range(nb):
            sigmas_row = []
            for j in range(nb):
                sigmas_row.append(1.0)
            for j in range(nl):
                sigmas_row.append(s_bl)
            sigmas.append(sigmas_row)
        for i in range(nl):
            sigmas_row = []
            for j in range(nb):
                sigmas_row.append(s_lb)
            for j in range(nl):
                sigmas_row.append(1.0)
            sigmas.append(sigmas_row)    
    return sigmas

def fill_rhos(n, nl, nb, rho_l, rho_b, l2b = False):
    rhos = []
    if l2b:
        for i in range(nl):
            rhos.append(rho_l)        
        for i in range(nb):
            rhos.append(rho_b)        
    else:
        for i in range(nb):
            rhos.append(rho_b)
        for i in range(nl):
            rhos.append(rho_l)
    return rhos

def fill_seq_times(n, nl, nb, t_l, t_b, l2b = False):
    seq_times = []
    if l2b:
        print("Little cores first")
        for i in range(nl):
            seq_times.append(t_l)
        for i in range(nb):
            seq_times.append(t_b)
    else:
        for i in range(nb):
            seq_times.append(t_b)
        for i in range(nl):
            seq_times.append(t_l)
    return seq_times

def rmsd(x, y, n):   
    ssum = sum((x[i] - y[i]) ** 2 for i in range(0,n))
    return math.sqrt(ssum/n)

def get_times_homogeneous(f, n, seq_time, time_func):
    predicted_times = []
    for j in range(0,n):
        predicted_times.append(time_func(f, j+1, seq_time))
    return predicted_times

def get_times(f, n, seq_times, sigmas, time_func):
    predicted_times = []
    for j in range(0,n):
        predicted_times.append(time_func(f, j+1, seq_times, sigmas, 0, j))
    return predicted_times

def get_speedups_homogeneous(f, n, speedup_func):
    predicted_speedups = [1.0]
    for j in range(1,n):
        predicted_speedups.append(speedup_func(f, j+1))
    return predicted_speedups

def get_speedups(f, n, sigmas, speedup_func):
    predicted_speedups = [1.0]
    for j in range(1,n):
        predicted_speedups.append(speedup_func(f, j+1, sigmas, 0, 0, j))
    return predicted_speedups

def get_energies_homogeneous(f, n, seq_time, p_sys, rho, en_func):
    predicted_en = []
    for j in range(0,n):
        predicted_en.append(en_func(f, j+1, seq_time, p_sys, rho))
    return predicted_en

def get_energies(f, n, seq_times, sigmas, p_sys, rhos, en_func):
    predicted_en = []
    for j in range(0,n):
        predicted_en.append(en_func(f, j+1, seq_times, sigmas, p_sys, rhos, 0, j))
    return predicted_en

def get_energy_savings_homogeneous(f, n, rho, es_func):
    predicted_es = [0.0]
    for j in range(1,n):
        predicted_es.append(es_func(f, j+1, rho))
    return predicted_es

def get_energy_savings(f, n, rhos, sigmas, es_func):
    predicted_es = [0.0]
    for j in range(1,n):
        predicted_es.append(es_func(f, j+1, rhos, sigmas, 0, 0, j))
    return predicted_es

def get_energy_savings_rmsd(measured_es, f, n, rhos, sigmas, es_func):
    return rmsd(measured_es, get_energy_savings(f, n, rhos, sigmas, es_func), n)

def get_best_f(measured_speedups, n, sigmas, speedup_func, is_homogeneous = False):
    min_rmsd = 2.0 * n
    min_f = 0
    for i in range(1, resolution):
        f = (1.0 * i) / resolution
        if is_homogeneous:
            predicted_speedups = get_speedups_homogeneous(f, n, speedup_func)            
        else:
            predicted_speedups = get_speedups(f, n, sigmas, speedup_func)
        curr_rmsd = rmsd(measured_speedups, predicted_speedups, n)       
        # print(curr_rmsd)
        if curr_rmsd < min_rmsd:
            min_rmsd = curr_rmsd
            min_f = f
    
    return [min_f, min_rmsd]

def format_f(f):
    if f < 0.001:
        return "%.4f" % f
    elif f < 0.01:
        return "%.3f" % f
    elif f > 0.99:
        return "%.4f" % f
    return "%.2f" % f

def save_to_csv(filename, n, measured_speedups, predicted_speedups, measured_es, predicted_es, measured_times, predicted_times, measured_energies, predicted_energies):
    with open(filename, 'wt') as outfile:
        outfile.write("#Cores;Measured Speedup;Predicted Speedup;Measured Energy Savings;Predicted Energy Savings;Measured Time;Predicted Time;Measured Energy;Predicted Energy\n")
        for i in range(0,n):
            data = [str(i+1), "%.2f" % measured_speedups[i], "%.2f" % predicted_speedups[i], "%.3f" % measured_es[i], "%.3f" % predicted_es[i], "%.1f" % measured_times[i], "%.1f" % predicted_times[i], "%.1f" % measured_energies[i], "%.1f" % predicted_energies[i]]
            outfile.write(";".join(data) + "\n") 
        outfile.close()

def save_stats_to_csv(filename, prg, stats):
    size = int(len(stats) / 3)
    with open(filename, 'at') as outfile:
        data = [prg]
        for j in range(size):
            data.append(format_f(stats[j]))    
        for j in range(size):
            data.append("%.3f" % stats[j+size])
        for j in range(size):
            data.append("%.1f" % (100.0 * stats[j+2*size]))             
        outfile.write(";".join(data) + "\n") 
        outfile.close()

''' Get the sequential time (T(1)) from file'''
def get_t_seq(filename):
    with open(filename, 'rt') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        for row in csvreader:
            if (row[0].startswith('#')):
                continue
            if (row[1] == '1'):
                return float(row[3])

def get_data(filename):
    times = []
    energies = []
    measured_speedups = []
    measured_energy_savings = []
    with open(filename, 'rt') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        for row in csvreader:
            if (row[0].startswith('#')):
                continue
            t = float(row[3])
            p = float(row[6])
            e = p * t
            times.append(t)
            energies.append(e)
            measured_speedups.append(times[0] / t)
            measured_energy_savings.append((energies[0] - e) / energies[0])

    return times, energies, measured_speedups, measured_energy_savings

