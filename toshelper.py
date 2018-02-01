from appJar import gui

"""These are the subroutines I will be using
in my code."""


def lvl_1(Button):
    global classic
    """Why have I set this as a global variable:
    I need the changes from this subroutine to be permanent."""
    if Button == "Classic":
        classic = True
        app.setImage("ToS Logo", "townofsalemlogo.gif")
    if Button == "Coven":
        classic = False
        app.setImage("ToS Logo", "townofsalemcovenlogo.gif")


def lvl_2(selection):
    gameTypeSelection = str(app.getListBox("Level 2"))
    """app.getListBox comes out as an array, and even when
    I put it as a string, it comes out like ['Custom']"""
    gameTypeSelection = gameTypeSelection.replace("['", "").replace("']", "")
    if classic:
        """if classic: is a synonym for if classic == True:
        this means that it is checking for Classic game modes."""
        if gameTypeSelection == "Normal":
            app.updateListBox("Level 3", ["Classic",
                                          "Ranked Practice",
                                          "Ranked"])
        elif gameTypeSelection == "Custom":
            app.updateListBox("Level 3", ["Custom",
                                          "Rapid Mode"])
        else:
            app.updateListBox("Level 3", ["All Any",
                                          "Rainbow",
                                          "Vigilantics"])
    if not classic:
        """if not classic: is a synonym for if classic == False:
        this means that it is checking for Coven game modes."""
        if gameTypeSelection == "Normal":
            app.updateListBox("Level 3", ["Classic",
                                          "Ranked Practice",
                                          "Ranked",
                                          "Mafia Returns"])
        elif gameTypeSelection == "Custom":
            app.updateListBox("Level 3", ["Custom"])
        else:
            app.updateListBox("Level 3", ["All Any",
                                          "VIP Mode",
                                          "Lovers Mode",
                                          "Rivals Mode"])


