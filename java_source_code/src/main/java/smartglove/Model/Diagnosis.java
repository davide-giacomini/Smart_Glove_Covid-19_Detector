package smartglove.Model;

import javafx.beans.property.*;

public class Diagnosis {
    private final IntegerProperty averageOxygen = new SimpleIntegerProperty(0);
    private final FloatProperty averageHeartRate = new SimpleFloatProperty(0);
    private final FloatProperty averageTemperature = new SimpleFloatProperty(0);
    private final StringProperty unit = new SimpleStringProperty("F");

    private final StringProperty labelDiagnosis = new SimpleStringProperty();
    private final BooleanProperty diagnosis = new SimpleBooleanProperty();

    public IntegerProperty averageOxygenProperty() {
        return averageOxygen;
    }

    public void setAverageOxygen(int averageOxygen) {
        this.averageOxygen.set(averageOxygen);
    }

    public FloatProperty averageHeartRateProperty() {
        return averageHeartRate;
    }

    public void setAverageHeartRate(float averageHeartRate) {
        this.averageHeartRate.set(averageHeartRate);
    }

    public FloatProperty averageTemperatureProperty() {
        return averageTemperature;
    }

    public void setAverageTemperature(float averageTemperature) {
        this.averageTemperature.set(averageTemperature);
    }

    public StringProperty unitProperty() {
        return unit;
    }

    public void setUnit(String unit) {
        this.unit.set(unit);
    }

    public StringProperty labelDiagnosisProperty() {
        return labelDiagnosis;
    }

    public void setLabelDiagnosis(String labelDiagnosis) {
        this.labelDiagnosis.set(labelDiagnosis);
    }

    public BooleanProperty diagnosisProperty() {
        return diagnosis;
    }

    public void setDiagnosis(boolean diagnosis) {
        this.diagnosis.set(diagnosis);
    }

    public void changeIntoFarheneit() {
        if (unit.get().equals("C")) {
            averageTemperature.set(Math.round((averageTemperature.get() * 9 / 5 + 32)*100/100.00));
        }
        else if ( unit.get().equals("K")) {
            averageTemperature.set(Math.round(((averageTemperature.get() - 273.15) * 9 / 5 +32)*100/100.0));
        }

        unit.set("F");
    }

    public void changeIntoCelsius() {
        if (unit.get().equals("F")) {
            averageTemperature.set(Math.round(((averageTemperature.get() - 32) * 5 / 9)*100/100.0));
        }
        else if ( unit.get().equals("K")) {
            averageTemperature.set(Math.round((averageTemperature.get() - 273.15)*100/100.0));
        }

        unit.set("C");
    }

    public void changeIntoKelvin() {
        if (unit.get().equals("C")) {
            averageTemperature.set(Math.round((averageTemperature.get() + 273.15)*100/100.0));
        }
        else if ( unit.get().equals("F")) {
            averageTemperature.set(Math.round(((averageTemperature.get() - 32.0) * 5 / 9 + 273.15)*100/100.0));
        }

        unit.set("K");
    }
}
