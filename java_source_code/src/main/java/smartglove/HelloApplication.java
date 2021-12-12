package smartglove;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.Locale;
import java.util.Objects;
import java.util.ResourceBundle;

public class HelloApplication extends Application {
    @Override
    public void start(Stage stage) throws IOException {

        // I shall call the file `strings_en_UK.properties` and fill it with properties
        // In the xml file, I call the properties through the percentage "%<name_properties>"
        ResourceBundle languageBundle = ResourceBundle.getBundle("language", new Locale("en", "US"));


        Parent root = FXMLLoader.load(Objects.requireNonNull(getClass().getClassLoader().getResource("mainview.fxml")), languageBundle);
        Scene scene = new Scene(root, 320, 240);
        stage.setTitle("Hello!");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}