def lvl_3(Button):
    gameModeSelection = str(app.getListBox("Level 3"))
    gameModeSelection = gameModeSelection.replace("['", "").replace("']", "")

    global roleList
    gameModeFile = open("game_modes.csv", "r")
    fileLines = []
    count = 0
    for line in gameModeFile.readlines():
        fileLines.append(line.split(","))
        if classic:
            if (fileLines[count][1] == gameModeSelection and
               fileLines[count][2] == "Classic"):
                fileLines[count][17] = fileLines[count][17].replace("\n", "")
                roleList = fileLines[count]
                break
                """break will end the for loop without checking any more lines.
                this is useful, because if it's found the role list, it doesn't
                need to search anymore."""
        else:
            """This will come into play if classic == False:,
            a.k.a if it needs to look for Coven game modes."""
            if (fileLines[count][1] == gameModeSelection and
               fileLines[count][2] == "Coven"):
                fileLines[count][17] = fileLines[count][17].replace("\n", "")
                roleList = fileLines[count]
                break
        count = count + 1
    gameModeFile.close()

    """Now it is time to display the Role List sub window.
    this will require changing the widgets to show the
    correct information for the game mode."""
    app.showSubWindow("Role List")
    app.setLabel("Intro 0", roleList[2] + " " + roleList[1])

    """These are the arrays I will need to find the correct information.
    This is because the role list can either define:
    1) A specific role (e.g. 'Jailor');
    2) A specific role alignment (e.g. 'Town Investigative';
    3) A specific faction (e.g. 'Random Town')
    I shortened Random Mafia to randomMaf
    and Random Neutral to randomNeu
    to correspond with PEP8 guidelines."""
    randomTown = ["Town Investigative",
                  "Town Killing",
                  "Town Protective",
                  "Town Support"]
    randomMaf = ["Mafia Deception",
                 "Mafia Killing",
                 "Mafia Support"]
    randomNeu = ["Neutral Benign",
                 "Neutral Chaos",
                 "Neutral Evil",
                 "Neutral Killing"]
    if classic:
        """In Classic, Any defines any role from the
        Town, Mafia or Neutral factions. This does not
        include Coven specific roles but this will be
        checked at a later period in the code."""
        anyRole = [randomTown,
                   randomMaf,
                   randomNeu]
    else:
        """In Coven, Any defines any role from the
        Town, Mafia, Neutral or Coven factions. Since
        Coven Specific roles are available, this means
        that every role possible currently is included."""
        anyRole = [randomTown,
                   randomMaf,
                   randomNeu,
                   "Coven Evil"]

    fileLines = find_all_roles()

    global allAvailableRoles
    allAvailableRoles = []
    """allAvailableRoles will be a 2-dimensional array.
    For each space in the role list, it will hold the
    possible roles that can be in that spot."""
    for player in range(1, 16):
        """There are 15 players in a game of ToS.
        Therefore, this code will need to run 15 times;
        once for each player."""
        availableRoles = []
        """availableRoles will be a single dimensional array.
        This will compile all the roles available for a specific
        space in the role list before being appended into
        the allAvailableRoles array."""
        for count in range(0, len(fileLines)):
            line = fileLines[count]
            if line[3] == roleList[player+2]:
                app.getButtonWidget("Role List "+str(player)).config(fg=colours[colour(line[3])])
                if (not classic or
                   line[-1] == "0\n"):
                    """This goes through in 2 seperate occasions:
                    1) It is a Coven game mode
                    2) It is a Classic game mode and the role is not
                       Coven specific.
                    line[-1] represents the last item in the array, which
                    corresponds to the Coven specific boolean indicator in
                    the roles csv file."""
                    availableRoles.append(line[1])
            if (roleList[player+2] == "Random Town" and
               any(line[3] == randomTown[x] for x in range(0, len(randomTown)))):
                app.getButtonWidget("Role List "+str(player)).config(fg=colours["Town"])
                if (not classic or
                   line[-1] == "0\n"):
                    availableRoles.append(line[1])
            if (roleList[player+2] == "Random Mafia" and
               any(line[3] == randomMaf[x] for x in range(0, len(randomMaf)))):
                app.getButtonWidget("Role List "+str(player)).config(fg=colours["Mafia"])
                if (not classic or
                   line[-1] == "0\n"):
                    availableRoles.append(line[1])
            if (roleList[player+2] == "Random Neutral" and
               any(line[3] == randomNeu[x] for x in range(0, len(randomNeu)))):
                """There is no need to change the foreground colour,
                when the faction is Neutral. This is because in the
                dictionary colours, Neutral is black, which is
                also the default colour for text."""
                if (not classic or
                   line[-1] == "0\n"):
                    availableRoles.append(line[1])
            if roleList[player+2] == "Any":
                app.getButtonWidget("Role List "+str(player)).config(fg="white")
                if (not classic or
                   line[-1] == "0\n"):
                    availableRoles.append(line[1])
            """In these next if statements, there is no
            need to check to see if the role is Coven specific.
            This is due to the nature of what it's checking:
            Firstly; when it's checking for Random Coven, because
            the Coven faction only appears in Coven game modes.
            Secondly; when it's checking for specific roles,
            since if it wasn't meant to be in the game mode,
            it wouldn't be there."""
            if (roleList[player+2] == "Random Coven" and
               line[3] == "Coven Evil"):
                app.getButtonWidget("Role List "+str(player)).config(fg=colours["Coven"])
                availableRoles.append(line[1])
            if roleList[player+2] == line[1]:
                app.getButtonWidget("Role List "+str(player)).config(fg=colours[colour(line[3])])
                availableRoles.append(line[1])
                if line[-2] == "1":
                    """When it comes to unique roles that are confirmed,
                    I need to make sure it doesn't appear anywhere else."""
                    for i in range(0, len(allAvailableRoles)):
                        for j in range(0, len(allAvailableRoles[i])):
                            if allAvailableRoles[i][j] == line[1]:
                                allAvailableRoles[i].remove(line[1])
                                break
                    fileLines[count] = ["", "", "", ""]
        allAvailableRoles.append(availableRoles)

    for player in range(1, 16):
        app.setButton("Role List "+str(player), roleList[player+2])
        app.changeOptionBox("Role "+str(player), allAvailableRoles[player-1])


def colour(alignment):
    alignment = alignment.split(" ")
    """In what this considers to be an alignment,
    the faction can either come in the first word,
    e.g. 'Town Investigative', or in the second,
    e.g. 'Random Town.'. Therefore, what this will do is
    turn it into an array of length 2.
    e.g. 'Town Investigative' -> ['Town','Investigative']"""
    for j in range(0, 1):
        if alignment[j] in colours:
            return alignment[j]


def death(checkBox):
    for player in range(1, 16):
        if app.getCheckBox("Dead "+str(player)):
            app.getButtonWidget("Role List "+str(player)).config(bg="red")
        else:
            app.getButtonWidget("Role List "+str(player)).config(bg="SystemButtonFace")
            """SystemButtonFace is the default colour for tkinter/appJar GUI's.
            If the person isn't dead, then it should return to this colour."""


