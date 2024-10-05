import pandas as pd
import math 

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

    
        planetDictionary[exoPlanet_name] = snr

    return planetDictionary
    # Check if the value is NaN
    #     if not math.isnan(snr):
    #         detectablePlanets.append(index)

if __name__ == "__main__":
    telescopeDiameter = 10
    print(calculateSNR(telescopeDiameter))

    

