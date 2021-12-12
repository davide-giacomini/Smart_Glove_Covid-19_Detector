package smartglove.View.ViewObservable;

import javafx.fxml.Initializable;
import smartglove.Controller.ControllerInterface.MainControllerListener;

import java.util.ArrayList;

public abstract class MainViewControllerObservable  implements Initializable {
    private static final ArrayList<MainControllerListener> mainControllerListeners = new ArrayList<>();

    public void notifyChange(String unit) {
        mainControllerListeners.forEach(mainControllerListener -> mainControllerListener.changeThermUnit(unit));
    }

    public void notifyStartDiagnosis() {
        mainControllerListeners.forEach(MainControllerListener::startDiagnosis);
    }

    public void addControllerListener(MainControllerListener mainControllerListener) {
        mainControllerListeners.add(mainControllerListener);
    }
}