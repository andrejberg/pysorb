# PYSORP

## Generate QE input files

In `examples/qe_input_source` are some example files to set up a series of QE input files. 
`.pos` files contain positions of surface atoms or molecule. In these files those atoms are marked
by a number `1`(atom in molecule or surface top side), `2`(surface bridge side), `3`(surface hollow side) which will be used for positioning of the molecule above the surface.
`qe_template` contains all options to run a QE calculation except the atom positions.
`generate_files.params` tells the script which template files to combine and how to generate 
the different configurations.

```bash
python2 pysorb_mkqein.py -i examples/qe_input_source/generate_files.params -o examples/qe_input_generated
```

This files can then be used for QE calculation runs:

```bash
pw.x < file.in > file.out
```


## Extract information from QE outputfiles
Place a series of QE output files inside of a directory. This script will extract atom positions
and energies from these files and generate a single file which contains all required information to
do further analysis or generate a GULP input file.

```bash
python2 pysorb_dump.py -qe examples/qe_output -e_ref -7425.27983804 -o examples/test.qedump
```

## Generate GULP input files

### Simple energy calculation with GULP
to get adsorption energies for a given set of potentials.
```bash
python2 pysorb_compare.py -d examples/test.qedump -p examples/gulp_compare/model1.param -o examples/compare_run.gin
``` 

### Parameter optimisation with GULP

```bash
python2 pysorb_fit.py -d examples/test.qedump -p examples/gulp_compare/model1.param -o examples/fit_run.gin

# or

python2 pysorb_fit.py -d examples/test.qedump -p examples/gulp_compare/model1.param -o examples/fit_run.gin -w -t 310
```

### Run GULP

```bash
gulp < file.gin > file.gout
```