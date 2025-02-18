"""
This the primary class for the Mario Expert agent. It contains the logic for the Mario Expert agent to play the game and choose actions.

Your goal is to implement the functions and methods required to enable choose_action to select the best action for the agent to take.

Original Mario Manual: https://www.thegameisafootarcade.com/wp-content/uploads/2017/04/Super-Mario-Land-Game-Manual.pdf
"""

import json
import logging
import random

import cv2
from mario_environment import MarioEnvironment
from pyboy.utils import WindowEvent


class MarioController(MarioEnvironment):
    """
    The MarioController class represents a controller for the Mario game environment.

    You can build upon this class all you want to implement your Mario Expert agent.

    Args:
        act_freq (int): The frequency at which actions are performed. Defaults to 10.
        emulation_speed (int): The speed of the game emulation. Defaults to 0.
        headless (bool): Whether to run the game in headless mode. Defaults to False.
    """

    def __init__(
        self,
        act_freq: int = 1,
        emulation_speed: int = 0,
        headless: bool = False,
    ) -> None:
        super().__init__(
            act_freq=act_freq,
            emulation_speed=emulation_speed,
            headless=headless,
        )

        self.act_freq = act_freq

        # Example of valid actions based purely on the buttons you can press
        valid_actions: list[WindowEvent] = [
            WindowEvent.PRESS_ARROW_DOWN,
            WindowEvent.PRESS_ARROW_LEFT,
            WindowEvent.PRESS_ARROW_RIGHT,
            WindowEvent.PRESS_ARROW_UP,
            WindowEvent.PRESS_BUTTON_A,
            WindowEvent.PRESS_BUTTON_B,
            
        ]

        release_button: list[WindowEvent] = [
            WindowEvent.RELEASE_ARROW_DOWN,
            WindowEvent.RELEASE_ARROW_LEFT,
            WindowEvent.RELEASE_ARROW_RIGHT,
            WindowEvent.RELEASE_ARROW_UP, 
            WindowEvent.RELEASE_BUTTON_A,
            WindowEvent.RELEASE_BUTTON_B,
        ]
        

        self.valid_actions = valid_actions
        self.release_button = release_button
        #Map Input strings to actions
        self.mappings = {
            "Up": WindowEvent.PRESS_ARROW_UP,
            "Down": WindowEvent.PRESS_ARROW_DOWN,
            "Left": WindowEvent.PRESS_ARROW_LEFT,
            "Right": WindowEvent.PRESS_ARROW_RIGHT,
            "B": WindowEvent.PRESS_BUTTON_B,
            "A": WindowEvent.PRESS_BUTTON_A,
            
        }
        self.release_mappings = {
            "Up": WindowEvent.RELEASE_ARROW_UP,
            "Down": WindowEvent.RELEASE_ARROW_DOWN,
            "Left": WindowEvent.RELEASE_ARROW_LEFT,
            "Right": WindowEvent.RELEASE_ARROW_RIGHT,
            "B": WindowEvent.RELEASE_BUTTON_B,
            "A": WindowEvent.RELEASE_BUTTON_A,
            
        }
        self.previous =[]
        with open('Input Log.txt', 'r') as file:
            file_content = file.read()
        
        self.inputs = self.parse_tas_input(file_content)
        print(self.inputs)
        

    def parse_tas_input(self, file_content):
        lines = file_content.split('\n')
        
        # Check if the file is empty
        if not lines:
            print("Error: The input file is empty.")
            return []

        # Parse the key mappings
        try:
            key_mapping_line = next(line for line in lines if line.startswith('LogKey:'))
            key_mapping = key_mapping_line.split(':')[1].strip('#').split('|')
        except StopIteration:
            print("Error: Could not find 'LogKey:' line in the input file.")
            return []
        except IndexError:
            print("Error: 'LogKey:' line is not in the expected format.")
            return []

        inputs = []
        input_started = False
        for line in lines:
            if line == '[Input]':
                input_started = True
                continue
            if line == '[/Input]':
                break
            if input_started and line.startswith('|') and line.endswith('|'):
                frame_input = []
                for i, char in enumerate(line[1:-1]):  # Exclude the first and last '|'
                    if char != '.' and i < len(key_mapping):
                        frame_input.append(key_mapping[i])
                inputs.append(tuple(frame_input))

        return inputs

    def run_action(self) -> None:
        """
        This is a very basic example of how this function could be implemented

        As part of this assignment your job is to modify this function to better suit your needs

        You can change the action type to whatever you want or need just remember the base control of the game is pushing buttons
        """

        if(len(self.inputs) > 0):
            current_input = self.inputs[0]
            # Release previous inputs if not in current input
            for item in self.previous:
                if(item != "Start"):
                    if(item not in self.inputs[0]):
                        self.pyboy.send_input(self.release_mappings[item])
            
            print("Input ",43792- len(self.inputs))
            
            for item in self.inputs[0]:
                print(item)
                if(item != "Start"):
                    self.pyboy.send_input(self.mappings[item])
                    
            self.previous = current_input
            
            #Remove the first item in the list
            self.inputs.pop(0)
        
        self.pyboy.tick(1, True)
        

        
    
    def manual_control(self):
        print("Position", self.get_x_position())
        self.pyboy.send_input(self.valid_actions[-1])

        for _ in range(self.act_freq):
            self.pyboy.tick()

        self.pyboy.send_input(self.release_button[-1])

    


    
        


