package smartglove.Controller;

import smartglove.Model.Diagnosis;
import smartglove.Model.Oximeter;
import smartglove.Model.Thermometer;
import smartglove.View.MainViewController;

public class MainController {
    private final Diagnosis diagnosis = new Diagnosis(0, 0, 0);
    private final Oximeter oximeter = new Oximeter();;
    private final Thermometer thermometer = new Thermometer();
    private final MainViewController mainViewController;

    public MainController(MainViewController mainViewController) {
        this.mainViewController = mainViewController;
        this.mainViewController.bindThermometerValues(thermometer);
    }
}
