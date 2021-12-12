package smartglove.Controller;

import javafx.application.Platform;
import smartglove.Model.Diagnosis;
import smartglove.Model.Oximeter;
import smartglove.Model.Thermometer;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Timer;
import java.util.TimerTask;

public class DiagnosisController {
    private final Diagnosis diagnosis;
    private final Thermometer thermometer;
    private final Oximeter oximeter;
    private long startTimeDiagnosis;
    private ArrayList<Float> avgHeartRateArray;
    private ArrayList<Integer> avgOxygenArray;
    private ArrayList<Float> avgTempArray;
    private boolean oxgValidated = true;


    public DiagnosisController(Diagnosis diagnosis, Thermometer thermometer, Oximeter oximeter) {
        this.diagnosis = diagnosis;
        this.thermometer = thermometer;
        this.oximeter = oximeter;
    }

    public void startDiagnosis() {
        startTimeDiagnosis = System.currentTimeMillis();
        diagnosis.setDiagnosis(true);
        avgHeartRateArray = new ArrayList<>();
        avgTempArray = new ArrayList<>();
        avgOxygenArray = new ArrayList<>();

        Timer timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                long currentTime = System.currentTimeMillis() - startTimeDiagnosis;
                if (currentTime <= 10000) {
                    if (oximeter.statusProperty().getValue()==null || !oximeter.statusProperty().get().equals("Finger detected"))
                        oxgValidated = false;

                    Float heartRate = oximeter.heartRateProperty().getValue();
                    Integer oxygen = oximeter.oxygenProperty().getValue();
                    Float temp = thermometer.objectTemperatureProperty().getValue();

                    avgHeartRateArray.add(heartRate==null ? 0 : heartRate);
                    avgOxygenArray.add(oxygen==null ? 0 : oxygen);
                    avgTempArray.add(temp==null ? 0 : temp);
                    Platform.runLater(() -> diagnosis.setLabelDiagnosis("Calculating average:\nWait for " + (10 - currentTime/1000) + "s"));
                }
                else {
                    Platform.runLater(() -> {
                        diagnosis.setAverageHeartRate((avgHeartRateArray.stream().reduce(Float::sum).orElse((float) 0))/avgHeartRateArray.size());
                        diagnosis.setAverageOxygen(oxgValidated ? (avgOxygenArray.stream().reduce(Integer::sum).orElse(0))/avgOxygenArray.size() : 0);
                        diagnosis.setAverageTemperature((avgTempArray.stream().reduce(Float::sum).orElse((float) 0))/avgTempArray.size());
                        diagnosis.setDiagnosis(false);
                        updateFinalDiagnosis();
                    });
                }
            }
        }, 0, 100);
    }

    private void updateFinalDiagnosis() {
        if (oxgValidated && diagnosis.averageOxygenProperty().get() < 95)
            diagnosis.setLabelDiagnosis("Oxygen too low!\\nPatient should be treated!");
        else if (thermometer.unitProperty().get().equals("C") && diagnosis.averageTemperatureProperty().get() > 38
                || thermometer.unitProperty().get().equals("F") && diagnosis.averageTemperatureProperty().get() > 100.4
                || thermometer.unitProperty().get().equals("K") && diagnosis.averageTemperatureProperty().get() > 38 + 273.15)
            diagnosis.setLabelDiagnosis("Temperature too high.\\nIt is suggested a Covid Test.");
        else
            diagnosis.setLabelDiagnosis("Parameters correct.\nThe patient is healthy");
    }
}