def role_info(button):
    app.showSubWindow("Role Information")

    buttonName = button.split(" ")
    """button returns something along the lines of 'Role List 3',
    to be able to find the corresponding player I need to split it
    into:
    ['Role','List','3']"""
    player = int(buttonName[2])-1
    app.updateListBox("Available Roles", allAvailableRoles[player])
    app.setListBoxSubmitFunction("Available Roles", update_information)
    app.selectListItemAtPos("Available Roles", 0, callFunction=True)
    """This should work, so that it automatically
    shows the information for the top role in the list."""


def update_information(selection):
    conditions = {"Town": "Lynch every criminal and evildoer.",
                  "Mafia": "Kill anyone that will not submit to the Mafia.",
                  "Coven": "Kill all who would oppose the Coven."}

    fileLines = find_all_roles()

    roleSelection = str(app.getListBox("Available Roles"))
    roleSelection = roleSelection.replace("['", "").replace("']", "")
    info_4 = "For more information, visit http://town-of-salem.wikia.com/"

    for i in range(0, len(fileLines)):
        line = fileLines[i]
        if roleSelection == line[1]:
            app.setLabel("Role", line[1])
            x = 0
            for i in range(4, 7):
                """line[4] = Description of role
                line[5] = Abilities
                line[6] = Attributes
                line[7] = Win condition"""
                app.setMessage("Info "+str(x), line[i])
                x = x + 1
            app.setMessage("Info 4", info_4+line[1])
            """Town roles are between 1 and 19,
            Mafia roles are between 20 and 30,
            Neutral roles are between 31 and 48,
            Coven roles are between 49 and 54."""
            if 1 <= int(line[0]) < 20:
                app.setMessage("Info 3", conditions["Town"])
                app.getLabelWidget("Role").config(fg=colours["Town"])
            elif 20 <= int(line[0]) < 31:
                app.setMessage("Info 3", conditions["Mafia"])
                app.getLabelWidget("Role").config(fg=colours["Mafia"])
            elif 49 <= int(line[0]) < 55:
                app.setMessage("Info 3", conditions["Coven"])
                app.getLabelWidget("Role").config(fg=colours["Coven"])
            else:
                app.getLabelWidget("Role").config(fg=colours["Neutral"])


def find_all_roles():
    roleFile = open("roles.csv", "r")
    fileLines = []

    for line in roleFile.readlines():
        fileLines.append(line.split(","))

    roleFile.close()

    if not classic:
        """In Coven game modes, the Witch role is replaced by Coven Leader.
        Therefore, I do not need the Witch role to be available,
        if it is a Coven game mode. In this case,
        filelines[39] corresponds to the witch role."""
        fileLines.remove(fileLines[39])

    gameModesNoVamp = ["Classic",
                       "Ranked Practice",
                       "Ranked",
                       "Mafia Returns",
                       "Rivals Mode"]
    """These game modes are where Vampire Hunters
    could potentially appear, but shouldn't, since there
    are no vampires. In this case, fileLines[7]
    corresponds to the Vampire Hunter role."""
    if any(roleList[1] == gameModesNoVamp[x] for x in range(0, len(gameModesNoVamp))):
        fileLines.remove(fileLines[7])

    return fileLines

"""This is the end of the subroutines.
From this point forth is the main code."""

"""Boolean is a good data type for this,
as there are only 2 types of games (Classic & Coven).
However, if any more DLC's are released, it wouldn't work.
Therefore in that instance I would use an int datatype."""
classic = True

"""This dictionary will be used to colour
various pieces of text throughout the program,
depending on which faction is being represented."""
global colours
colours = {"Town": "green",
           "Mafia": "red",
           "Coven": "purple",
           "Neutral": "black"}

"""Here is the code for the main window.
I have preset it at 600x500px, since
it is a size easily displayable by almost
all screens without taking up too much
of the space."""
app = gui("Front Page", "600x500")

"""Here is where I shall put the decorations for the
main page. It will have a logo, that will change to
indicate whether the user is looking at Classic or
Coven game modes, and will also say a sentence about
what the program does. I have set the logo to be at
540x200px because this is the size of the larger gif file.
Beneath it I have added 2 buttons to change between
looking at Classic game modes and Coven."""
app.addImage("ToS Logo", "townofsalemlogo.gif", colspan=2)
app.setImageSize("ToS Logo", 540, 200)
app.addLabel("Hello", "A Town of Salem helper by Emma Mann", colspan=2)

