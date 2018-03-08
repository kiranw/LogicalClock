# Logical Clock Experiment

By: Kiran Wattamwar and Mali Akmanalp

This is an experiment to see the changes in logical clocks across different
nodes in a distributed system depending on type and frequency of messages.

Please see the report for technical decisions and observations of results.

## Instructions to run

The only dependencies required to run the simulation is python 2.7 and the
matplotlib package for plotting the results.

To run the simulation, simply run `python setup.py`. This will run many
different experiment trials with different clock rates and message destination
probabilities - you can configure these in `trials.py`. The code will output
log files into folders named `trialXX/`.

Finally you can plot the logs by running `python plots.py`.

There is an included sample run of logs and plots that you can view in the
directory, if you like.
