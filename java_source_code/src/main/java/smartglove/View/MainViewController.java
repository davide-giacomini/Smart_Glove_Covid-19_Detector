package smartglove.View;

import javafx.beans.property.SimpleStringProperty;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.Priority;
import javafx.scene.layout.VBox;
import smartglove.Model.Diagnosis;
import smartglove.Model.Oximeter;
import smartglove.Model.Thermometer;
import smartglove.View.ViewObservable.MainViewControllerObservable;

import java.net.URL;
import java.text.DecimalFormat;
import java.util.ResourceBundle;

import static javafx.scene.paint.Color.BLACK;

public class MainViewController extends MainViewControllerObservable {

    private final DecimalFormat f = new DecimalFormat("##.00");

    @FXML
    private VBox thermVBox;
    @FXML
    private VBox oxVBox;
    @FXML
    private AnchorPane lineChartAnchorPane;
    @FXML
    private VBox diagVBox;
    @FXML
    private Label diagnosisLabel;
    @FXML
    private Button startDiagnosisButton;

    private final LineChart<Number, Number> lineChart = new LineChart<>(new NumberAxis(), new NumberAxis());

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        initChart();
    }

    private void initChart() {
        lineChart.setTitle("Heart Rate and Oxygen Saturation");

        lineChart.getXAxis().setLabel("Time [s]");
        lineChart.getXAxis().setTickMarkVisible(false);
        lineChart.getXAxis().setTickLabelsVisible(false);
        lineChart.getYAxis().setLabel("HR [BPM] and Oxg Sat [%]");
        lineChart.getYAxis().setTickLabelFill(BLACK);   // It doesn't work here or in the CSS

        lineChartAnchorPane.getChildren().add(lineChart);
        AnchorPane.setBottomAnchor(lineChart, 0.0);
        AnchorPane.setTopAnchor(lineChart, 0.0);
        AnchorPane.setRightAnchor(lineChart, 0.0);
        AnchorPane.setLeftAnchor(lineChart, 0.0);

        //defining a series to display heart rate
        XYChart.Series<Number, Number> hrSeries = new XYChart.Series<>();
        hrSeries.setName("Heart Rate");
        // add series to chart
        lineChart.getData().add(hrSeries);

        //defining a series to display oxygen
        XYChart.Series<Number, Number> oxgSeries = new XYChart.Series<>();
        oxgSeries.setName("Oxygen Saturation");
        // add series to chart
        lineChart.getData().add(oxgSeries);

        // Prepare a fixed time length of 20s
        for (int i=0; i<20; i++) {
            hrSeries.getData().add(new XYChart.Data<>(i, 0));
            oxgSeries.getData().add(new XYChart.Data<>(i,0));
        }
    }

    public void bindThermometerValues(Thermometer thermometer) {
        Label labelObjTemperature = new Label();
        labelObjTemperature.textProperty().
                bind(new SimpleStringProperty("Object Temperature: ")
                        .concat(thermometer.objectTemperatureProperty())
                        .concat(thermometer.unitProperty()));
        labelObjTemperature.getStyleClass().add("value-label");

        Label labelAmbTemperature = new Label();
        labelAmbTemperature.textProperty()
                .bind(new SimpleStringProperty("Ambient Temperature: ")
                        .concat(thermometer.ambientTemperatureProperty())
                        .concat(thermometer.unitProperty()));
        labelAmbTemperature.getStyleClass().add("value-label");

        BorderPane objTempBorderPane = new BorderPane();
        objTempBorderPane.setCenter(labelObjTemperature);

        BorderPane ambTempBorderPane = new BorderPane();
        ambTempBorderPane.setCenter(labelAmbTemperature);

        thermVBox.getChildren().add(0, objTempBorderPane);
        VBox.setVgrow(objTempBorderPane, Priority.ALWAYS);
        objTempBorderPane.setPadding(new Insets(10,0,0,0));
        thermVBox.getChildren().add(1, ambTempBorderPane);
        ambTempBorderPane.setPadding(new Insets(10,0,0,0));
        VBox.setVgrow(ambTempBorderPane, Priority.ALWAYS);
    }

    public void bindOximeterValues(Oximeter oximeter) {
        Label labelStatus = new Label();
        labelStatus.textProperty().
                bind(new SimpleStringProperty("Status: ")
                        .concat(oximeter.statusProperty()));
        labelStatus.getStyleClass().add("value-label");

        Label labelOxygen = new Label();
        labelOxygen.textProperty()
                .bind(new SimpleStringProperty("Oxygen saturation: ")
                        .concat(oximeter.oxygenProperty())
                        .concat(new SimpleStringProperty("%")));
        labelOxygen.getStyleClass().add("value-label");

        Label labelConfidence = new Label();
        labelConfidence.textProperty()
                .bind(new SimpleStringProperty("Confidence: ")
                        .concat(oximeter.oxygenProperty())
                        .concat(new SimpleStringProperty("%")));
        labelConfidence.getStyleClass().add("value-label");

        Label labelHeartRate = new Label();
        labelHeartRate.textProperty()
                .bind(new SimpleStringProperty("Heart Rate: ")
                        .concat(oximeter.heartRateProperty())
                        .concat(new SimpleStringProperty("BPM")));
        labelHeartRate.getStyleClass().add("value-label");

        BorderPane statusBorderPane = new BorderPane();
        statusBorderPane.setCenter(labelStatus);

        BorderPane oxygenBorderPane = new BorderPane();
        oxygenBorderPane.setCenter(labelOxygen);

        BorderPane confidenceBorderPane = new BorderPane();
        confidenceBorderPane.setCenter(labelConfidence);

        BorderPane heartRateBorderPane = new BorderPane();
        heartRateBorderPane.setCenter(labelHeartRate);

        oxVBox.getChildren().add(statusBorderPane);
        VBox.setVgrow(statusBorderPane, Priority.ALWAYS);
        statusBorderPane.setPadding(new Insets(10,0,0,0));
        oxVBox.getChildren().add(oxygenBorderPane);
        VBox.setVgrow(oxygenBorderPane, Priority.ALWAYS);
        oxygenBorderPane.setPadding(new Insets(10,0,0,0));
        oxVBox.getChildren().add(confidenceBorderPane);
        VBox.setVgrow(confidenceBorderPane, Priority.ALWAYS);
        confidenceBorderPane.setPadding(new Insets(10,0,0,0));
        oxVBox.getChildren().add(heartRateBorderPane);
        VBox.setVgrow(heartRateBorderPane, Priority.ALWAYS);
        heartRateBorderPane.setPadding(new Insets(10,0,0,0));
    }

    public void bindDiagnosisValues(Diagnosis diagnosis) {
        Label labelOxygen = new Label();
        labelOxygen.textProperty().
                bind(new SimpleStringProperty("Average Oxygen Sat: ")
                        .concat(diagnosis.averageOxygenProperty())
                        .concat(new SimpleStringProperty("%")));
        labelOxygen.getStyleClass().add("value-label");

        Label labelTemperature = new Label();
        labelTemperature.textProperty()
                .bind(new SimpleStringProperty("Average Temperature: ")
                        .concat(diagnosis.averageTemperatureProperty())
                        .concat(diagnosis.unitProperty()));
        labelTemperature.getStyleClass().add("value-label");

        Label labelHeartRate = new Label();
        labelHeartRate.textProperty()
                .bind(new SimpleStringProperty("Average Heart Rate: ")
                        .concat(diagnosis.averageHeartRateProperty())
                        .concat(new SimpleStringProperty("BPM")));
        labelHeartRate.getStyleClass().add("value-label");

        BorderPane statusBorderPane = new BorderPane();
        statusBorderPane.setCenter(labelOxygen);

        BorderPane oxygenBorderPane = new BorderPane();
        oxygenBorderPane.setCenter(labelTemperature);

        BorderPane confidenceBorderPane = new BorderPane();
        confidenceBorderPane.setCenter(labelHeartRate);

        diagVBox.getChildren().add(0, statusBorderPane);
        VBox.setVgrow(statusBorderPane, Priority.ALWAYS);
        statusBorderPane.setPadding(new Insets(10,0,0,0));
        diagVBox.getChildren().add(1, oxygenBorderPane);
        VBox.setVgrow(oxygenBorderPane, Priority.ALWAYS);
        oxygenBorderPane.setPadding(new Insets(10,0,0,0));
        diagVBox.getChildren().add(2, confidenceBorderPane);
        VBox.setVgrow(confidenceBorderPane, Priority.ALWAYS);
        confidenceBorderPane.setPadding(new Insets(10,0,0,0));


        startDiagnosisButton.disableProperty().bind(diagnosis.diagnosisProperty());
        diagnosisLabel.textProperty().bind(diagnosis.labelDiagnosisProperty());
    }

    @FXML
    private void thermometerFarhenheitChosen(ActionEvent actionEvent) {
        notifyChange("F");
    }

    @FXML
    private void thermometerCelsiusChosen(ActionEvent actionEvent) {
        notifyChange("C");
    }

    @FXML
    private void thermometerKelvinChosen(ActionEvent actionEvent) {
        notifyChange("K");
    }

    @FXML
    private void startDiagnosisAction(ActionEvent actionEvent) {
        diagnosisLabel.setVisible(true);
        notifyStartDiagnosis();
    }

    public void updateChart(Integer oxygen, Float heartRate) {
        ObservableList<XYChart.Data<Number, Number>> pointsHR = lineChart.getData().get(0).getData();
        ObservableList<XYChart.Data<Number, Number>> pointsOx = lineChart.getData().get(1).getData();

        for (int i=0; i<pointsHR.size()-1; i++) {
            pointsHR.get(i).setYValue(pointsHR.get(i+1).getYValue());
        }
        pointsHR.get(pointsHR.size()-1).setYValue(heartRate);

        for (int i=0; i<pointsOx.size()-1; i++) {
            pointsOx.get(i).setYValue(pointsOx.get(i+1).getYValue());
        }
        pointsOx.get(pointsOx.size()-1).setYValue(oxygen);
    }
}