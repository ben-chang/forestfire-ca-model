/** Written by Matayas Boros 4-18-2017 **/

import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class TopographyCreatorController extends JFrame implements ActionListener {

    final int width, height;
    private JButton saveButton, startButton, deleteButton;
    private JButton squareBrushShapeButton, circularBrushShapeButton;
    private JTextField minEntry, maxEntry, widthEntry, heightEntry;
    private JTextField brushIntensityEntry, brushSizeEntry;
    private JLabel brushShapeText, brushSizeText, brushIntensityText;
    private JLabel minLabel, maxLabel, widthLabel, heightLabel;
    private JButton changeBrushSizeButton, changeBrushIntensityButton;
    private TopographyCreator canvas;
    private JLabel fakeLabel1, fakeLabel2, fakeLabel3, fakeLabel4;
    private boolean hasCanvas = false;

    TopographyCreatorController(int width, int height) {
        this.height = height;
        this.width = width;
        Container cp = getContentPane();
        cp.setLayout(new GridLayout(8, 3, 4, 4));


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

        this.minLabel = new JLabel("Minimum value within matrix:");
        this.minEntry = new JTextField("0");
        this.fakeLabel3 = new JLabel("");
        cp.add(minLabel);
        cp.add(minEntry);
        cp.add(fakeLabel3);

        this.maxLabel = new JLabel("Maximum value within matrix:");
        this.maxEntry = new JTextField("0");
        this.fakeLabel4 = new JLabel("");
        cp.add(maxLabel);
        cp.add(maxEntry);
        cp.add(fakeLabel4);

        this.brushSizeEntry = new JTextField("0");
        this.brushSizeText = new JLabel("Brush Size:");
        this.changeBrushSizeButton = new JButton("Apply!");
        changeBrushSizeButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                final int newSize = Integer.parseInt(brushSizeEntry.getText());
                canvas.setBrushIntensity(newSize);
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

        this.brushIntensityText = new JLabel("Brush Intensity:");
        this.brushIntensityEntry = new JTextField("0");
        this.changeBrushIntensityButton = new JButton("Apply!");
        changeBrushIntensityButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                final double newIntensity = Double.parseDouble(brushIntensityEntry.getText());
                canvas.setBrushIntensity(newIntensity);
            }
        });
        cp.add(brushIntensityText);
        cp.add(brushIntensityEntry);
        cp.add(changeBrushIntensityButton);


        this.saveButton = new JButton("save drawing");
        this.deleteButton = new JButton("delete drawing");
        this.startButton = new JButton("start drawing");

        startButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

                final int canvasHeight = Integer.parseInt(heightEntry.getText());
                final int canvasWidth = Integer.parseInt(widthEntry.getText());
                final double min = Double.parseDouble(minEntry.getText());
                final double max = Double.parseDouble(maxEntry.getText());
                final int brushSize = Integer.parseInt(brushSizeEntry.getText());
                final double brushIntensity = Double.parseDouble(brushIntensityEntry.getText());
                canvas = new TopographyCreator(canvasWidth, canvasHeight, min, max,
                        brushIntensity, brushSize, 1);
                JFrame canvasContainer = new JFrame();
                Container cp = canvasContainer.getContentPane();
                cp.setLayout(new BorderLayout());
                cp.add(canvas, BorderLayout.CENTER);
                canvasContainer.setTitle("Drawing Canvas");
                canvasContainer.setSize(310, 310);
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

        setTitle("Topography Creator Demo");
        setSize(width, height);
        setVisible(true);
    }

    private void writeToFile(String toPath, double[][] valueMatrix) {
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
                        line += Double.toString(valueMatrix[i - firstLines.length][j]) + " ";
                    }
                    System.out.println(i + ":  " + line);
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
        new TopographyCreatorController(500, 500);
    }


    @Override
    public void actionPerformed(ActionEvent e) {
        JFileChooser chooser = new JFileChooser();
        int returnVal = chooser.showOpenDialog(this);
        if (returnVal == JFileChooser.APPROVE_OPTION) {
            String fileName = chooser.getSelectedFile().getAbsolutePath();
            System.out.println(fileName);
            writeToFile(fileName, canvas.getValueMatrix());
        }
    }
}