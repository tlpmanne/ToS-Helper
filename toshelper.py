from appJar import gui

##Start Screen Functions - these help the user choose the game mode they want to play##
def lvl_1(Button):
    global classic #I have set this as a global variable because I need the changes from this subroutine to be permanent.
    if Button=="Classic":
        #Show classic game modes
        classic=True
        app.setImage("ToS Logo","townofsalemlogo.gif")
    if Button=="Coven":
        #Show coven game modes
        classic=False
        app.setImage("ToS Logo","townofsalemcovenlogo.gif")

def lvl_2(selection):
    gameTypeSelection=str(app.getListBox("Level 2")) #app.getListBox comes out with an array
    gameTypeSelection=gameTypeSelection.replace("['","").replace("']","")
    if classic:
        if gameTypeSelection=="Normal":
            app.updateListBox("Level 3",["Classic","Ranked Practice","Ranked"])
        elif gameTypeSelection=="Custom":
            app.updateListBox("Level 3",["Custom","Rapid Mode"])
        else:
            app.updateListBox("Level 3",["All Any","Rainbow","Vigilantics"])
    if not classic: #Coven
        if gameTypeSelection=="Normal":
            app.updateListBox("Level 3",["Classic","Ranked Practice","Ranked","Mafia Returns"])
        elif gameTypeSelection=="Custom":
            app.updateListBox("Level 3",["Custom"])
        else:
            app.updateListBox("Level 3",["All Any","VIP Mode","Lovers Mode","Rivals Mode"])

def lvl_3(Button):
    gameModeSelection=str(app.getListBox("Level 3"))
    #This will output something like this: ['Ranked Practice']
    gameModeSelection=gameModeSelection.replace("['","").replace("']","")

    gameModeFile=open("game_modes.csv","r")
    fileLines=[]
    count=0
    for line in gameModeFile.readlines():
        fileLines.append(line.split(","))
        if classic: #classic==True
            if fileLines[count][1]==gameModeSelection and fileLines[count][2]=="Classic":
                fileLines[count][17]=fileLines[count][17].replace("\n","")
                roleList=fileLines[count]
                break #End for loop, result found
        else: #Classic=False, give Coven game mode
            if fileLines[count][1]==gameModeSelection and fileLines[count][2]=="Coven":
                fileLines[count][17]=fileLines[count][17].replace("\n","")
                roleList=fileLines[count]
                break #End for loop, result found
        count=count+1
    gameModeFile.close()

    #Display SubWindow "Role List"
    app.showSubWindow("Role List")

    #Change all the information in "Role List" to correspond with game mode chosen.
    app.setLabel("Intro 0",roleList[2]+" "+roleList[1])

    #Arrays
    randomTown=["Town Investigative","Town Killing","Town Protective","Town Support"]
    randomMafia=["Mafia Deception","Mafia Killing","Mafia Support"]
    randomNeutral=["Neutral Benign","Neutral Chaos","Neutral Evil","Neutral Killing"]
    if classic:
        anyRole=[randomTown,randomMafia,randomNeutral]
    else: #Coven
        anyRole=[randomTown,randomMafia,randomNeutral,"Coven Evil"]

    roleFile=open("roles.csv","r")
    fileLines=[]

    for line in roleFile.readlines():
        fileLines.append(line.split(","))

    roleFile.close()

    if not classic: #Remove Witch role from being possible in Coven game mode.
        fileLines.remove(fileLines[39]) #fileLines[39] is Witch

    gameModesNoVamp=["Classic","Ranked Practice","Ranked","Mafia Returns","Rivals Mode"]
    #These are the game modes where Vampire Hunter could potentially appear but shouldn't.
    if any(roleList[1]==gameModesNoVamp[x] for x in range(0,len(gameModesNoVamp)))==True:
        fileLines.remove(fileLines[7]) #fileLines[7] is Vampire Hunter

    allAvailableRoles=[] #I am doing this seperately so I can go back and remove unique confirmed roles.
    for player in range(1,16): #Find all available roles
        availableRoles=[]
        for count in range(0,len(fileLines)):
            line=fileLines[count]
            if line[3]==roleList[player+2]:
                if not classic or line[-1]=="0\n": #If classic is false, don't need to check if Coven specific.
                    availableRoles.append(line[1])
                colour(line[3],str(player))
            if roleList[player+2]=="Random Town" and any(line[3]==randomTown[x] for x in range(0,len(randomTown)))==True:
                if not classic or line[-1]=="0\n": #line[-1] is last item in line
                    availableRoles.append(line[1])
                app.getLabelWidget("Role List "+str(player)).config(fg="green")
            if roleList[player+2]=="Random Mafia" and any(line[3]==randomMafia[x] for x in range(0,len(randomMafia)))==True:
                if not classic or line[-1]=="0\n":
                    availableRoles.append(line[1])
                app.getLabelWidget("Role List "+str(player)).config(fg="red")
            if roleList[player+2]=="Random Neutral" and any(line[3]==randomNeutral[x] for x in range(0,len(randomNeutral)))==True:
                if not classic or line[-1]=="0\n":
                    availableRoles.append(line[1])
            if roleList[player+2]=="Any": #Any is any role, no need to check for alignment.
                if not classic or line[-1]=="0\n":
                    availableRoles.append(line[1])
                app.getLabelWidget("Role List "+str(player)).config(fg="white")
            if roleList[player+2]=="Random Coven" and line[3]=="Coven Evil":
                #No need to check if Coven Specific, this will only come up in Coven game modes.
                availableRoles.append(line[1])
                app.getLabelWidget("Role List "+str(player)).config(fg="purple")
            if roleList[player+2]==line[1]:
                #No need to check if Coven Specific, this is only for confirmed roles.
                availableRoles.append(line[1])
                colour(line[3],str(player))
                if line[-2]=="1": #But if it's unique, it shouldn't appear anywhere else in the role list.
                    for i in range(0,len(allAvailableRoles)):
                        for j in range(0,len(allAvailableRoles[i])):
                            if allAvailableRoles[i][j]==line[1]:
                                allAvailableRoles[i].remove(line[1])
                                break #End for loop
                    fileLines[count]=["","","",""]
        allAvailableRoles.append(availableRoles)

    for player in range(1,16):
        app.setLabel("Role List "+str(player),roleList[player+2])

        app.changeOptionBox("Role "+str(player),allAvailableRoles[player-1])

