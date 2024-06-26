import javax.swing.*;

public class Driver extends JFrame{

    Driver(){
        Window w = new Window(this);
        add(w);

        setSize(Window.WIDTH, Window.HEIGHT + 37);
        setVisible(true);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(()->{
            Driver d = new Driver();
        });
    }
}
