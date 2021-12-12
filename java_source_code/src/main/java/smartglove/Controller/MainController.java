package smartglove.Controller;

import javafx.fxml.FXMLLoader;
import smartglove.Controller.ControllerInterface.MainControllerListener;
import smartglove.Model.Diagnosis;
import smartglove.Model.Oximeter;
import smartglove.Model.Thermometer;
import smartglove.View.MainViewController;

import java.util.ArrayList;

public class MainController implements MainControllerListener {
    private final Diagnosis diagnosis = new Diagnosis();
    private final Oximeter oximeter = new Oximeter();;
    private final Thermometer thermometer = new Thermometer();
    private final MainViewController mainViewController;
    private final DiagnosisController diagnosisController;

    public MainController(MainViewController mainViewController) {
        this.mainViewController = mainViewController;
        mainViewController.addControllerListener(this);

        diagnosisController = new DiagnosisController(diagnosis, thermometer, oximeter);

        this.mainViewController.bindThermometerValues(thermometer);
        this.mainViewController.bindOximeterValues(oximeter);
        this.mainViewController.bindDiagnosisValues(diagnosis);
    }

    @Override
    public void changeThermUnit(String unit) {
        switch (unit) {
            case "F" -> {
                thermometer.changeIntoFarheneit();
                diagnosis.changeIntoFarheneit();
            }
            case "C" -> {
                thermometer.changeIntoCelsius();
                diagnosis.changeIntoCelsius();
            }
            case "K" -> {
                thermometer.changeIntoKelvin();
                diagnosis.changeIntoKelvin();
            }
        }
    }

    @Override
    public void startDiagnosis() {
        diagnosisController.startDiagnosis();
    }

    /**
     * All the gets are synchronized with the Arduino code. For example, `values.get(0)` corresponds
     * to the arduino first values printed in the serial communication, `values.get(3)` corresponds to the
     * third, etc.
     * @param values all the values passed along the serial communication
     */
    public void fillValues(ArrayList<String> values) {
        if (thermometer.unitProperty().get().equals("F")) {
            thermometer.setObjectTemperature(Float.parseFloat(values.get(0)));
            thermometer.setAmbientTemperature(Float.parseFloat(values.get(3)));
        }
        else if (thermometer.unitProperty().get().equals("C")){
            thermometer.setObjectTemperature(Float.parseFloat(values.get(1)));
            thermometer.setAmbientTemperature(Float.parseFloat(values.get(4)));
        }
        else if (thermometer.unitProperty().get().equals("K")){
            thermometer.setObjectTemperature(Float.parseFloat(values.get(2)));
            thermometer.setAmbientTemperature(Float.parseFloat(values.get(5)));
        }

        Integer oxygen = Integer.valueOf(values.get(7));
        Float heartRate = Float.valueOf(values.get(9));

        oximeter.setStatus(Integer.parseInt(values.get(6)));
        oximeter.setOxygen(oxygen);
        oximeter.setHeartRate(heartRate);
        oximeter.setConfidence(Integer.parseInt(values.get(8)));

        mainViewController.updateChart(oxygen, heartRate);
    }
}
