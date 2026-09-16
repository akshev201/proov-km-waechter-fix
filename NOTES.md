# What I checked, and what the agent got wrong


## What the agent got wrong
analyze.py initally opened the CSV and crashed.

## What I checked before I accepted its work
I ran verify.py and many of the constants stayed untouched. 

## What the data actually said
Milage and age are identical between broken and working cars. They are useless info, just misleading. The real signals are km_since_service and load_factor.
