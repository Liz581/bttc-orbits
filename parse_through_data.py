import pandas as pd
import math
import matplotlib.pyplot as plt


def calculateSNR(telescopeDiameter):
    # Load the Excel file
    df = pd.read_csv('PSCompPars_2024.10.05_11.19.54.csv')
    df = df.dropna()

    #Dictionary
    planetDictionary = {}

    for index, row in df.iterrows():
        exoPlanet_name = row["pl_name"] 
        planetRadius = float(row["pl_rade"]) # RP
        stellarRadius = float(row["st_rad"]) # R*
        planetStarDistance = float(row["pl_orbsmax"]) # PS
        distanceToPlanetary = float(row["sy_dist"]) #ES    
    
        snr = 100 * ((stellarRadius * planetRadius * (telescopeDiameter/6))/((distanceToPlanetary/10) *(planetStarDistance))) ** 2

        if snr > 5:
            planetDictionary[exoPlanet_name] = snr

    return planetDictionary
    # Check if the value is NaN
    #     if not math.isnan(snr):
    #         detectablePlanets.append(index)

def parseDMS(str):
    d = str.split("d")
    deg = float(d[0])
    ms = d[1].split("m")
    min = float(ms[0])
    sec = float(ms[1][:-1])
    return deg, min, sec

def parseHMS(str):
    d = str.split("h")
    deg = float(d[0])
    ms = d[1].split("m")
    min = float(ms[0])
    sec = float(ms[1][:-1])
    return deg, min, sec

def convertDMStoRadian(str):
    deg, min, sec = parseDMS(str)
    rad = deg + (min/60) + (sec/3600)
    return rad

def timeToRadians(str):
    hr, min, sec = parseHMS(str)
    totHrs = hr + (min/60) + (sec/3600)
    rad = (totHrs / 24) * 2 * math.pi
    return rad

def raDectoCartesian(raStr, decStr, distance):
    ra = timeToRadians(raStr)
    dec = convertDMStoRadian(decStr)
    x = (distance * math.cos(dec)) * math.cos(ra)
    y = (distance * math.cos(dec)) * math.sin(ra)
    z = distance * math.sin(dec)
    return x, y, z

def decideColor(str):
    if str[0].upper() == 'O':
        return "purple"
    elif str[0].upper() == 'B':
        return "darkblue"
    elif str[0].upper() == 'A':
        return "blue"
    elif str[0].upper() == 'F':
        return "lime"
    elif str[0].upper() == 'G':
        return "yellow"
    elif str[0].upper() == 'K':
        return "red"
    elif str[0].upper() == 'M':
        return "darkred"
    else:
        return "white"


def findExoPlanets(telescopeDiameter):
    # Load the Excel file
    df = pd.read_csv('PSCompPars_2024.10.05_11.19.54.csv')
    df = df.dropna()

    #Dictionary
    planetDictionary = []

    for index, row in df.iterrows():
        exoPlanet_name = row["pl_name"] 
        planetRadius = float(row["pl_rade"]) # RP
        stellarRadius = float(row["st_rad"]) # R*
        planetStarDistance = float(row["pl_orbsmax"]) # PS
        distanceToPlanetary = float(row["sy_dist"]) #ES    
        x, y, z = raDectoCartesian(row["rastr"], row["decstr"], distanceToPlanetary)
        snr = 100 * ((stellarRadius * planetRadius * (telescopeDiameter/6))/((distanceToPlanetary/10) *(planetStarDistance))) ** 2
        color = decideColor(row["st_spectype"])
        if snr > 5:
            planetDictionary.append([exoPlanet_name, snr, x, y, z, color])

    return planetDictionary

    
if __name__ == "__main__":
    telescopeDiameter = 10
    # print(calculateSNR(telescopeDiameter))
    # print(findExoPlanets(telescopeDiameter))
    # print(parseDMS("25d 4m 6s"))
    # print(convertDMStoRadian("25d 4m 6s"))
    # print(raDectoCartesian("25h 4m 6s", "5d 2m 16s", 12))

    planets = findExoPlanets(telescopeDiameter)
    fig = plt.figure(facecolor = 'black')
    ax = fig.add_subplot(projection='3d')   
    ax.set_facecolor('black')
    for i in planets:
        xs = i[2]
        ys = i[3]
        zs = i[4]
        color = i[5]
        ax.scatter(xs, ys, zs, c = color)

    ax.scatter(0, 0, 0, c = 'white')

    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # ax.set_zlabel('Z Label')

    for angle in range(0, 360*4 + 1):
        elevation = azimmuth = roll = 0
        angleNormalized = (angle + 180) % 360 - 180
        if angle <= 360:
            elevation = angleNormalized
        elif angle <= 360*2:
            azimmuth = angleNormalized
        elif angle <= 360*3:
            roll = angleNormalized
        else:
            elevation = azimmuth = roll = angleNormalized

    ax.view_init(elevation, azimmuth, roll)
    plt.title('Elevation: %d°, Azimuth: %d°, Roll: %d°' % (elevation, elevation, roll))

    plt.draw()
    plt.show()