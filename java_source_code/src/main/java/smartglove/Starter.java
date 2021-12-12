package smartglove;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import smartglove.Controller.MainController;
import smartglove.View.MainViewController;

import java.io.IOException;
import java.util.Locale;
import java.util.Objects;
import java.util.ResourceBundle;

public class Starter extends Application {
    @Override
    public void start(Stage stage) throws IOException {

        // I shall call the file `strings_en_UK.properties` and fill it with properties
        // In the xml file, I call the properties through the percentage "%<name_properties>"
        ResourceBundle languageBundle = ResourceBundle.getBundle("language", new Locale("en", "US"));

        FXMLLoader loader = new FXMLLoader(Objects.requireNonNull(getClass().getClassLoader().getResource("mainview.fxml")), languageBundle);
        Scene scene = new Scene(loader.load(), 800, 600);
        stage.setTitle("Smart Glove Detector");
        stage.setScene(scene);
        stage.show();

        MainViewController mainViewController = loader.getController();
        new MainController(mainViewController);
    }

    public static void main(String[] args) {
        launch();
    }
}