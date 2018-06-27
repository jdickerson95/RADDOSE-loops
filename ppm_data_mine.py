import os
import csv

def loop(inputFile="input.txt", changeMe='$', metric='DWD'):
    # set of values to change
    size_vals = [17.2, 0.5, 1, 5, 10, 20, 50, 100, 200]
    beam_energy = [0.5, 1, 5, 8, 10, 12, 15, 20]

    same_DWD = False
    DWD = []
    lines = []
    ppm = 0.0
    counter = -1;
    for x in size_vals:
        for y in size_vals:
            for z in size_vals:
                for bx in size_vals:
                    for by in size_vals:
                        for e in beam_energy:
                            same_DWD = False
                            DWD = []
                            lines = []

                            #minimum possible ppm
                            ppm = 1/min(x, y, z) # - 0.05
                            remainder = ppm % 0.05
                            ppm = ppm - remainder

                            counter = -1
                            while same_DWD == False:
                                # change the file
                                ppm += 0.05
                                counter += 1
                                newInputFile = inputFile.replace('.txt', '-updated.txt')
                                f = open(inputFile, 'r')
                                g = open(newInputFile, 'w')
                                for l in f.readlines():
                                    l = l.replace(changeMe, str(ppm))
                                    l = l.replace('@', str(x))
                                    l = l.replace ('?', str(y))
                                    l = l.replace('_', str(z))
                                    l = l.replace('&', str(bx))
                                    l = l.replace ('{', str(by))
                                    l = l.replace ('}', str(e))
                                    lines.append(l)
                                for value in lines:
                                    g.write(value)
                                f.close()
                                g.close()

                                # run new RD3D file
                                os.system('java -jar raddose3d.jar -i ' + newInputFile)

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
                                        DWD.append(met)
                                        break
                                f.close()
                                # now need to compare previous to exit the loop
                                if (counter > 1) and (DWD[counter - 2] > 0.0):
                                    if (abs((DWD[counter] - DWD[counter - 1]) / DWD[counter - 1]) < 0.01) and (
                                        abs((DWD[counter] - DWD[counter - 2]) / DWD[counter - 2]) < 0.01) \
                                            and (abs((DWD[counter - 1] - DWD[counter - 2]) / DWD[counter - 2]) < 0.01):
                                        same_DWD = True

                            # extract all of the inputs
                            xstal_x = x
                            xstal_y = y
                            xstal_z = z
                            xstal_area = xstal_x * xstal_y
                            xstal_vol = xstal_x * xstal_y * xstal_z
                            beam_x = bx
                            beam_y = by
                            beam_area = beam_x * beam_y
                            beam_energy = e
                            area_ratio = xstal_area / beam_area
                            pe_escape = 'FALSE'
                            actual_ppm = ppm - 0.1
                            with open('./ppm.csv', 'ab') as csvfile:
                                ppmwriter = csv.writer(csvfile)
                                ppmwriter.writerow(
                                    [pe_escape, xstal_x, xstal_y, xstal_z, xstal_area, xstal_vol, beam_energy, beam_x,
                                    beam_y, beam_area,
                                    area_ratio, actual_ppm])

                            print "test"




    # write new csv file
'''
    with open('./ppm.csv', 'wb') as csvfile:
        ppmwriter = csv.writer(csvfile)
        ppmwriter.writerow(['pe_escape','xstal x', 'xstal y', 'xstal z', 'xstal area', 'xstal volume', 'beam energy', 'beam x', 'beam y', 'beam area', 'area ratio', 'ppm'])
        ppmwriter.writerow([pe_escape, xstal_x, xstal_y, xstal_z, xstal_area, xstal_volume, beam_energy, beam_x, beam_y, beam_area, area_ratio, actual_ppm])
    '''
    #append to existing file


if __name__ == "__main__":
    loop()