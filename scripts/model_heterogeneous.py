''' Copyright (c) 2017-2019 - Dumitrel Loghin (dumitrel@comp.nus.edu.sg) '''

''' Apply Speedup and Energy Savings on Heterogeneous Systems '''

from model import *

def main(args):
    if len(args) < 12:
        print("Usage: " + args[0] + " n nl nb apf_l apf_b app file_l file_b file_static file_dynamic [-l2b]")
        print("\tn - total number of cores")
        print("\tnl - number of little cores")
        print("\tnb - number of big cores")
        print("\tapf_l - APF of little core")
        print("\tapf_b - APF of big core")
        print("\tp_sys - system (idle) power")
        print("\tapp - application name")
        print("\tfile_l - performance measuremnets on little cores only")
        print("\tfile_b - performance measuremnets on big cores only")
        print("\tfile_static - performance measuremnets on all cores using static OpenMP scheduling")
        print("\tfile_dynamic - performance measuremnets on all cores using dynamic OpenMP scheduling")
        return

    # args
    n = int(args[1])
    nl = int(args[2])
    nb = int(args[3])
    apf_l = float(args[4])
    apf_b = float(args[5])
    p_sys = float(args[6])
    app = args[7].upper()
    little_file = args[8]
    big_file = args[9]
    all_static_file = args[10]
    all_dynamic_file = args[11]
    l2b = False
    if len(args) == 13 and args[12] == "-l2b":
        l2b = True

    tl = get_t_seq(little_file)
    tb = get_t_seq(big_file)

    s_lb = tb / tl
    s_bl = tl / tb

    sigmas = fill_sigmas(n, nl, nb, s_lb, s_bl, l2b)
    apfs = fill_rhos(n, nl, nb, apf_l, apf_b, l2b)
    seq_times = fill_seq_times(n, nl, nb, tl, tb, l2b)

    stats = [0.0 for i in range(12)]

    # Static
    times, energies, measured_speedups, measured_energy_savings = get_data(all_static_file)

    [f, f_rmsd] = get_best_f(measured_speedups, n, sigmas, speedup_amdahl_static)
    predicted_speedups = get_speedups(f, n, sigmas, speedup_amdahl_static)
    predicted_energy_savings = get_energy_savings(f, n, apfs, sigmas, ensave_amdahl_static)
    es_rmsd = rmsd(measured_energy_savings, predicted_energy_savings, n)
    predicted_times = get_times(f, n, seq_times, sigmas, time_amdahl_static)
    predicted_energies = get_energies(f, n, seq_times, sigmas, p_sys, apfs, energy_amdahl_static)
    save_to_csv("amdahl-static/data-" + app.lower() + ".csv", n, measured_speedups, predicted_speedups, measured_energy_savings, predicted_energy_savings, times, predicted_times, energies, predicted_energies)
    print(app, "Amdahl Static [f RMSD(f) RMSD(es)]: ", format_f(f), "%.3f" % f_rmsd, "%.1f" % (100.0 * es_rmsd))
    stats[col_amdahl_static] = f
    stats[col_amdahl_static + 4] = f_rmsd
    stats[col_amdahl_static + 8] = es_rmsd
    
    [f, f_rmsd] = get_best_f(measured_speedups, n, sigmas, speedup_gustafson_static)
    predicted_speedups = get_speedups(f, n, sigmas, speedup_gustafson_static)
    predicted_energy_savings = get_energy_savings(f, n, apfs, sigmas, ensave_gustafson_static)
    es_rmsd = rmsd(measured_energy_savings, predicted_energy_savings, n)
    predicted_times = [0.0 for i in range(n)]
    predicted_energies = [0.0 for i in range(n)]
    save_to_csv("gustafson-static/data-" + app.lower() + ".csv", n, measured_speedups, predicted_speedups, measured_energy_savings, predicted_energy_savings, times, predicted_times, energies, predicted_energies)
    print(app, "Gustafson Static [f RMSD(f) RMSD(es)]: ", format_f(f), "%.3f" % f_rmsd, "%.1f"% (100.0 * es_rmsd))
    stats[col_gustafson_static] = f
    stats[col_gustafson_static + 4] = f_rmsd
    stats[col_gustafson_static + 8] = es_rmsd

    # Dynamic
    times, energies, measured_speedups, measured_energy_savings = get_data(all_dynamic_file)
    
    [f, f_rmsd] = get_best_f(measured_speedups, n, sigmas, speedup_amdahl_dynamic)
    predicted_speedups = get_speedups(f, n, sigmas, speedup_amdahl_dynamic)
    predicted_energy_savings = get_energy_savings(f, n, apfs, sigmas, ensave_amdahl_dynamic)
    es_rmsd = rmsd(measured_energy_savings, predicted_energy_savings, n)
    predicted_times = get_times(f, n, seq_times, sigmas, time_amdahl_dynamic)
    predicted_energies = get_energies(f, n, seq_times, sigmas, p_sys, apfs, energy_amdahl_dynamic)
    save_to_csv("amdahl-dynamic/data-" + app.lower() + ".csv", n, measured_speedups, predicted_speedups, measured_energy_savings, predicted_energy_savings, times, predicted_times, energies, predicted_energies)
    print(app, "Amdahl Dynamic [f RMSD(f) RMSD(es)]: ", format_f(f), "%.3f" % f_rmsd, "%.1f" % (100.0 * es_rmsd))
    stats[col_amdahl_dynamic] = f
    stats[col_amdahl_dynamic + 4] = f_rmsd
    stats[col_amdahl_dynamic + 8] = es_rmsd

    [f, f_rmsd] = get_best_f(measured_speedups, n, sigmas, speedup_gustafson_dynamic)
    predicted_speedups = get_speedups(f, n, sigmas, speedup_gustafson_dynamic)
    predicted_energy_savings = get_energy_savings(f, n, apfs, sigmas, ensave_gustafson_dynamic)
    es_rmsd = rmsd(measured_energy_savings, predicted_energy_savings, n)
    predicted_times = [0.0 for i in range(n)]
    predicted_energies = [0.0 for i in range(n)]
    save_to_csv("gustafson-dynamic/data-" + app.lower() + ".csv", n, measured_speedups, predicted_speedups, measured_energy_savings, predicted_energy_savings, times, predicted_times, energies, predicted_energies)
    print(app, "Gustafson Dynamic [f RMSD(f) RMSD(es)]: ", format_f(f), "%.3f" % f_rmsd, "%.1f" % (100.0 * es_rmsd))
    stats[col_gustafson_dynamic] = f
    stats[col_gustafson_dynamic + 4] = f_rmsd
    stats[col_gustafson_dynamic + 8] = es_rmsd

    save_stats_to_csv("stats.csv", app, stats)

if __name__ == "__main__":
    main(sys.argv)
