# Time-energy Measurements of Shared-memory Applications on Modern Multicore Systems

This repository provides the time-energy data collected and analyzed in our research paper
entitled "The Time and Energy Efficiency of Modern Multicore Systems" (PARCO 2019). Please 
read our [Data-in-Brief article](article.pdf) for a detailed description of the data.

## How to Use

To generate model data in `data/model` folder, go to scripts folder and run:

```
$ ./run-homogeneous.sh
$ ./run-heterogeneous.sh
```

You need `bash` and `Python 3` to run these scripts.

The model's equations are implemented in [model.py](scripts/model.py).

### Homogeneous

The script [model_homogeneous.py](scripts/model_homogeneous.py) uses the equations corresponding to
homogeneous multicore systems implemented in [model.py](scripts/model.py). It takes as paramters the
number of cores, the active power fraction of the system (APF), the idle power of the system (in Watts), 
application name (for display) and the measured data for the given application on the given homogeneous 
system.

```
Usage: model_homogeneous.py n apf psys app measurements_file
	n - total number of cores
	apf - APF
	psys - system power [W]
	app - application name
	measurements_file - time-energy measuremnets on all cores
```

We provide a set of parameters for the AMD, ARM, Xeon, i7 and Pi3 homogeneous systems [1, 2, 3] in 
[conf-amd.sh](scripts/conf-amd.sh), [conf-arm.sh](scripts/conf-arm.sh), [conf-xeon.sh](scripts/conf-xeon.sh), 
[conf-i7.sh](scripts/conf-i7.sh), [conf-pi3.sh](scripts/conf-pi3.sh), respectively.

### Heterogeneous

The script [model_heterogeneous.py](scripts/model_heterogeneous.py) uses the equations corresponding to
heterogeneous multicore systems implemented in [model.py](scripts/model.py). It takes as paramters the total
number of cores, the number of little and big cores, the active power fraction (APF) of little and big cores, 
the idle power of the system (in Watts), application name (for display) and the measured data for the given 
application on little cores, big cores, all cores using static scheduling and all cores using dynamic scheduling.

```
Usage: model_heterogeneous.py n nl nb apf_l apf_b app file_l file_b file_static file_dynamic [-l2b]
	n - total number of cores
	nl - number of little cores
	nb - number of big cores
	apf_l - APF of little core
	apf_b - APF of big core
	p_sys - system (idle) power
	app - application name
	file_l - performance measuremnets on little cores only
	file_b - performance measuremnets on big cores only
	file_static - performance measuremnets on all cores using static OpenMP scheduling
	file_dynamic - performance measuremnets on all cores using dynamic OpenMP scheduling
```

We provide a set of parameters for the XU3 and TX2 heterogeneous systems [1, 2, 3] in [conf-xu3.sh](scripts/conf-xu3.sh), 
[conf-tx2.sh](scripts/conf-tx2.sh), respectively.

## List of Publications

* [1] D. Loghin and Y.M. Teo, *"The Energy Efficiency of Modern Multicore Systems"*, in Proc. of the 47th International Conference on Parallel Processing Companion [https://doi.org/10.1145/3229710.3229714](https://doi.org/10.1145/3229710.3229714)

* [2] D. Loghin and Y.M. Teo, *"The Time and Energy Efficiency of Modern Multicore Systems"*, in "PARCO" [https://doi.org/10.1016/j.parco.2019.04.009](https://doi.org/10.1016/j.parco.2019.04.009)

* [3] D. Loghin and Y.M. Teo, *"Time-energy Measured Data on Modern Multicore Systems Running Shared-memory Applications"*, in "Data in Brief" [https://doi.org/10.1016/j.dib.2019.104670](https://doi.org/10.1016/j.dib.2019.104670)).

## License

This repository is licensed under Creative Commons Attribution 4.0 license (http://creativecommons.org/licenses/by/4.0/)

If you are using these data in your research, please cite one of our papers.
