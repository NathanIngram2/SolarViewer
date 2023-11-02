# moving this method into the exp so it can be called by experiment scripts

def measPower(freq_min, freq_max, integration_interval):
    """
    Measure the power using rtl_power and return the mean power over all frequencies and time.

    :param freq_min: Minimum frequency for power measurement.
    :param freq_max: Maximum frequency for power measurement.
    :param integration_interval: Integration interval for SDR power measurement.
    :return: Mean power (dB) over all frequencies and time.
    """
    Log.info("Starting measPower with min: " + str(freq_min) + " max: " + str(freq_max) + " integration interval: "
             + integration_interval)

    command = ('rtl_power -f ' + str(freq_min) + ':' + str(freq_max) + ':128k -i ' + str(integration_interval)
               + ' -1 tmp/rtl_power_out.csv')
    Log.info("Executing command: " + str(command))

    # TODO: Parse rst for error message or nan. Log error.
    try:
        #rst = sp.run([command], shell=True, capture_output=True, text=True, check=True)
        rst = sp.run([command], shell=True, capture_output=True, text=True)
    except sp.CalledProcessError as e:
        Log.error("Error executing rtl_power command: " + str(e))
        return 0.0

    Log.info("Done rtl_power. Reading CSV...")
    raw = pd.read_csv("tmp/rtl_power_out.csv")
    proc = raw.iloc[:, 0:4]
    proc[len(proc.columns)] = raw.iloc[:, 6:-1].mean(axis=1)
    mean_all_freq_and_time = proc.iloc[:, 4].mean()

    Log.info("Power: " + str(mean_all_freq_and_time))
    Log.info("End measPower")

    return mean_all_freq_and_time