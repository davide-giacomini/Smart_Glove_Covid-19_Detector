package smartglove;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.chart.XYChart;
import javafx.stage.Stage;
import smartglove.Controller.MainController;
import smartglove.View.MainViewController;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.*;

public class Starter extends Application {
    private final static ScheduledExecutorService scheduledExecutorService = Executors.newSingleThreadScheduledExecutor();

    @Override
    public void start(Stage stage) throws IOException {

        // I shall call the file `strings_en_UK.properties` and fill it with properties
        // In the xml file, I call the properties through the percentage "%<name_properties>"
        ResourceBundle languageBundle = ResourceBundle.getBundle("language", new Locale("en", "US"));

        FXMLLoader loader = new FXMLLoader(Objects.requireNonNull(getClass().getClassLoader().getResource("mainview.fxml")), languageBundle);
        Scene scene = new Scene(loader.load(), 1200, 800);
        stage.setTitle("Smart Glove Detector");
        stage.setScene(scene);
        stage.show();

        MainViewController mainViewController = loader.getController();
        MainController mainController = new MainController(mainViewController);

        // put dummy data onto graph per second
        Starter.scheduledExecutorService.scheduleAtFixedRate(() -> {

            ArrayList<String> values = simulateSerialReading();

            if (values!=null) {
                Platform.runLater(() -> mainController.fillValues(values));
            }

        }, 0, 200, TimeUnit.MILLISECONDS);
    }

    /**
     * I cannot use Arduino right now and I have to simulate a reading.
     * It simulates a reading through the serial communication.
     * @return an ArrayList with all the values of each sensor.
     */
    private ArrayList<String> simulateSerialReading() {
        ArrayList<String> values = new ArrayList<>();

        // get a random integer between 90-104
        values.add(String.valueOf(ThreadLocalRandom.current().nextFloat(90, 104)));
        values.add(String.valueOf(ThreadLocalRandom.current().nextFloat(35, 39)));
        values.add(String.valueOf(ThreadLocalRandom.current().nextFloat(35-273, 39-273)));
        values.add(String.valueOf(ThreadLocalRandom.current().nextFloat(50, 70)));
        values.add(String.valueOf(ThreadLocalRandom.current().nextFloat(20, 30)));
        values.add(String.valueOf(ThreadLocalRandom.current().nextFloat(20-273, 30-273)));
        values.add(String.valueOf(3));
        values.add(String.valueOf(ThreadLocalRandom.current().nextInt(96, 99)));
        values.add(String.valueOf(99));
        values.add(String.valueOf(ThreadLocalRandom.current().nextFloat(60, 120)));


        return values;
    }

    public static void main(String[] args) {
        launch();
    }
}