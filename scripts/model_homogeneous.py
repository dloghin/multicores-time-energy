''' Copyright (c) 2017-2019 - Dumitrel Loghin (dumitrel@comp.nus.edu.sg) '''

''' Apply Speedup and Energy Savings on Homogeneous Systems '''

from model import *

def main(args):
  if len(args) < 6:
    print("Usage: " + args[0] + " n apf psys app measurements_file")
    print("\tn - total number of cores")
    print("\tapf - APF")
    print("\tpsys - system power [W]")
    print("\tapp - application name")
    print("\tmeasurements_file - time-energy measuremnets on all cores")
    print("Current number of arguments: " + str(len(args)))
    return

  # args
  n = int(args[1])
  apf = float(args[2])
  psys = float(args[3])
  app = args[4].upper()
  measurements_file = args[5]

  # read data
  times, energies, measured_speedups, measured_energy_savings = get_data(measurements_file)
  
  # prepare stats (f, rmsd(f), rmsd(ensave)
  stats = [0.0 for i in range(6)]

  # Amdahl
  [f, f_rmsd] = get_best_f(measured_speedups, n, [], speedup_amdahl, True)
  predicted_speedups = get_speedups_homogeneous(f, n, speedup_amdahl)
  predicted_energy_savings = get_energy_savings_homogeneous(f, n, apf, ensave_amdahl)
  es_rmsd = rmsd(measured_energy_savings, predicted_energy_savings, n)
  predicted_times = get_times_homogeneous(f, n, times[0], time_amdahl)
  predicted_energies = get_energies_homogeneous(f, n, times[0], psys, apf, energy_homogeneous)
  save_to_csv("amdahl/data-" + app.lower() + ".csv", n, measured_speedups, predicted_speedups, measured_energy_savings, predicted_energy_savings, times, predicted_times, energies, predicted_energies)
  print(app, "Amdahl [f RMSD(f) RMSD(es)]: ", format_f(f), "%.3f" % f_rmsd, "%.1f" % (100.0 * es_rmsd))
  stats[col_amdahl] = f
  stats[col_amdahl + 2] = f_rmsd
  stats[col_amdahl + 4] = es_rmsd

  # Gustafson
  [f, f_rmsd] = get_best_f(measured_speedups, n, [], speedup_gustafson, True)
  predicted_speedups = get_speedups_homogeneous(f, n, speedup_gustafson)
  predicted_energy_savings = get_energy_savings_homogeneous(f, n, apf, ensave_gustafson)
  es_rmsd = rmsd(measured_energy_savings, predicted_energy_savings, n)
  predicted_times = get_times_homogeneous(f, n, times[0], time_gustafson)
  predicted_energies = get_energies_homogeneous(f, n, times[0], psys, apf, energy_homogeneous)
  save_to_csv("gustafson/data-" + app.lower() + ".csv", n, measured_speedups, predicted_speedups, measured_energy_savings, predicted_energy_savings, times, predicted_times, energies, predicted_energies)
  print(app, "Gustafson [f RMSD(f) RMSD(es)]: ", format_f(f), "%.3f" % f_rmsd, "%.1f" % (100.0 * es_rmsd))
  stats[col_gustafson] = f
  stats[col_gustafson + 2] = f_rmsd
  stats[col_gustafson + 4] = es_rmsd

  save_stats_to_csv("stats.csv", app, stats)

if __name__ == "__main__":
  main(sys.argv)
