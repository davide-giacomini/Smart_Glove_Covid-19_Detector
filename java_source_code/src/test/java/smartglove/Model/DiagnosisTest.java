package smartglove.Model;

import javafx.beans.property.FloatProperty;
import javafx.beans.property.StringProperty;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.internal.util.reflection.Whitebox;

class DiagnosisTest {
    Diagnosis diagnosis;

    @BeforeEach
    void setUp() {
        diagnosis = new Diagnosis();
    }

    @AfterEach
    void tearDown() {
        diagnosis = null;
    }

    @Test
    void changeIntoFarheneit() {
        FloatProperty averageTemperature = (FloatProperty) Whitebox.getInternalState(diagnosis, "averageTemperature");
        StringProperty unit = (StringProperty) Whitebox.getInternalState(diagnosis, "unit");

        unit.setValue("C");
        averageTemperature.setValue(0);
        diagnosis.changeIntoFarheneit();
        Assertions.assertEquals(32, averageTemperature.getValue());

        unit.setValue("K");
        averageTemperature.setValue(300);
        diagnosis.changeIntoFarheneit();
        Assertions.assertEquals(80.0, (Math.round(averageTemperature.getValue())));
    }

    @Test
    void changeIntoCelsius() {
    }

    @Test
    void changeIntoKelvin() {
    }
}