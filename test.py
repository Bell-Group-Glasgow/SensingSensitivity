def manu_convert(x):
    pulse_volume = 1/30 * 0.01
        
    # To get ml/sec to pulse per sec:
    pulse_per_sec = x/pulse_volume
    return int(pulse_per_sec)

def nicola_convert(x):
    return x/0.02

print(manu_convert(5/60), nicola_convert(5))