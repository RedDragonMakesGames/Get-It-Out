import SetUpScreen
import GetItOut

#Run the set up screen
setUpScreen = SetUpScreen.SetUp()
boardsetup = setUpScreen.Run()
game = GetItOut.GetItOut(boardsetup)
#Restart the board if the restart button was pressed
while game.Run() == True:
    board = game = GetItOut.GetItOut(boardsetup)