class MarioExpert:
    """
    The MarioExpert class represents an expert agent for playing the Mario game.

    Edit this class to implement the logic for the Mario Expert agent to play the game.

    Do NOT edit the input parameters for the __init__ method.

    Args:
        results_path (str): The path to save the results and video of the gameplay.
        headless (bool, optional): Whether to run the game in headless mode. Defaults to False.
    """

    def __init__(self, results_path: str, headless=False):
        self.results_path = results_path

        self.environment = MarioController(headless=headless)

        self.video = None

    def choose_action(self):
        state = self.environment.game_state()
        frame = self.environment.grab_frame()
        game_area = self.environment.game_area()
        x_pos = self.environment.get_x_position()
        
        action = -1

        # Implement your code here to choose the best action
        # time.sleep(0.1)
        #print(game_area)

        """ for rows, row in enumerate(game_area):
            for cols, col in enumerate(row):
                if col == 1 and mario_row == -1:
                    print(f"Mario at Row: {rows}, Col: {cols}")
                    mario_row = rows
                    mario_col = cols
                if col == 13:
                    question_blocks.append(cols)
                    print(f"Question Block Col: {cols}") """

        
        
        if x_pos >= 100:
            action = 4
        
        else:
            action = 2
        print(action)
            
        return action
        
        
        
   

    def step(self):
        """
        Modify this function as required to implement the Mario Expert agent's logic.

        This is just a very basic example
        """

        # Choose an action - button press or other...
        self.environment.manual_control()
        return 
        
        # Process up to 60 frames at a time, or fewer if there aren't 60 inputs left
        frames_to_process = min(60, len(self.environment.inputs))
        
        for _ in range(frames_to_process):
            self.environment.run_action()
        
        # If we've run out of inputs, we can stop the emulation
        if len(self.environment.inputs) == 0:
            return False
        
        return True

    def play(self):
        """
        Do NOT edit this method.
        """
        self.environment.reset()

        frame = self.environment.grab_frame()
        height, width, _ = frame.shape

        self.start_video(f"{self.results_path}/mario_expert.mp4", width, height)

        while not self.environment.get_game_over():
            frame = self.environment.grab_frame()
            self.video.write(frame)

            self.step()

        final_stats = self.environment.game_state()
        logging.info(f"Final Stats: {final_stats}")

        with open(f"{self.results_path}/results.json", "w", encoding="utf-8") as file:
            json.dump(final_stats, file)

        self.stop_video()

    def start_video(self, video_name, width, height, fps=30):
        """
        Do NOT edit this method.
        """
        self.video = cv2.VideoWriter(
            video_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
        )

    def stop_video(self) -> None:
        """
        Do NOT edit this method.
        """
        self.video.release()
