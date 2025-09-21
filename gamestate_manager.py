'''
Module: GameStateManager class
Description:

    The GameStateManager is an object that can be passed between functions 
    and class. Its job is to track what the current state ("page") is.
    
    For example, a typical game will have a main menu, levels, and settings.
    The GameStateManager tracks whether you are on the main menu levels or setting page.
    This can be used in the main loop of the game as a flow control. 

    The typical scructure of how to use the GameStateManager is:

    main_loop ->  initialize GameStateManager and stores all possible states
    Then, get and execute the current page (typicaly first initialized to the main menu page)
    This will run the pages run loop.

    main_menu -> tracks whether the user has triggered a page change (ie. move to levels screen)
    main_menu will set the current state to the desired state (levels for example) and return to 
    the main_loop

    main_loop -> gets the current state and executes the pages run loop. This cycle runs continuously.

    NOTE: 
    All states need to have the same function name for their run loops. They are typically named run() or draw()

Inputs: currentState (string)
Outputs: currentState (string)
External Sources: None
Authors: Abdulaziz Ali
Creation Date: 9/7/2025
'''

class GameStateManager():
    
    def __init__(self, currentState):
        '''
        Initializes the current state
        '''
        
        self.currentState = currentState
        self.params = {}

    def getState(self):
        '''
        Gets the current state
        '''
        
        return self.currentState
    
    def setState(self, newState, params=None):
        '''
        Returns the current state and store a parameters for 
        run loops that require a parameter to be passed in.
        '''
        
        self.currentState = newState
        self.params = params or {}

    def getParams(self):
        '''
        Sets the Prameters
        '''
        
        return self.params
