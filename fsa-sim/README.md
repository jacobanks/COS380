# Deterministic Finite State Machine

## Usage

```bash
python3 dfsa-sim.py definition.txt input.txt
```

### Definition File

Formated as follows:

```
0,1,b 	# 0 represents the current state, 1 is the next state and 'b' is the value
1,2,a
#2			# The pound signifies the accepting state and then the state number
```

### Input File

Formated as follows:

```
Y baaa!
Y baaaaaa!
N abaaa!
```

