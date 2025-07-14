from utils import *
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QMenuBar,
    QPushButton,
    QWidget,
    QFrame,
    QSplitter,
    QLabel,
    QLineEdit,
    QAction,
    QSizePolicy,
    QMessageBox,
    QHBoxLayout,
    QTextBrowser,
    QGroupBox,
    QFileDialog,
)

# Global variables to set window size
windowWidth = 720
windowHeight = 480


def displayBox(messageType, messageInfo, messageTitle, isError=False):
    """
    Handles the creation of a QMessageBox, allowing the user to set the windowTitle, Text, and type of the message show easily.
    """
    messageBox = QMessageBox()
    if isError:
        messageBox.setIcon(QMessageBox.Critical)
    else:
        messageBox.setIcon(QMessageBox.Information)
    messageBox.setText(messageType)
    messageBox.setInformativeText(messageInfo)
    messageBox.setWindowTitle(messageTitle)
    messageBox.exec_()


class borderedQGroupBox(QGroupBox):
    """
    Used to allow for rounded corners on GroupBoxes in the stylesheet without affecting other group boxes
    """

    def __init__(self, args):
        super().__init__(args)


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Channel Processing Tool")
        self.setStyleSheet(
            """
                            
                            QFrame{
                                background-color: #F0F0F0;
                                font-size: 16px;}
                            QLabel{
                                font-size: 16px;
                            }
                            QLineEdit
                            {
                                font-size: 16px;
                            }
                            borderedQGroupBox{
                                background-color: #F0F0F0;
                                border : 1px solid #CECECE;
                                border-top-left-radius : 20px;
                                border-top-right-radius : 20px;
                                border-bottom-left-radius : 20px;
                                border-bottom-right-radius : 20px;}"""
        )

        self.resize(windowWidth, windowHeight)

        self.channelFile = ""
        self.paramFile = ""

        # Set up all Frames and Layouts

        # Main layout for the entire widget
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)  # Remove padding from the layout
        mainLayout.setSpacing(0)  # No spacing between elements
        self.setLayout(mainLayout)  # Apply the main layout to the widget

        # Frame that holds both file picking frames
        contentAreaFrame = QFrame()
        contentAreaFrame.setFrameStyle(QFrame.NoFrame)  # No border around the frame
        contentAreaFrame.setBaseSize(600, 100)
        contentAreaFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout for the contentArea frame
        contentAreaLayout = QVBoxLayout()
        contentAreaLayout.setContentsMargins(
            25, 25, 25, 25
        )  # Remove padding from the layout
        contentAreaLayout.setSpacing(10)  # No spacing between elements
        contentAreaFrame.setLayout(contentAreaLayout)  # Apply the layout to the frame

        mainLayout.addWidget(contentAreaFrame)

        # Frame which holds both input frames
        inputFrame = QFrame()
        inputLayout = QHBoxLayout()
        inputFrame.setLayout(inputLayout)
        contentAreaLayout.addWidget(inputFrame)

        # Frame that allows user to choose a Channel file as input
        channelFileFrame = borderedQGroupBox("Select Channel File")
        channelFileFrame.setBaseSize(800, 400)

        channelFileLayout = QVBoxLayout()
        channelFileLayout.setContentsMargins(25, 25, 25, 25)  # Pad 25 pixels each way
        channelFileFrame.setLayout(channelFileLayout)

        inputLayout.addWidget(channelFileFrame)

        # Frame that allows user to choose a Parameter file as input
        paramFileFrame = borderedQGroupBox("Select Parameter File")
        paramFileFrame.setBaseSize(800, 400)

        paramFileLayout = QVBoxLayout()
        paramFileLayout.setContentsMargins(25, 25, 25, 25)  # Pad 25 pixels each way
        paramFileFrame.setLayout(paramFileLayout)

        inputLayout.addWidget(paramFileFrame)

        # Frame which holds both output frames
        outputFrame = QFrame()
        outputLayout = QHBoxLayout()
        outputFrame.setLayout(outputLayout)
        contentAreaLayout.addWidget(outputFrame)

        # Frame that holds line edits that let user choose output file names
        channelOutputFrame = borderedQGroupBox("Select Output Channel Name")
        channelOutputFrame.setBaseSize(800, 400)
        channelOutputLayout = QVBoxLayout()
        channelOutputLayout.setSpacing(10)  # 10 Pixels spacing between elements
        channelOutputLayout.setContentsMargins(25, 25, 25, 25)  # Pad 25 pixels each way
        channelOutputFrame.setLayout(channelOutputLayout)
        outputLayout.addWidget(channelOutputFrame)

        # Frame which holds line edits that let user choose output file names
        paramOutputFrame = borderedQGroupBox("Select Output Parameter Name")
        paramOutputFrame.setBaseSize(800, 400)
        metricOutputLayout = QVBoxLayout()
        metricOutputLayout.setSpacing(10)  # 10 Pixels spacing between elements
        metricOutputLayout.setContentsMargins(25, 25, 25, 25)  # Pad 25 pixels each way
        paramOutputFrame.setLayout(metricOutputLayout)
        outputLayout.addWidget(paramOutputFrame)

        # Frame that holds the Confirm button
        buttonFrame = QFrame()
        buttonFrame.setBaseSize(600, 60)
        buttonFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(25, 25, 25, 25)  # Pad 25 pixels each way
        buttonLayout.setSpacing(10)

        buttonFrame.setLayout(buttonLayout)

        mainLayout.addWidget(buttonFrame)

        # Add content to frames and layouts

        # Add channel file label and button for selecting file

        self.channelFileLabel = QLabel("No Channel File Selected.")
        channelFileLayout.addWidget(self.channelFileLabel)

        channelFileButton = QPushButton("Select File")
        channelFileButton.clicked.connect(self.selectChannelFile)
        channelFileLayout.addWidget(channelFileButton)

        # Add parameter file label and button for selecting file

        self.paramFileLabel = QLabel("No Parameter File Selected.")
        paramFileLayout.addWidget(self.paramFileLabel)

        paramFileButton = QPushButton("Select File")
        paramFileButton.clicked.connect(self.selectParamFile)
        paramFileLayout.addWidget(paramFileButton)

        # Add line edits to allow user to select name of output files

        outputChannelLabel = QLabel("Channel Output File Name")
        channelOutputLayout.addWidget(outputChannelLabel)
        self.outputChannelLineEdit = QLineEdit("OutputChannels")
        channelOutputLayout.addWidget(self.outputChannelLineEdit)

        outputMetricLabel = QLabel("Metric Output File Name: ")
        metricOutputLayout.addWidget(outputMetricLabel)
        self.outputMetricLineEdit = QLineEdit("OutputMetrics")
        metricOutputLayout.addWidget(self.outputMetricLineEdit)

        # Add a button to begin calculation

        calculateButton = QPushButton("Calculate")
        calculateButton.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold;"
        )
        calculateButton.clicked.connect(self.beginCalculation)
        buttonLayout.addWidget(calculateButton)

    def selectChannelFile(self):
        """
        Called when the channelFileButton is clicked. Will open a file dialog allowing the user to select a file.
        """
        fileName = QFileDialog.getOpenFileName(
            self, "Select Channel File", "", "TXT Files (*.txt)"
        )
        if fileName[0] != "":
            self.channelFile = fileName[0]  # Get first file path of files selected
            self.channelFileLabel.setText(
                "File: " + self.channelFile.split("/")[-1]
            )  # Only show the name of the file, not the whole path
        else:
            self.channelFile = ""
            self.channelFileLabel.setText("No Channel File Selected.")

    def selectParamFile(self):
        """
        Called when the paramFileButton is clicked. Will open a file dialog allowing the user to select a file.
        """
        fileName = QFileDialog.getOpenFileName(
            self, "Select Parameter File", "", "TXT Files (*.txt)"
        )
        if fileName[0] != "":
            self.paramFile = fileName[0]  # Get first file path of files selected
            self.paramFileLabel.setText(
                "File: " + self.paramFile.split("/")[-1]
            )  # Only show the name of the file, not the whole path
        else:
            self.paramFile = ""
            self.paramFileLabel.setText("No Parameter File Selected.")

    def beginCalculation(self):
        """
        Called when the calculateButton is clicked, will perform the bulk of all calculations using functions from the utils.py file.
        """
        if self.channelFile == "" or self.paramFile == "":
            # Check if files have been selected
            return displayBox(
                "File Error",
                "Both a channel file and a parameter file must be selected.",
                "Error",
                isError=True,
            )

        try:
            # Check if the files exist
            file = open(self.channelFile, "r")
            file.close()
            file = open(self.paramFile, "r")
            file.close()
        except FileNotFoundError:
            return displayBox(
                "File Error", "Selected file does not exist.", "Error", isError=True
            )

        if (
            self.outputMetricLineEdit.text() == ""
            or self.outputChannelLineEdit.text() == ""
        ):  # Check if desired file names are empty
            return displayBox(
                "File Name Error", "File names cannot be empty.", "Error", isError=True
            )
        if (
            " " in self.outputMetricLineEdit.text()
            or " " in self.outputChannelLineEdit.text()
        ):  # Check if desired file names have spaces in them
            return displayBox(
                "File Name Error",
                "File names cannot contain spaces.",
                "Error",
                isError=True,
            )

        metrics = (
            {}
        )  # Create a dict for metrics to allow system to be extended to multiple different metrics
        channels = readChannels(self.channelFile)  # Read in given channels
        params = readParameters(self.paramFile)  # Read in given parameters
        # Calculate channel Y and add to channels dict
        try:
            channels.update({"Y": functionOne(params, channels["X"])})
        except KeyError:
            return displayBox(
                "File Error",
                "Needed inputs (X, m, c) are not present in your input files.",
                "Error",
                isError=True,
            )
        # Calculate channel X and add to channels dict
        channels.update({"A": functionThree(channels["X"])})

        # Calculates channel B and finds the average of B
        channelB, meanB = functionTwo(channels["A"], channels["Y"])
        # Add channel B to channels dict, and add metric b to metrics dict
        channels.update({"B": channelB})
        metrics.update({"b": meanB})

        # Calculate channel C and add it to channels dict
        channels.update({"C": functionFour(channels["X"], metrics["b"])})

        writeOutputChannels(channels, self.outputChannelLineEdit.text() + ".txt")
        writeOutputMetrics(metrics, self.outputMetricLineEdit.text() + ".txt")

        displayBox(
            "Processing Complete",
            "Data has been processed, output has been saved to "
            + self.outputChannelLineEdit.text()
            + ".txt and "
            + self.outputMetricLineEdit.text()
            + ".txt",
            "Success",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
