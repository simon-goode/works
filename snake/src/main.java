import javax.swing.*;

public class main extends JFrame {
    private SnakeGame game;

    main(){
        game = new SnakeGame(this);
        add(game);

        setSize(764, 787);
        setVisible(true);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
    }


    public static void main(String[] args) {
        SwingUtilities.invokeLater(()->{
           main m = new main();
        });
    }
}
