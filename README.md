# ecmo_pulse_scripts

You must run these scripts in an environment set up with the Pulse bindings. It is suggested that you follow their guide for setup in [PyCharm](https://gitlab.kitware.com/physiology/engine/-/wikis/Using-Pycharm). Checkout the `Debug` file if you run into any issues 
In order to generate graphs, you first need to run all the scripts to generate cvs files. Run `run_scripts/generate_cvs_files.py` in order to accomplish this. This has proven to take up a lot of RAM. If `generate_cvs_files.py`gets hung up because of RAM restrictions, run it in smaller blocks. This simply means commenting out some of the disease states and treatments or edit the script to run one patient at a time.
You can then run `run_scripts/generate_graphs.py`. 
