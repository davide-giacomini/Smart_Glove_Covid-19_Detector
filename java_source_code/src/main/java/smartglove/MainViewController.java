package smartglove;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;
import javafx.scene.layout.*;

import java.net.URL;
import java.util.ResourceBundle;

public class MainViewController implements Initializable {

    @FXML
    private AnchorPane thermValuesAnchorPane;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        displayThermometerValues();
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