def colour(alignment,string):
    colours={"Town":"green","Mafia":"red","Coven":"purple","Neutral":"black"}
    alignment=alignment.split(" ")
    for i in range(0,4):
        for j in range(0,1):
            if alignment[j] in colours:
                app.getLabelWidget("Role List "+string).config(fg=colours[alignment[j]])
                break #End for loop, result found


def death(checkBox):
    for player in range(1,16):
        if app.getCheckBox("Dead "+str(player)): #==True
            app.getLabelWidget("Role List "+str(player)).config(bg="red")
        else:
            app.getLabelWidget("Role List "+str(player)).config(bg="SystemButtonFace") #Default colour for GUI

#Boolean is a good data type for this, as there are only 2 types of games (Classic & Coven).
#If anymore DLC's are released, this can be changed into an int datatype.
classic=True

##Introductory Window##

#800x600 is a size easily displayable by most screens without taking up too much room.
app = gui("Front Page","600x500")
app.winIcon = None

#Adding ToS Logo & Introductory Message
app.addImage("ToS Logo","townofsalemlogo.gif",colspan=2)
app.setImageSize("ToS Logo",540,200)
app.addLabel("Hello","A Town of Salem helper by Emma Mann",colspan=2)

#Adding Classic/Coven buttons
row=app.gr() #gr = getRow
app.addButton("Classic",lvl_1,row,0)
app.addButton("Coven",lvl_1,row,1)

#Adding Level 2 list box
app.addListBox("Level 2",["Normal","Custom","Chaos"],(row+1),0)
app.setListBoxRows("Level 2",4)
app.setListBoxSubmitFunction("Level 2",lvl_2)

#Adding Level 3 list box
app.addListBox("Level 3",["Classic","Ranked Practice","Ranked"],(row+1),1)
app.setListBoxRows("Level 3",4)

#Adding buttons to select options
app.addButton("Select Game Mode",lvl_3,(row+2),0,colspan=2)

##Second Window - this will contain the main information on the role list.##
app.startSubWindow("Role List",modal=True)
app.setPadding([2,2])

#Top text labels
app.addLabel("Intro 0","Game mode name",0,0,colspan=6)
app.getLabelWidget("Intro 0").config(font=("Sans Serif","24","bold"))
app.addLabel("Intro 1","Role list",1,0)
app.addLabel("Intro 2","Player Number/Name",1,1,colspan=2)
app.addLabel("Intro 3","Real Role",1,3)
app.addLabel("Intro 4","Dead?",1,4)
app.addLabel("Intro 5","Text",1,5)

#Add all the boxes - 15 rows in total
for player in range(1,16):
    app.addLabel("Role List "+str(player),"test",(player+1),0)
    app.addSpinBoxRange("Number "+str(player),1,15,(player+1),1)
    app.setSpinBoxWidth("Number "+str(player),3)
    app.addEntry("Name "+str(player),(player+1),2)
    app.setEntryMaxLength("Name "+str(player),16) #Maximum name length is 16 characters. It does not need to be longer.
    app.addOptionBox("Role "+str(player),[],(player+1),3)
    app.addNamedCheckBox("","Dead "+str(player),(player+1),4)
    app.setCheckBoxSubmitFunction("Dead "+str(player),death)
for textbox in range(0,3):
    app.addScrolledTextArea("Text "+str(textbox),(2+textbox*5),5,rowspan=5)

#This says that I have finished creating the Role List Window.
app.stopSubWindow()

#This window will only be required once the subroutine lvl_3 is ran.
app.hideSubWindow("Role List")

##Finally, start the gui
app.go()