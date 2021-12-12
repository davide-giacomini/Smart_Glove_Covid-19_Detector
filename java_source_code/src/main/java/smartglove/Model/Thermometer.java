package smartglove.Model;

import javafx.beans.property.FloatProperty;
import javafx.beans.property.SimpleFloatProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;

public class Thermometer {
    private final FloatProperty objectTemperature = new SimpleFloatProperty(0);
    private final FloatProperty ambientTemperature = new SimpleFloatProperty(0);
    private final StringProperty unit = new SimpleStringProperty("F");

    public FloatProperty objectTemperatureProperty() {
        return objectTemperature;
    }

    public void setObjectTemperature(float objectTemperature) {
        this.objectTemperature.set(objectTemperature);
    }

    public FloatProperty ambientTemperatureProperty() {
        return ambientTemperature;
    }

    public void setAmbientTemperature(float ambientTemperature) {
        this.ambientTemperature.set(ambientTemperature);
    }
    public StringProperty unitProperty() {
        return unit;
    }

    public void setUnit(String unit) {
        this.unit.set(unit);
    }
}
