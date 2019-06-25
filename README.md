# Work shifts

## Motivation
Sometimes we need to divide certain tasks among a group of collectives, so that
everyone pulls their fair share of the work while at the same time not
overworking themselves.

This simple script does this using a greedy algorithm (not necessarily
optimal), according to the following criteria:
* Each task has a weight, according to how exhausting it is.
* Each time of the day in which a task is performed has a weight according to
  how long the task is being performed.
* Each shift (i.e. each task fulfilled at a certain time) has a weight which is
  a combination of the weight of the task itself and the weight of the time it
  is being fulfilled.
* Each group should do tasks which roughly sum the same weight.
* Each group should not be overworked in a single day if it can be avoided.
  Their workload should be spread over the whole schedule.

## Customization
In order to customize this script for your cases, modify the variables and the
enums at the top of the script.

## Limitations
It is a greedy algorithm, which works fine with shifts of similar weight. The
more unequeal the weights, the more likely it is to perform badly.

## Possible improvements
This problem is a generalization of the partition problem with K (number of
sets) larger than 2. Researching this problem might shed light on better
algorithms.
