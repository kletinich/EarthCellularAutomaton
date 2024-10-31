from Cell import Cell
import random

# a matrix of cells representing earth
class Earth:
    def __init__(self):
        
        self.ROWS = 10
        self.COLUMNS = 10        
        self.earth = [[0 for _ in range(self.ROWS)] for _ in range(self.COLUMNS)] 
        self.riseInTempAvg = 0 ## the average rise in temperature on earth
        
        self.MAX_HEIGHT = 500 # max cell height for this simulation
        self.TYPES_OF_CELLS = 5 # types of cells - land, sea, iceberg, forest, city
        self.BASE_LAND_TEMP = 20 # the base temperature for a land
        self.BASE_SEA_TEMP = 20 # the base temperature for sea
        self.BASE_ICEBERG_TEMP = -20 # the base temperature for an iceberg
        self.BASE_FOREST_TEMP = 20 # the base temperature for a forest
        self.BASE_CITY_TEMP = 25 # the base temperature for a city
        self.TEMP_RATIO_FOR_LAND = 0.004 # a ratio derieved from the height to land
        self.TEMP_RATIO_FOR_ICEBERG = 0.002 # a ratio derieved from the height to iceberg
        self.TEMP_RATIO_FOR_FOREST = 0.004 # a ratio derieved from the height to forest
        self.TEMP_RATIO_FOR_CITY = 0.006 # a ratio derieved from the height to city
        
    # generates a random earth in which every cell is randomize type, height and temperature
    def generateEarth(self):
        cellType = ""
        randCellHeight = 0
        cellTemp = 0
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                randCellType = random.random()
                randCellHeight = random.randint(0, self.MAX_HEIGHT)
                
                if(randCellType <= 0.3): # 30% of cells are land
                    cellType = "land"
                    cellTemp = self.BASE_LAND_TEMP - randCellHeight * self.TEMP_RATIO_FOR_LAND
                    
                elif(0.3 < randCellType <= 0.75): # 45% of cells are sea
                    cellType = "sea"
                    randCellHeight = 0
                    cellTemp = self.BASE_SEA_TEMP
                    
                elif(0.75 < randCellType <= 0.8): # 5% of cells are icebergs
                    cellType = "iceberg"
                    cellTemp = self.BASE_ICEBERG_TEMP - randCellHeight * self.TEMP_RATIO_FOR_ICEBERG
                    
                elif(0.8 < randCellType <= 0.92): # 12% of cells are forests
                    cellType = "forest"
                    cellTemp = self.BASE_FOREST_TEMP - randCellHeight * self.TEMP_RATIO_FOR_FOREST
                    
                elif(0.92 < randCellType): # 8% of cells are cities
                    cellType = "city"
                    cellTemp = self.BASE_CITY_TEMP - randCellHeight * self.TEMP_RATIO_FOR_CITY
                    
                self.earth[i][j] = Cell(cellType, randCellHeight, cellTemp)
          
    # update the inside enviornment of all cells - clouds, winds, rain, pollution, temperature.
    # first updating the temperature and then clouds, winds, rain, pollution.
    def updateEarthEnviornment(self):
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                self.earth[i][j].setTemperature()
                self.earth[i][j].generateClouds()
                self.earth[i][j].generateRain()
                self.earth[i][j].generateWind()
                self.earth[i][j].generatePollution()
                
    # update earth with the transfer of clouds and pollution through wind
    def windCloudsAndPollution(self):
        update = self.windCloudsAndPollutionUpdateMatrix()
        
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                
                self.earth[i][j].cloudPercentage += update[i][j].cloudPercentage
                if(self.earth[i][j].cloudPercentage > 1):
                    self.earth[i][j].cloudPercentage = 1
                    
                self.earth[i][j].pollutionPercentage += update[i][j].pollutionPercentage
                if(self.earth[i][j].pollutionPercentage > 1):
                    self.earth[i][j].pollutionPercentage = 1
         
    # transfer clouds and pollution with wind to a temporary update matrix
    def windCloudsAndPollutionUpdateMatrix(self):
        
        # Store a temporary update to each cell before updating the cells.
        # Need to do this because the update need to come after all the cells
        # transfered the clouds and the pollution.
        update = [[0 for _ in range(self.ROWS)] for _ in range(self.COLUMNS)]
        updateRow = 0 # the updated row
        updateCol = 0 # the updated column
        transferClouds = 0 # how much clouds to transfer
        transferPollution = 0 # how much pollution to transfer
        
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                update[i][j] = Cell("",0,0)
                
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                # Wind exists and needs to transfer clouds and pollution
                if(self.earth[i][j].wind == True):
                    # clouds or pollution exist, needed to be transfered
                    if(self.earth[i][j].cloudPercentage > 0 or self.earth[i][j].pollutionPercentage > 0 ):
                        if(self.earth[i][j].windDirection == "north"):
                            updateCol = j
                            if(i == 0):
                                updateRow = self.ROWS - 1
                            else:
                                updateRow = i - 1
                        
                        elif(self.earth[i][j].windDirection == "south"):
                            updateCol = j
                            if(i == self.ROWS - 1):
                                updateRow = 0
                            else:
                                ipdateRow = i + 1
                                
                        elif(self.earth[i][j].windDirection == "west"):
                            updateRow = i
                            if(j == 0):
                                updateCol = self.COLUMNS - 1
                            else:
                                updateCol = j - 1
                        
                        elif(self.earth[i][j].windDirection == "east"):
                            updateRow = i
                            if(j == self.COLUMNS - 1):
                                updateCol = 0
                            else:
                                updateCol = j + 1
                                
                        # transfering clouds to the updated cell and reducing clouds from the current cell
                        if(self.earth[i][j].cloudPercentage > 0):
                            transferClouds = (self.earth[i][j].cloudPercentage * self.earth[i][j].windIntensity * 0.2)
                            update[updateRow][updateCol].cloudPercentage += transferClouds
                            update[i][j].cloudPercentage -= transferClouds
                            
                        # transfering pollution to the updated cell and reducing clouds from the current cell
                        if(self.earth[i][j].pollutionPercentage > 0):
                            transferPollution = (self.earth[i][j].pollutionPercentage * self.earth[i][j].windIntensity * 0.2)
                            update[updateRow][updateCol].pollutionPercentage += transferPollution
                            update[i][j].pollutionPercentage -= transferPollution
        return update
    
    def calculateAvg(self):
        sum = 0.0
        
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                sum += self.earth[i][j].tempChange
                
        self.riseInTempAvg = sum/(self.ROWS * self.COLUMNS)
    
    # a day in earth
    def step(self):
        self.updateEarthEnviornment()
        self.windCloudsAndPollution()
        self.calculateAvg()
                          