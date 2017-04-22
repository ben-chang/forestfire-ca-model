import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.image.BufferedImage;
import java.util.HashMap;

class FuelPatchDrawer extends JPanel implements MouseListener, MouseMotionListener{

    private final static int SQUARE_SHAPE_CODE = 0;
    final static int CIRCULAR_SHAPE_CODE = 1;
    private final int height;
    private final int width;
    private int brushSize;
    private int brushShape;
    private int fuelChoice;
    private int[][] valueMatrix;
    private BufferedImage chachedImage;
    private final HashMap<Integer, Triple3<Integer>> fuelColorMap;
    static final HashMap<Integer, Triple3<Integer>> DEFAULT_FUEL_COLOR_MAP;
    static {
        DEFAULT_FUEL_COLOR_MAP = new HashMap<Integer, Triple3<Integer>>(){
            {
                put(0, new Triple3<>(128, 128, 128));
                put(1, new Triple3<>(255, 255, 153));
                put(2, new Triple3<>(255, 255, 102));
                put(3, new Triple3<>(204, 204, 0));
                put(4, new Triple3<>(0, 255, 0));
                put(5, new Triple3<>(0, 102, 0));
                put(6, new Triple3<>(0, 51, 0));
                put(7, new Triple3<>(0, 102, 51));
                put(8, new Triple3<>(0, 51, 25));
                put(9, new Triple3<>(102, 51, 0));
                put(10, new Triple3<>(51, 25, 0));
            }
        };
    }

    FuelPatchDrawer (int width, int height, int brushSize, int brushShape,
                     HashMap<Integer, Triple3<Integer>> fuelColorMap,
                     int startingFuelType) {
        this.width = width;
        this.height = height;
        this.valueMatrix = makeHomogeneousIntArray(width, height, startingFuelType);
        this.brushSize = brushSize;
        this.brushShape = brushShape;
        this.fuelColorMap = fuelColorMap;
        this.fuelChoice = startingFuelType;
        addMouseListener(this);
        addMouseMotionListener(this);
        setSize(width, height);
    }

    private static int[][] makeHomogeneousIntArray(int width, int height,
                                                   int fillValue){
        final int[][] homogeneousArray = new int[height][width];
        for (int i = 0; i < height; i++){
            for (int j = 0; j < width; j++) {
                homogeneousArray[i][j] = fillValue;
            }
        }
        return homogeneousArray;
    }

    private static boolean isInCircle(int centerX, int centerY, int radiusSquare, int x, int y) {
        final int deltaX = centerX - x; final int deltaY = centerY - y;
        final int squareDist = deltaX * deltaX + deltaY * deltaY;
        return squareDist <= radiusSquare;
    }

    private void updateMatrix(int eventX, int eventY){
        final int startX = eventX - brushSize;
        final int startY = eventY - brushSize;
        final int endX = eventX + brushSize;
        final int endY = eventY + brushSize;
        for (int y = startY; y < endY+1; y++) {
            for (int x = startX; x < endX+1; x++) {
                try {
                    if (brushShape == SQUARE_SHAPE_CODE) {
                        valueMatrix[y][x] = fuelChoice;
                    } else {
                        final int radiusSquare = brushSize * brushSize;
                        if (isInCircle(eventX, eventY, radiusSquare, x, y)){
                            valueMatrix[y][x] = fuelChoice;
                        }
                    }

                } catch (ArrayIndexOutOfBoundsException e) {
                    //System.out.println("Painting out of array bounds...");
                }

            }
        }
    }

    private BufferedImage drawImage () {
        BufferedImage cachedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                Triple3<Integer> rbgCode = fuelColorMap.get(valueMatrix[y][x]);
                Color col = new Color(rbgCode.getF1(),
                                      rbgCode.getF2(),
                                      rbgCode.getF3());

                cachedImage.setRGB(x, y, col.getRGB());
            }
        }
        return cachedImage;
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        BufferedImage img = drawImage();
        g.drawImage(img, 0, 0, null);
    }

    @Override
    public void mouseClicked(MouseEvent e) {
        updateMatrix(e.getX(), e.getY());
        repaint();
    }

    @Override
    public void mousePressed(MouseEvent e) {
        updateMatrix(e.getX(), e.getY());
        repaint();
    }

    @Override
    public void mouseReleased(MouseEvent e) {

    }

    @Override
    public void mouseEntered(MouseEvent e) {

    }

    @Override
    public void mouseExited(MouseEvent e) {

    }

    @Override
    public void mouseDragged(MouseEvent e) {
        updateMatrix(e.getX(), e.getY());
        repaint();
    }

    @Override
    public void mouseMoved(MouseEvent e) {

    }

    void setFueltype(int newChoice) {
        fuelChoice = newChoice;
    }

    void setBrushSize(int newSize){
        this.brushSize = newSize;
    }

    void setBrushShape(int brushShape){
        this.brushShape = brushShape;
    }

    int[][] getValueMatrix() {
        return valueMatrix;
    }

    void emptyMatrix() {
        valueMatrix = makeHomogeneousIntArray(width, height, 0);
        repaint();
    }
}