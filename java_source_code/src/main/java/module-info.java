module smartglove.java_source_code {
    requires javafx.controls;
    requires javafx.fxml;

    opens smartglove to javafx.fxml;
    exports smartglove;
    exports smartglove.View;
    opens smartglove.View to javafx.fxml;
}