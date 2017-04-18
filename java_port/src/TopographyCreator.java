/** Written by Matayas Boros 4-18-2017 **/

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.image.BufferedImage;

class TopographyCreator extends JPanel implements MouseListener, MouseMotionListener {

    private final static int SQUARE_SHAPE_CODE = 0;
    final static int CIRCULAR_SHAPE_CODE = 1;
    private final int height;
    private final int width;
    private final double max;
    private final double min;
    private double brushIntensity;
    private int brushSize;
    private int brushShape;
    private double[][] valueMatrix;


    TopographyCreator (int width, int height, double min, double max,
                       double brushIntensity, int brushSize, int brushShape){
        this.width = width;
        this.height = height;
        this.valueMatrix = makeHomogeneousDoubleArray(width, height, min);
        this.min = min;
        this.max = max;
        this.brushIntensity = brushIntensity;
        this.brushSize = brushSize;
        this.brushShape = brushShape;
        addMouseListener(this);
        addMouseMotionListener(this);
        setSize(width, height);
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
        System.out.println("event at: x="+e.getX()+" y="+e.getY());
        updateMatrix(e.getX(), e.getY());
        repaint();
    }

    @Override
    public void mouseMoved(MouseEvent e) {

    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        BufferedImage img = drawImage();
        g.drawImage(img, 0, 0, null);

    }

    private BufferedImage drawImage () {
        BufferedImage cachedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        int redStart = 0, redEnd = 255;
        int greenStart = 0, greenEnd = 255;
        int blueStart = 0, blueEnd = 255;
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                Triple3<Integer, Integer, Integer> rbgCode;
                rbgCode = calculateColor(redStart, redEnd,
                                         greenStart, greenEnd,
                                         blueStart, blueEnd,
                                         valueMatrix[y][x],
                                         min, max, 20);
                Color col = new Color(rbgCode.getF1(),
                                      rbgCode.getF2(),
                                      rbgCode.getF3());

                cachedImage.setRGB(x, y, col.getRGB());
            }
        }
        return cachedImage;
    }

    private static Triple3<Integer, Integer, Integer> calculateColor(int rStart, int rEnd, int gStart,
                                                                     int gEnd, int bStart, int bEnd,
                                                                     double val, double min, double max,
                                                                     int classes) {
        double gradient = (max - min) / (double) classes;
        int colorClass = (int) ((val - min) / gradient);
        return new Triple3<>(rStart - (colorClass * ((rStart - rEnd) / classes)),
                gStart - (colorClass * ((gStart - gEnd) / classes)),
                bStart - (colorClass * ((bStart - bEnd) / classes)));
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
                        valueMatrix[y][x] = Math.min(max, valueMatrix[y][x] + brushIntensity);
                        valueMatrix[y][x] = Math.max(min, valueMatrix[y][x]);
                    } else {
                        final int radiusSquare = brushSize * brushSize;
                        if (isInCircle(eventX, eventY, radiusSquare, x, y)){
                            valueMatrix[y][x] = Math.min(max, valueMatrix[y][x] + brushIntensity);
                            valueMatrix[y][x] = Math.max(min, valueMatrix[y][x]);
                        }
                    }

                } catch (ArrayIndexOutOfBoundsException e) {
                    //System.out.println("Painting out of array bounds...");
                }

            }
        }
    }

    private static boolean isInCircle(int centerX, int centerY, int radiusSquare, int x, int y) {
        final int deltaX = centerX - x; final int deltaY = centerY - y;
        final int squareDist = deltaX * deltaX + deltaY * deltaY;
        return squareDist <= radiusSquare;
    }

    private static double[][] makeHomogeneousDoubleArray(int width, int height,
                                                         double fillValue){
        final double[][] homogeneousArray = new double[height][width];
        for (int i = 0; i < height; i++){
            for (int j = 0; j < width; j++) {
                homogeneousArray[i][j] = fillValue;
            }
        }
        return homogeneousArray;
    }

    void setBrushIntensity(double newIntensity) {
        this.brushIntensity = newIntensity;
    }

    public void setBrushSize(int newSize){
        this.brushSize = newSize;
    }

    void setBrushShape(int brushShape){
        this.brushShape = brushShape;
    }

    double[][] getValueMatrix() {
        return valueMatrix;
    }

    void emptyMatrix() {
        valueMatrix = makeHomogeneousDoubleArray(width, height, min);
        repaint();
    }
}