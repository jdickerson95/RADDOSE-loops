import os


def loop(inputFile='MyInput.txt', changeMe='$', metric='AD-WC', alsoChangeMe='@'):

    # set of values to change
    vals = [1, 2, 5, 8, 10, 12, 15, 18, 20, 30, 50, 100]

    extractedMetrics = []

    for v in vals:
       # ppm = 10/float(v)
        ppm = 0.1
        # change input file for current value
        newInputFile = inputFile.replace('.txt', '-updated.txt')
        f = open(inputFile, 'r')
        g = open(newInputFile, 'w')
        for l in f.readlines():
            g.write(l.replace(changeMe, str(v)))
        f.close()
        g.close()
        '''
        newerInputFile = newInputFile.replace('.txt', '-updated.txt')
        f = open(newInputFile, 'r')
        g = open(newerInputFile, 'w')
        for l in f.readlines():
            g.write(l.replace(alsoChangeMe, str(ppm)))
        f.close()
        g.close()
        '''

        # run new RD3D file
       # os.system('java -jar RD3DDone.jar -i ' + newerInputFile)
        os.system('java -jar RD3DDone.jar -i ' + newInputFile)

        # parse the output file
        f = open('./output-Summary.csv', 'r')
        for i, l in enumerate(f.readlines()):
            l = l.replace(' ', '')
            if i == 0:
                # get metric place in csv file
                ind = l.split(',').index(metric)
            else:
                # extract the metric value
                met = float(l.split(',')[ind])
                extractedMetrics.append(met)
                break
        f.close()

    # write new csv file
    f = open('./loop-metrics.csv', 'w')
    f.write(','.join(map(str, extractedMetrics)))
    f.close()

if __name__ == "__main__":
    loop()
