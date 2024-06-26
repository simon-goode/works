import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.awt.image.BufferedImageOp;
import java.awt.image.ConvolveOp;
import java.awt.image.Kernel;
import java.util.ArrayList;

public class Window extends JPanel implements ActionListener {

    public static final int WIDTH = 800;
    public static final int HEIGHT = 800;
    public static final int SIZE = 1;
    public static final int MOVE_SPEED = 5;

    Timer t;
    ArrayList<Agent> agents;
    Driver parent;
    BufferedImage img;

    Window(Driver parent){
        setBackground(Color.BLACK);
        img = new BufferedImage(WIDTH, HEIGHT, BufferedImage.TYPE_BYTE_INDEXED);
        agents = new ArrayList<Agent>();
        this.parent = parent;
        for (int i = 0; i < 30000; i++) {
            double a = i / 5000.0 * Math.PI;
            agents.add(new Agent(WIDTH / 2 + (int)(Math.cos(a) * 100), HEIGHT / 2 + (int)(Math.sin(a) * 100), a + Math.PI / 2));
        }

        t = new Timer(1000/60, this);
        t.start();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        for(Agent a: agents){
            updateAgent(a, agents.indexOf(a));
        }

        Kernel kernel = new Kernel(3, 3, new float[] { 1f / 9.5f, 1f / 9.5f, 1f / 9.5f, 1f / 9.5f, 1f / 9.5f,
            1f / 9.5f, 1f / 9.5f, 1f / 9.5f, 1f / 9.5f});
        BufferedImageOp op = new ConvolveOp(kernel);
        img = op.filter(img, null);
        repaint();
    }

    public void updateAgent(Agent a, int i){
        int random = hash(a.y * WIDTH + a.x + hash(i));
        a.x += Math.cos(a.a) * MOVE_SPEED;
        a.y += Math.sin(a.a) * MOVE_SPEED;

        if(a.x < 0 || a.x > WIDTH || a.y < 0 || a.y > HEIGHT){
            a.x = Math.max(a.x, 0);
            a.x = Math.min(a.x, WIDTH);
            a.y = Math.max(a.y, 0);
            a.y = Math.min(a.y, HEIGHT);
            a.a = Math.random() * 2 * Math.PI;
        }
    }

    public void paintComponent(Graphics g){
//        g.setColor(Color.BLACK);
//        g.fillRect(0, 0, WIDTH, HEIGHT);
        for(Agent a: agents){
            displayAgent(a, g);
        }
        g.drawImage(img, 0, 0, this);
    }

    public void displayAgent(Agent a, Graphics g){
//        g.setColor(Color.WHITE);
//        g.fillRect(a.x, a.y, SIZE, SIZE);
        img.setRGB(boundX(a.x), boundY(a.y), 0xFFFFFF);
    }

    public int boundX(int x){
        return Math.min(WIDTH - 1, Math.max(1, x));
    }

    public int boundY(int y){
        return Math.min(HEIGHT - 1, Math.max(1, y));
    }

    public int hash(int n){
        long b = (long)n;
        b ^= 2747636419L;
        b *= 2654435769L;
        b ^= b >> 16;
        b *= 2654435769L;
        b ^= b >> 16;
        b *= 2654435769L;
        return (int)b;
    }
}
