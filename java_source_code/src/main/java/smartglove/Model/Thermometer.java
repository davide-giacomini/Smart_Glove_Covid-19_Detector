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

    public void changeIntoFarheneit() {
        if (unit.get().equals("C")) {
            objectTemperature.set(Math.round((objectTemperature.get() * 9 / 5 + 32)*100/100.00));
            ambientTemperature.set(Math.round((ambientTemperature.get() * 9 / 5 + 32)*100/100.0));
        }
        else if ( unit.get().equals("K")) {
            objectTemperature.set(Math.round(((objectTemperature.get() - 273.15) * 9 / 5 +32)*100/100.0));
            ambientTemperature.set(Math.round(((ambientTemperature.get() - 273.15) * 9 / 5 +32)*100/100.0));
        }

        unit.set("F");
    }

    public void changeIntoCelsius() {
        if (unit.get().equals("F")) {
            objectTemperature.set(Math.round(((objectTemperature.get() - 32) * 5 / 9)*100/100.0));
            ambientTemperature.set(Math.round(((ambientTemperature.get() - 32) * 5 / 9)*100/100.0));
        }
        else if ( unit.get().equals("K")) {
            objectTemperature.set(Math.round((objectTemperature.get() - 273.15)*100/100.0));
            ambientTemperature.set(Math.round((ambientTemperature.get() - 273.15)*100/100.0));
        }

        unit.set("C");
    }

    public void changeIntoKelvin() {
        if (unit.get().equals("C")) {
            objectTemperature.set(Math.round((objectTemperature.get() + 273.15)*100/100.0));
            ambientTemperature.set(Math.round((ambientTemperature.get() + 273.15)*100/100.0));
        }
        else if ( unit.get().equals("F")) {
            objectTemperature.set(Math.round(((objectTemperature.get() - 32.0) * 5 / 9 + 273.15)*100/100.0));
            ambientTemperature.set(Math.round(((ambientTemperature.get() - 32.0) * 5 / 9 + 273.15)*100/100.0));
        }

        unit.set("K");
    }
}
