package smartglove;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.control.Label;
import javafx.scene.layout.*;

import java.net.URL;
import java.util.ResourceBundle;

public class MainViewController implements Initializable {

    @FXML
    private AnchorPane thermValuesAnchorPane;

    @FXML
    private AnchorPane lineChartAnchorPane;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        displayThermometerValues();
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

    private void displayThermometerValues() {
        Label label = new Label();
        label.setText("prova: 34%");
        label.getStyleClass().add("value-label");

        BorderPane valuesBorderPane = new BorderPane();
        valuesBorderPane.setCenter(label);

        VBox vBox = new VBox();
        VBox.setVgrow(valuesBorderPane, Priority.ALWAYS);
        vBox.getChildren().add(valuesBorderPane);
        vBox.getStyleClass().add("ciao");

        thermValuesAnchorPane.getChildren().add(vBox);
        AnchorPane.setBottomAnchor(vBox, 0.0);
        AnchorPane.setTopAnchor(vBox, 0.0);
        AnchorPane.setRightAnchor(vBox, 0.0);
        AnchorPane.setLeftAnchor(vBox, 0.0);
    }
}