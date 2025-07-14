import unittest
import numpy
from utils import *


class UtilsTest(unittest.TestCase):
    def setUp(self):
        # Set up a suite of valid values
        self.channelX = numpy.array((1, 2, 4, 5))
        self.channelY = numpy.array((2.5, 4.5, 8.5, 10.5))
        self.channelA = numpy.array((1, 0.5, 0.25, 0.2))
        self.channelB = numpy.array((3.5, 5, 8.75, 10.7))
        self.channelC = numpy.array((7.9875, 8.9875, 10.9875, 11.9875))
        self.metrics = {"b": 6.9875}
        self.params = {"m": 2, "c": 0.5}
        self.channels = {"X": self.channelX}
        self.badFile = open("TestBadFile.txt", "w")
        self.badFile.write("Test for bad data.")
        self.badFile.close()

    def testFunctionOne(self):
        numpy.testing.assert_array_equal(
            functionOne(self.params, self.channelX),
            self.channelY,
            "Function One is incorrect.",
        )

    def testFunctionTwo(self):
        outputChannelB, outputMeanB = functionTwo(self.channelA, self.channelY)
        numpy.testing.assert_array_equal(
            outputChannelB,
            self.channelB,
            "Function 2 is incorrect when calculating channel B.",
        )
        self.assertEqual(
            outputMeanB,
            self.metrics["b"],
            "Function 2 is incorrect when calculating mean of channel B.",
        )

    def testFunctionThree(self):
        numpy.testing.assert_array_equal(
            functionThree(self.channelX), self.channelA, "Function Three is incorrect."
        )

    def testFunctionFour(self):
        numpy.testing.assert_array_equal(
            functionFour(self.channelX, self.metrics["b"]),
            self.channelC,
            "Function Four is incorrect.",
        )

    def testReadChannels(self):
        # Check if each key is in the dictionary, then check the values assigned to them
        output = readChannels("TestChannels.txt")
        keys = output.keys()
        if len(keys) == len(self.channels.keys()):  # Catches too few or too many keys
            for key in keys:
                self.assertIn(key, self.channels.keys(), "Unknown key being read.")
                numpy.testing.assert_array_equal(
                    output[key],
                    self.channels[key],
                    "readChannels reading incorrect values.",
                )
        else:
            self.fail("Number of keys does not match.")
        self.assertRaises(
            FileNotFoundError, lambda: readChannels("NonExistent.txt")[:1]
        )  # Test nothing is read if a non-existent file is given

        self.assertRaises(
            TypeError, lambda: readChannels(self.badFile)[-1]
        )  # Test a type error is raised with bad input file

    def testReadParams(self):
        # Check if each key is in the dictionary, then check the values assigned to them
        output = readParameters("TestParameters.txt")
        keys = output.keys()
        if len(keys) == len(self.params.keys()):  # Catches too few or too many keys
            for key in keys:
                self.assertIn(key, self.params.keys(), "Unknown key being read.")
                self.assertEqual(
                    output[key],
                    self.params[key],
                    "readParameters reading incorrect values.",
                )
        else:
            self.fail("Number of keys does not match.")

    def testWriteOutputChannels(self):
        writeOutputChannels(self.channels, "TestChannelOutput.txt")
        try:
            file = open("TestChannelOutput.txt", "r")
            file.close()
        except FileNotFoundError:
            self.fail("Written file cannot be found.")
        output = readChannels("TestChannelOutput.txt")
        keys = output.keys()
        if len(keys) == len(self.channels.keys()):  # Catches too few or too many keys
            for key in keys:
                self.assertIn(key, self.channels.keys(), "Unknown key being read.")
                numpy.testing.assert_array_equal(
                    output[key], self.channels[key], "Written values are incorrect."
                )
        else:
            self.fail("Number of keys does not match.")

        self.assertRaises(
            FileNotFoundError, lambda: readParameters("NonExistent.txt")[:1]
        )  # Test nothing is read if a non-existent file is given

        self.assertRaises(
            TypeError, lambda: readParameters(self.badFile)[-1]
        )  # Test a type error is raised with bad input file

    def testWriteOutputMetrics(self):
        writeOutputMetrics(self.metrics, "TestMetricOutput.txt")
        try:
            file = open("TestMetricOutput.txt", "r")
            file.close()
        except FileNotFoundError:
            self.fail("Written file cannot be found.")
        output = readParameters("TestMetricOutput.txt")
        keys = output.keys()
        if len(keys) == len(self.metrics.keys()):  # Catches too few or too many keys
            for key in keys:
                self.assertIn(key, self.metrics.keys(), "Unknown key being read.")
                self.assertEqual(
                    output[key],
                    self.metrics[key],
                    "readParameters reading incorrect values.",
                )
        else:
            self.fail("Number of keys does not match.")

        self.assertRaises(
            FileNotFoundError, lambda: readParameters("NonExistent.txt")[:1]
        )  # Test nothing is read if a non-existent file is given

        self.assertRaises(
            TypeError, lambda: readParameters(self.badFile)[-1]
        )  # Test a type error is raised with bad input file


if __name__ == "__main__":
    unittest.main()
