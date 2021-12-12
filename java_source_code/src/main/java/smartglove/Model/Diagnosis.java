package smartglove.Model;

public class Diagnosis {
    private int averageOxygen;
    private float averageHeartRate;
    private float averageTemperature;

    public Diagnosis(int averageOxygen, float averageHeartRate, float averageTemperature) {
        this.averageOxygen = averageOxygen;
        this.averageHeartRate = averageHeartRate;
        this.averageTemperature = averageTemperature;
    }
}
