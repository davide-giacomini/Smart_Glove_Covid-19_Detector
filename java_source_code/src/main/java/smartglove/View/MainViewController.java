package smartglove.View;

import javafx.beans.property.SimpleStringProperty;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.geometry.Insets;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.control.Label;
import javafx.scene.layout.*;
import smartglove.Model.Thermometer;

import java.net.URL;
import java.util.ResourceBundle;

public class MainViewController implements Initializable {

    @FXML
    private AnchorPane thermValuesAnchorPane;

    @FXML
    private AnchorPane lineChartAnchorPane;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        initChart();
    }

    private void initChart() {
        LineChart<Number, Number> lineChart = new LineChart<>(new NumberAxis(), new NumberAxis());

        lineChart.getXAxis().setLabel("Time");

        lineChartAnchorPane.getChildren().add(lineChart);
        AnchorPane.setBottomAnchor(lineChart, 0.0);
        AnchorPane.setTopAnchor(lineChart, 0.0);
        AnchorPane.setRightAnchor(lineChart, 0.0);
        AnchorPane.setLeftAnchor(lineChart, 0.0);
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
        objTempBorderPane.setPadding(new Insets(10,0,0,0));

        BorderPane ambTempBorderPane = new BorderPane();
        ambTempBorderPane.setCenter(labelAmbTemperature);
        ambTempBorderPane.setPadding(new Insets(10,0,0,0));

        VBox vBox = new VBox();
        VBox.setVgrow(objTempBorderPane, Priority.ALWAYS);
        vBox.getChildren().add(objTempBorderPane);
        VBox.setVgrow(ambTempBorderPane, Priority.ALWAYS);
        vBox.getChildren().add(ambTempBorderPane);

        thermValuesAnchorPane.getChildren().add(vBox);
//        AnchorPane.setBottomAnchor(vBox, 0.0);
        AnchorPane.setTopAnchor(vBox, 0.0);
        AnchorPane.setRightAnchor(vBox, 0.0);
        AnchorPane.setLeftAnchor(vBox, 0.0);
    }
}