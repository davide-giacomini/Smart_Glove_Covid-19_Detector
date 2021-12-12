package smartglove.Model;

import javafx.beans.property.*;

public class Oximeter {
    private final StringProperty status = new SimpleStringProperty();
    private final IntegerProperty oxygen = new SimpleIntegerProperty();
    private final IntegerProperty confidence = new SimpleIntegerProperty();
    private final FloatProperty heartRate = new SimpleFloatProperty();

    public void setStatus(int status) {
        switch (status) {
            case 0:
                this.status.set(Status.NO_OBJECT_DETECTED.toString());
            case 1:
                this.status.set(Status.OBJECT_DETECTED.toString());
            case 2:
                this.status.set(Status.OBJECT_NO_FINGER_DETECTED.toString());
            case 3:
                this.status.set(Status.FINGER_DETECTED.toString());
            default:
                throw new IllegalArgumentException("The integer must be between 0 and 3.");
        }
    }

    public void setOxygen(int oxygen) {
        this.oxygen.set(oxygen);
    }

    public void setConfidence(int confidence) {
        this.confidence.set(confidence);
    }

    public void setHeartRate(float heartRate) {
        this.heartRate.set(heartRate);
    }
}

enum Status {
    NO_OBJECT_DETECTED("No object detected"),
    OBJECT_DETECTED("Object detected"),
    OBJECT_NO_FINGER_DETECTED("Object other than finger detected"),
    FINGER_DETECTED("Finger detected");

    private final String status;

    Status(String status) {
        this.status = status;
    }

    @Override
    public String toString() {
        return status;
    }
}
