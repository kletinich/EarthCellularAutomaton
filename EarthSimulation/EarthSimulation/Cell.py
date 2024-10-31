import random

# a single cell in the simulation
class Cell:
    def __init__(self, cellType, cellHeight, cellTemp):
        self.cellType = cellType # type of cell (String) = land/sea/iceberg/forest/city
        self.cellHeight = cellHeight # height of a cell (int) 
        self.cellTemp = cellTemp # temperature of a cell (double)
        self.tempChange = 0 # the change in temperature through time
        self.cloudPercentage = 0.0 # how many clouds in a cell (0 <= percentage <= 1)
        self.pollutionPercentage = 0.0  # how much pollution in a cell (0 <= percentage <= 1)
        self.rain = False # is it raining? (boolean)
        self.wind = False # is there a wind? (boolean)
        self.windIntensity = 0 # intensity of the wind (int) 
        self.windDirection = " " # direction of the wind (string) = north, east, south, west
        
        self.LOWEST_TEMP = cellTemp - 10 # the lowest temperature possible in a cell
        self.HIGHEST_TEMP = 80 # the highest temperature possible in a cell
        self.BASE_CHANCE_FOR_WIND = 0.38 # a constant that sets wind in a cell
        self.TEMP_CHANGE = 0.005 # a constant that changes the temperature by a constant
        self.BASE_CLOUD_CHANCE = 0.2 # a constant for the base chance of a cell to generate clouds
        
    # generate cloud percentage in a cell according to the height of the cell
    def generateClouds(self):
        cloudChance = random.random()
        
        if(cloudChance <= self.BASE_CLOUD_CHANCE + self.cellHeight*0.001):
            self.cloudPercentage = random.uniform(0,1)
        
        else:
            self.cloudPercentage = 0
         
    # generates the rain according to the cloud percentage
    def generateRain(self):
        rand = random.random()
        if(rand <= self.cloudPercentage):
           self.rain = True
        else:
           self.rain = False
        
    # generates the wind according to the chance for wind
    def generateWind(self):
        rand = random.random()
        # random success if making wind
        if(rand <= self.BASE_CHANCE_FOR_WIND):
            #if there wasn't a winf before, set the direction of it
            if(self.wind == False):
                self.wind = True
                randDirection = random.randint(1,4)
                if(randDirection == 1):
                    self.windDirection = "north"
                elif(randDirection == 2):
                    self.windDirection = "east"
                elif(randDirection == 3):
                    self.windDirection = "south"
                else:
                    self.windDirection = "west"
                
            # strengthen the wind up to maximum 5
            if(self.windIntensity < 5):
                self.windIntensity += 1
              
        # unsuccess of making wind, lowering its intensity
        else:
            if(self.wind == True):
                self.windIntensity -= 1
                if(self.windIntensity == 0):
                    self.wind = False
                    self.windDirection = " "
         
    # generate a new level of pollution in a cell according to its type
    def generatePollution(self):
        # cell type is a city and it generates pollution until maximum value of 1
        if(self.cellType == "city" and self.pollutionPercentage < 1):
            self.pollutionPercentage += 0.02
                
        # cell type is not a city. Lower the pollution until minimum of 0
        elif(self.cellType != "city"):
            self.pollutionPercentage -= 0.003
            if(self.pollutionPercentage < 0):
                self.pollutionPercentage = 0
                
        if(self.pollutionPercentage > 1):
            self.pollutionPercentage = 1
            
    # updating the temperature in a cell according to wind, clouds, rain and pollution
    def setTemperature(self):
        if(self.wind == True and self.tempChange > 0):
            self.cellTemp -= self.TEMP_CHANGE * self.windIntensity
        elif(self.wind == False and self.tempChange < 0):
            self.cellTemp += self.TEMP_CHANGE * self.windIntensity
        
        if(self.cloudPercentage != 0 and self.tempChange > 0):
            self.cellTemp -= self.TEMP_CHANGE * self.cloudPercentage
        elif(self.cloudPercentage == 0 and self.tempChange < 0):
            self.cellTemp += self.TEMP_CHANGE * self.cloudPercentage
                
        if(self.rain == True and self.tempChange > 0):
            self.cellTemp -= self.TEMP_CHANGE
        elif(self.rain == False and self.tempChange < 0):
            self.cellTemp += self.TEMP_CHANGE
            
        self.cellTemp += self.TEMP_CHANGE * self.pollutionPercentage * 20
                
        # temperature can't get lower than the minimum temperature
        if(self.cellTemp < self.LOWEST_TEMP):
            self.cellTemp = self.LOWEST_TEMP
        
        # temperature can't get higher than the maximum temperature
        elif(self.cellTemp > self.HIGHEST_TEMP):
            self.cellTemp = self.HIGHEST_TEMP
                 
        self.tempChange = self.cellTemp - (self.LOWEST_TEMP + 10)
        
    # passing a certain temperatures may melt icebergs and burning forests
    def disaster(self):
           if(self.cellType == "iceberg" and self.cellTemp > 10):
               self.cellType = "melted iceberg"
           elif(self.cellType == "forest" and self.cellTemp > 50):
               self.cellType = "burnt forest"
                    
    def toString(self):
        info = "Cell type: " + self.cellType + "\n"
        info += "Height: " + str(self.cellHeight) + " meters\n"
        info += "Temperature: " + str(round(self.cellTemp, 2)) + " celcius\n"
        info += "Change of temperature: " + str(round(self.tempChange, 2)) + " celcius\n"
        info += "Cloud percentage: " + str(round(self.cloudPercentage * 100, 2)) + "%\n"
        info += "Pollution percentage: " + str(round(self.pollutionPercentage * 100, 2)) + "%\n"
        info += "Rain: " + str(self.rain) + "\n"
        info += "Wind: " + str(self.wind) + "\n"
        info += "Wind intensity: " + str(self.windIntensity) + "\n"
        info += "Wind direction: " + self.windDirection + "\n"
        return info
            
                
             

