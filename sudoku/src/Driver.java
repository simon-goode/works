import javax.swing.*;

public class Driver{

    BruteSolver brute_solver;

    Driver(){
        brute_solver = new BruteSolver(this);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(()->{
            Driver d = new Driver();
        });
    }
}
