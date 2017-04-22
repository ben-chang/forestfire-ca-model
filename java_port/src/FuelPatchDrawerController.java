import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class FuelPatchDrawerController extends JFrame implements ActionListener {

    final int width, height;
    private JButton saveButton, startButton, deleteButton;
    private JButton squareBrushShapeButton, circularBrushShapeButton;
    private JTextField widthEntry, heightEntry, brushSizeEntry;

    private JLabel fuelLabel0, fuelLabel1, fuelLabel2, fuelLabel3, fuelLabel4;
    private JLabel fuelLabel5, fuelLabel6, fuelLabel7, fuelLabel8, fuelLabel9, fuelLabel10;

    private JButton fuelButton0, fuelButton1, fuelButton2, fuelButton3, fuelButton4;
    private JButton fuelButton5, fuelButton6, fuelButton7, fuelButton8, fuelButton9, fuelButton10;

    private JLabel brushShapeText, brushSizeText;
    private JLabel widthLabel, heightLabel;
    private JButton changeBrushSizeButton;
    private FuelPatchDrawer canvas;
    private JLabel fakeLabel1, fakeLabel2, fakeLabel3, fakeLabel4;
    private JLabel fakeLabel5, fakeLabel6, fakeLabel7, fakeLabel8;
    private JLabel fakeLabel9, fakeLabel10, fakeLabel11, fakeLabel12, fakeLabel13;
    private boolean hasCanvas = false;

    private FuelPatchDrawerController(int width, int height) {
        this.height = height;
        this.width = width;
        Container cp = getContentPane();
        cp.setLayout(new GridLayout(16, 3, 4, 4));


        this.widthLabel = new JLabel("Width:");
        this.widthEntry = new JTextField("0");
        this.fakeLabel1 = new JLabel("");
        cp.add(widthLabel);
        cp.add(widthEntry);
        cp.add(fakeLabel1);

        this.heightLabel = new JLabel("Height:");
        this.heightEntry = new JTextField("0");
        this.fakeLabel2 = new JLabel("");
        cp.add(heightLabel);
        cp.add(heightEntry);
        cp.add(fakeLabel2);

        this.fuelLabel0 = new JLabel("fuel type 0 (0.0 m/s)");
        this.fuelButton0 = new JButton("Choose!");
        this.fakeLabel3 = new JLabel("");
        Triple3<Integer> rbg0 = FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP.get(0);
        fuelButton0.setBackground(new Color(rbg0.getF1(), rbg0.getF2(), rbg0.getF3()));
        fuelButton0.setOpaque(true);
        fuelButton0.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setFueltype(0);
            }
        });
        cp.add(fuelLabel0);
        cp.add(fuelButton0);
        cp.add(fakeLabel3);

        this.fuelLabel1 = new JLabel("fuel type 1 (0.1 m/s)");
        this.fuelButton1 = new JButton("Choose!");
        this.fakeLabel4 = new JLabel("");
        Triple3<Integer> rbg = FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP.get(1);
        fuelButton1.setBackground(new Color(rbg.getF1(), rbg.getF2(), rbg.getF3()));
        fuelButton1.setOpaque(true);
        fuelButton1.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setFueltype(1);
            }
        });
        cp.add(fuelLabel1);
        cp.add(fuelButton1);
        cp.add(fakeLabel4);

        this.fuelLabel2 = new JLabel("fuel type 2 (0.2 m/s)");
        this.fuelButton2 = new JButton("Choose!");
        this.fakeLabel5 = new JLabel("");
        Triple3<Integer> rbg2 = FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP.get(2);
        fuelButton2.setBackground(new Color(rbg2.getF1(), rbg2.getF2(), rbg2.getF3()));
        fuelButton2.setOpaque(true);
        fuelButton2.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setFueltype(2);
            }
        });
        cp.add(fuelLabel2);
        cp.add(fuelButton2);
        cp.add(fakeLabel5);

        this.fuelLabel3 = new JLabel("fuel type 3 (0.3 m/s)");
        this.fuelButton3 = new JButton("Choose!");
        this.fakeLabel6 = new JLabel("");
        Triple3<Integer> rbg3 = FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP.get(3);
        fuelButton3.setBackground(new Color(rbg3.getF1(), rbg3.getF2(), rbg3.getF3()));
        fuelButton3.setOpaque(true);
        fuelButton3.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setFueltype(3);
            }
        });
        cp.add(fuelLabel3);
        cp.add(fuelButton3);
        cp.add(fakeLabel6);

        this.fuelLabel4 = new JLabel("fuel type 4 (0.4 m/s)");
        this.fuelButton4 = new JButton("Choose!");
        this.fakeLabel7 = new JLabel("");
        Triple3<Integer> rbg4 = FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP.get(4);
        fuelButton4.setBackground(new Color(rbg4.getF1(), rbg4.getF2(), rbg4.getF3()));
        fuelButton4.setOpaque(true);
        fuelButton4.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setFueltype(4);
            }
        });
        cp.add(fuelLabel4);
        cp.add(fuelButton4);
        cp.add(fakeLabel7);

        this.fuelLabel5 = new JLabel("fuel type 5 (0.5 m/s)");
        this.fuelButton5 = new JButton("Choose!");
        this.fakeLabel8 = new JLabel("");
        Triple3<Integer> rbg5 = FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP.get(5);
        fuelButton5.setBackground(new Color(rbg5.getF1(), rbg5.getF2(), rbg5.getF3()));
        fuelButton5.setOpaque(true);
        fuelButton5.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setFueltype(5);
            }
        });
        cp.add(fuelLabel5);
        cp.add(fuelButton5);
        cp.add(fakeLabel8);

        this.fuelLabel6 = new JLabel("fuel type 6 (0.6 m/s)");
        this.fuelButton6 = new JButton("Choose!");
        this.fakeLabel9 = new JLabel("");
        Triple3<Integer> rbg6 = FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP.get(6);
        fuelButton6.setBackground(new Color(rbg6.getF1(), rbg6.getF2(), rbg6.getF3()));
        fuelButton6.setOpaque(true);
        fuelButton6.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setFueltype(6);
            }
        });
        cp.add(fuelLabel6);
        cp.add(fuelButton6);
        cp.add(fakeLabel9);

        this.fuelLabel7 = new JLabel("fuel type 7 (0.7 m/s)");
        this.fuelButton7 = new JButton("Choose!");
        this.fakeLabel10 = new JLabel("");
        Triple3<Integer> rbg7 = FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP.get(7);
        fuelButton7.setBackground(new Color(rbg7.getF1(), rbg7.getF2(), rbg7.getF3()));
        fuelButton7.setOpaque(true);
        fuelButton7.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setFueltype(7);
            }
        });
        cp.add(fuelLabel7);
        cp.add(fuelButton7);
        cp.add(fakeLabel10);

        this.fuelLabel8 = new JLabel("fuel type 8 (0.8 m/s)");
        this.fuelButton8 = new JButton("Choose!");
        this.fakeLabel11 = new JLabel("");
        Triple3<Integer> rbg8 = FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP.get(8);
        fuelButton8.setBackground(new Color(rbg8.getF1(), rbg8.getF2(), rbg8.getF3()));
        fuelButton8.setOpaque(true);
        fuelButton8.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setFueltype(8);
            }
        });
        cp.add(fuelLabel8);
        cp.add(fuelButton8);
        cp.add(fakeLabel11);

        this.fuelLabel9 = new JLabel("fuel type 9 (0.9 m/s)");
        this.fuelButton9 = new JButton("Choose!");
        this.fakeLabel12 = new JLabel("");
        Triple3<Integer> rbg9 = FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP.get(9);
        fuelButton9.setBackground(new Color(rbg9.getF1(), rbg9.getF2(), rbg9.getF3()));
        fuelButton9.setOpaque(true);
        fuelButton9.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setFueltype(9);
            }
        });
        cp.add(fuelLabel9);
        cp.add(fuelButton9);
        cp.add(fakeLabel12);

        this.fuelLabel10 = new JLabel("fuel type 10 (1.0 m/s)");
        this.fuelButton10 = new JButton("Choose!");
        this.fakeLabel13 = new JLabel("");
        Triple3<Integer> rbg10 = FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP.get(10);
        fuelButton10.setBackground(new Color(rbg10.getF1(), rbg10.getF2(), rbg10.getF3()));
        fuelButton10.setOpaque(true);
        fuelButton10.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setFueltype(10);
            }
        });
        cp.add(fuelLabel10);
        cp.add(fuelButton10);
        cp.add(fakeLabel13);

        this.brushSizeEntry = new JTextField("0");
        this.brushSizeText = new JLabel("Brush Size:");
        this.changeBrushSizeButton = new JButton("Apply!");
        changeBrushSizeButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                final int newSize = Integer.parseInt(brushSizeEntry.getText());
                canvas.setBrushSize(newSize);
            }
        });
        cp.add(brushSizeText);
        cp.add(brushSizeEntry);
        cp.add(changeBrushSizeButton);

        this.brushShapeText = new JLabel("Choose Brush Shape:");
        this.squareBrushShapeButton = new JButton("square brush shape");
        this.circularBrushShapeButton = new JButton("circular brush shape");
        squareBrushShapeButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setBrushShape(0);
            }
        });
        circularBrushShapeButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.setBrushShape(1);
            }
        });
        cp.add(brushShapeText);
        cp.add(squareBrushShapeButton);
        cp.add(circularBrushShapeButton);

        this.saveButton = new JButton("save drawing");
        this.deleteButton = new JButton("delete drawing");
        this.startButton = new JButton("start drawing");

        startButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

                final int canvasHeight = Integer.parseInt(heightEntry.getText());
                final int canvasWidth = Integer.parseInt(widthEntry.getText());
                final int brushSize = Integer.parseInt(brushSizeEntry.getText());
                //final int startingFuel =
                canvas = new FuelPatchDrawer(canvasWidth, canvasHeight, brushSize,
                        FuelPatchDrawer.CIRCULAR_SHAPE_CODE, FuelPatchDrawer.DEFAULT_FUEL_COLOR_MAP,
                        0);
                JFrame canvasContainer = new JFrame();
                Container cp = canvasContainer.getContentPane();
                cp.setLayout(new BorderLayout());
                cp.add(canvas, BorderLayout.CENTER);
                canvasContainer.setTitle("Drawing Canvas");
                canvasContainer.setSize(canvasWidth, canvasHeight);
                canvasContainer.setVisible(true);
                hasCanvas = true;
            }
        });

        deleteButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                canvas.emptyMatrix();
            }
        });

        saveButton.addActionListener(this);

        cp.add(startButton);
        cp.add(deleteButton);
        cp.add(saveButton);

        setTitle("Fuel Patch Drawer Demo");
        setSize(width, height);
        setVisible(true);
    }

    private void writeToFile(String toPath, int[][] valueMatrix) {
        try {
            System.out.println(valueMatrix[0].length + " " + valueMatrix.length);
            System.out.println(valueMatrix[valueMatrix.length - 1][valueMatrix[0].length - 1] + " " + valueMatrix.length);
            BufferedWriter out = new BufferedWriter(new FileWriter(toPath));

            final String[] firstLines = {
                    "ncols         " + Integer.toString(valueMatrix[0].length),
                    "nrows         " + Integer.toString(valueMatrix.length),
                    "xllcorner     0",
                    "yllcorner     0",
                    "cellsize      0",
                    "NODATA_value  -9999"
            };

            for (int i = 0; i < valueMatrix.length + firstLines.length; i++) {
                if (i < firstLines.length) {
                    out.write(firstLines[i]);
                    out.newLine();
                } else {
                    String line = "";
                    for (int j = 0; j < valueMatrix[0].length; j++) {
                        line += Integer.toString(valueMatrix[i - firstLines.length][j]) + " ";
                    }
                    //System.out.println(i + ":  " + line);
                    out.write(line);
                    out.newLine();
                }
            }
            out.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    public static void main(String[] args) {
        new FuelPatchDrawerController(400, 500);
    }


    @Override
    public void actionPerformed(ActionEvent e) {
        String fileName = "fuel.asc";
        writeToFile(fileName, canvas.getValueMatrix());
        //JFileChooser chooser = new JFileChooser();
        //int returnVal = chooser.showOpenDialog(this);
        //if (returnVal == JFileChooser.APPROVE_OPTION) {
        //    String fileName = chooser.getSelectedFile().getAbsolutePath();
        //    System.out.println(fileName);
        //    writeToFile(fileName, canvas.getValueMatrix());
        //}
    }
}