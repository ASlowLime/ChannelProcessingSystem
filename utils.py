import numpy


def readChannels(channelsPath):
    """
    Inputs: Path of the file containing channels to be read.
    Outputs: Dict containing numpy arrays of channel values with the name of the channel as a key.
    """
    channels = {}
    channelFile = open(channelsPath, "r")
    for line in channelFile:
        line = line.split(",")
        channelName = line[0]
        channelContent = numpy.array(line[1:], dtype=numpy.float64)
        channels.update({channelName: channelContent})
    channelFile.close()
    return channels


def readParameters(paramsPath):
    """
    Inputs: Path of the file containing parameters to be read.
    Outputs: Dict containing parameter values with the name of the parameter as a key.
    """
    params = {}  # params is shorthand for parameters
    paramFile = open(paramsPath, "r")
    for line in paramFile:
        line = line.replace(
            "\n", ""
        )  # If the line break code \n is in the line which has been read, remove it.
        line = line.split(",")
        paramName = line[0]  # This will be the name of the parameter, used as the key
        paramValue = float(line[1])  # Cast the parameters value to float
        params.update({paramName: paramValue})  # Add to the dictionary
    paramFile.close()
    return params


def functionOne(params, channel):
    """
    Inputs: Dict of paramaters (params), Numpy array of channel denoted 'X' (channel)
    Output: Numpy array of channel denoted 'Y', calculated from the following function: Y = mX + c
    Performs the function Y = mX + c
    """
    return (channel * params["m"]) + params["c"]


def functionTwo(channelA, channelY):
    """
    Inputs: Numpy array of channel denoted 'A' (channelA), Numpy array of channel denoted 'Y' (channelY)
    Outputs: Numpy array of channel denoted 'B' (channelB), mean of channelB (meanB)
    Performs the function B = A + Y, then calculates the mean of channelB
    """
    channelB = channelA + channelY
    meanB = numpy.mean(channelB)
    return channelB, meanB


def functionThree(channelX):
    """
    Inputs: Numpy array of channel denoted 'X' (channelX)
    Outputs: Numpy array of channel denoted 'A', in which each element is the reciprocal of the corresponding element in channel X
    Performs the function A = 1/X
    """
    return 1 / channelX


def functionFour(channelX, metricB):
    """
    Inputs: Numpy array of channel denoted 'X' (channelX), float of metric denoted 'b' (metricB)
    Outputs: Numpy array of channel denoted 'C'
    Performs the function C = X + b
    """
    return channelX + metricB


def writeOutputChannels(channels, fileName):
    """
    Inputs: Dictionary containing channels (channels), name of the file to be written to as a string (fileName)
    Output: Text file containing all channels, written in the same format as the given channels.txt
    """
    file = open(fileName, "w")
    for key in channels.keys():
        file.write(key)  # Write the name of the channel
        for val in channels[
            key
        ]:  # Write each value to the file individually to allow for specific formatting
            file.write(", " + str(val))
        file.write("\n")  # Add a newline at the end
    file.close()


def writeOutputMetrics(metrics, fileName):
    """
    Inputs: Dictionary containing metrics (metrics), name of the file to be written to as a string (fileName)
    Output: Text file containing all metrics, written in the same format as the given parameters.txt
    """
    file = open(fileName, "w")
    for key in metrics.keys():
        file.write(key + ", " + str(metrics[key]) + "\n")
    file.close()
