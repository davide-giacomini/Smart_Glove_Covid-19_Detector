package smartglove.Model;

public class Oximeter {
    private Status status;
    private int oxygen;
    private int confidence;
    private float heartRate;

    public Oximeter(Status status, int oxygen, int confidence, float heartRate) {
        this.status = status;
        this.oxygen = oxygen;
        this.confidence = confidence;
        this.heartRate = heartRate;
    }
}

enum Status {
    NO_OBJECT_DETECTED,
    OBJECT_DETECTED,
    OBJECT_NO_FINGER_DETECTED,
    FINGER_DETECTED
}
