## COS470 PROJECT 
### AI Gomoku 
#### Mason Yu
```
This is an AI Gomoku player who can compete with human
```

### Introduction of game rule
 https://en.wikipedia.org/wiki/Gomoku

### Project architecture
```
Project/
       |----__init__.py
       |----StartGame.py   ** Main UI, could be run directly
       |----configure.py   ** UI configuration function
       |----modules/
                   |----__init__.py
                   |----algorithm/
                                 |----__init__.py
                                 |----Agent.py   ** AI algorithm
                                 |----PlayWithAgent.py    ** The UI in which human could                      
                   |----ui_element/                          compete with the AI agent
                                  |----__init__.py
                                  |----Button.py          ** Button class
                                  |----Chessman.py        ** Chessman class
                                  |----Auxiliary.py       ** Some auxiliary functions
```

### Environment & required packages
```
OS: macOS
Python:  
    Version: Python3.5+ (with necessary dependencies installed)
    Packages:  pygame, PyQt5
```

### Start the game
```
1. Configure the required environment mentioned above 
2. Run "python3 StartGame.py"
```
