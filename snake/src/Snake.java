import java.util.ArrayList;
import java.util.LinkedList;

public class Snake {
    int dx, dy;
    int max_length;
    LinkedList<Pair> nodes;

    Snake(){
        dx = 0;
        dy = 0;
        max_length = 3;
        nodes = new LinkedList<Pair>();
        nodes.add(new Pair(7, 7));
    }

    boolean update(){
        int x_ = nodes.get(0).x;
        int y_ = nodes.get(0).y;
        if(!(dx == 0 && dy == 0)) {
            nodes.addFirst(new Pair(x_ + dx, y_ + dy));
        }
        if(nodes.size() > max_length) nodes.removeLast();

        for (int i = 1; i < nodes.size(); i++) {
            if(nodes.get(i).x == nodes.get(0).x && nodes.get(i).y == nodes.get(0).y){
                return false;
            }
        }

        Pair p = nodes.get(0);
        return p.x >= 0 && p.x < SnakeGame.WIDTH && p.y >= 0 && p.y < SnakeGame.HEIGHT;
    }
}
