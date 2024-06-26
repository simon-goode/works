import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

public class SnakeGame extends JPanel implements ActionListener, KeyListener {
    private Timer t;
    private main parent;
    private Snake snake;
    public static final int WIDTH = 25;
    public static final int HEIGHT = 25;
    private static final int SQUARE_SIZE = 30;
    private int tick = 0;
    private Food f;
    private int score;


    SnakeGame(main parent){
        this.parent = parent;
        parent.addKeyListener(this);
        t = new Timer(30, this);

        snake = new Snake();
        f = GenerateRandomFood();
        t.start();
    }

    Food GenerateRandomFood(){
        int x = (int)(Math.random() * WIDTH);
        int y = (int)(Math.random() * HEIGHT);
        boolean safe = false;
        while(!safe){
            safe = true;
            for (Pair p: snake.nodes){
                if(p.x == x && p.y == y) safe = false;
            }
            if(!safe){
                x = (int)(Math.random() * WIDTH);
                y = (int)(Math.random() * HEIGHT);
            }
        }

        return new Food(x, y);
    }

    @Override
    public void paintComponent(Graphics g){
        g.setColor(Color.BLACK);
        g.fillRect(0, 0, 900, 922);

        g.setColor(Color.RED.darker().darker());
        for(Pair p: snake.nodes){
            g.fillRect(p.x * SQUARE_SIZE, p.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE);
        }

        g.setColor(Color.GREEN.darker().darker());
        g.fillRect(f.x * SQUARE_SIZE, f.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE);

        g.setColor(Color.GRAY);
        for (int i = 0; i < (Math.max(WIDTH, HEIGHT)); i++) {
            g.drawLine(0, i * SQUARE_SIZE, 900, i * SQUARE_SIZE);
            g.drawLine(i * SQUARE_SIZE, 0, i * SQUARE_SIZE, 922);
        }
    }

    void GameOver(){
        t.stop();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        tick++;
        if(tick == 3) {
            tick = 0;
            if (!snake.update()) {
                GameOver();
            }
            if(snake.nodes.get(0).x == f.x && snake.nodes.get(0).y == f.y){
                f = GenerateRandomFood();
                snake.max_length++;
                score++;
                parent.setTitle(String.valueOf(score));
            }
            repaint();
        }
    }

    @Override
    public void keyTyped(KeyEvent e) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        if(e.getKeyCode() == KeyEvent.VK_UP && snake.dy != 1){
            snake.dx = 0;
            snake.dy = -1;
        }else if(e.getKeyCode() == KeyEvent.VK_DOWN && snake.dy != -1){
            snake.dx = 0;
            snake.dy = 1;
        }else if(e.getKeyCode() == KeyEvent.VK_LEFT && snake.dx != 1){
            snake.dx = -1;
            snake.dy = 0;
        }else if(e.getKeyCode() == KeyEvent.VK_RIGHT && snake.dx != -1){
            snake.dx = 1;
            snake.dy = 0;
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {

    }
}