row = app.gr()
app.addButton("Classic", lvl_1, row, 0)
app.addButton("Coven", lvl_1, row, 1)

"""I will be adding 2 ListBoxes:
the first one will be for Normal/Custom/Chaos,
and the second one will be for more specific game modes.
I have named them Level 2 and Level 3 accordingly.
(Where Level 1 is the buttons that switch between
Classic and Coven)
At the bottom there will be a button for the user
to select their final choice."""
app.addListBox("Level 2", ["Normal",
                           "Custom",
                           "Chaos"], (row+1), 0)
app.setListBoxRows("Level 2", 4)
app.setListBoxSubmitFunction("Level 2", lvl_2)

app.addListBox("Level 3", ["Classic",
                           "Ranked Practice",
                           "Ranked"], (row+1), 1)
app.setListBoxRows("Level 3", 4)

app.addButton("Select Game Mode", lvl_3, (row+2), 0, colspan=2)

"""From here onwards is the code for the first
sub window. This will be where most of the time
a user spends on my program will be, since
this is where they'll be able to keep track of their games.
To begin with I added text labels and made them all bold."""
app.startSubWindow("Role List", modal=True)
app.setPadding([2, 2])

app.addLabel("Intro 0", "Game mode name", 0, 0, colspan=6)
app.getLabelWidget("Intro 0").config(font=("Sans Serif", "24", "bold"))
app.addLabel("Intro 1", "Role list", 1, 0)
app.addLabel("Intro 2", "Player Number/Name", 1, 1, colspan=2)
app.addLabel("Intro 3", "Real Role", 1, 3)
app.addLabel("Intro 4", "Dead?", 1, 4)
app.addLabel("Intro 5", "Text", 1, 5)

for i in range(1, 6):
    app.getLabelWidget("Intro "+str(i)).config(font="-weight bold")

"""Now I need to add a row of boxes for each player,
15 in total. For the name box I am able to limit it to
16 characters, since that is the maximum length
for names in ToS."""
for player in range(1, 16):
    app.addNamedButton("test", "Role List "+str(player), role_info, (player+1), 0)
    app.getButtonWidget("Role List "+str(player)).config(relief="flat")
    app.addSpinBoxRange("Number "+str(player), 1, 15, (player+1), 1)
    app.setSpinBoxWidth("Number "+str(player), 3)
    app.addEntry("Name "+str(player), (player+1), 2)
    app.setEntryMaxLength("Name "+str(player), 16)
    app.addOptionBox("Role "+str(player), [], (player+1), 3)
    app.addNamedCheckBox("", "Dead "+str(player), (player+1), 4)
    app.setCheckBoxSubmitFunction("Dead "+str(player), death)
for textbox in range(0, 3):
    app.addScrolledTextArea("Text "+str(textbox), (2+textbox*5), 5, rowspan=5)

"""I am now stopping the sub window and
hiding it. It will become visible once the
user has selected a game mode and the lvl_3
subroutine is ran."""
app.stopSubWindow()
app.hideSubWindow("Role List")

"""Here is my second subwindow. This is
for users to see information about roles,
such as their abilities and attributes."""
app.startSubWindow("Role Information", modal=True)
app.setPadding([2, 2])

app.addListBox("Available Roles", [], 0, 0, rowspan=11)

app.addLabel("Role", "test", 0, 1)

app.getLabelWidget("Role").config(font=("Sans Serif", "24", "bold"))

headings = ["Description",
            "Abilities",
            "Attributes",
            "Win Condition",
            "Other"]
x = 1
for group in range(0, 5):
    app.addLabel("Heading "+str(group), headings[group], x, 1)
    app.getLabelWidget("Heading "+str(group)).config(font="-weight bold")

    x = x + 1

    app.addMessage("Info "+str(group), "Test", x, 1)
    """Messages are labels that can wrap over several lines.
    I will use this instead of a normal label because
    some of the role attributes are quite long."""
    app.setMessageWidth("Info "+str(group), "400")
    app.setMessageAnchor("Info "+str(group), "center")

    x = x + 1

"""I am now stopping this sub window
and hiding it. This will become visible when
a Role Alignment in the role list in the
first sub window is clicked."""
app.stopSubWindow()
app.hideSubWindow("Role Information")

"""At the end of all this, it is
time to start the GUI. No actual code
is after this point."""
app.go()

"""PHPMyAdmin password = UFevxHx2ThbFqsYj
PHPMyAdmin remote user = remotedb
PHPMyAdmin remote password = eNMzH43ZwfySWyqq"""
