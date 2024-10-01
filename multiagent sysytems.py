import tkinter as tk
from tkinter import ttk
import random
import time
import threading

class TrafficSignalAgent:
    def __init__(self, name, display_frame):
        self.name = name
        self.green_light_duration = 10  # default green light duration
        self.traffic_density = random.randint(1, 10)  # random traffic density
        self.neighboring_agents = []  # list of neighboring agents
        self.display_frame = display_frame  # frame to display traffic light info

        # Create title and labels within the frame
        self.title_label = tk.Label(self.display_frame, text=self.name, font=("Arial", 14, "bold"))
        self.title_label.pack(pady=5)
        
        self.info_label = tk.Label(self.display_frame, text=f"Traffic Density: {self.traffic_density}\nGreen Light: {self.green_light_duration}s", font=("Arial", 12))
        self.info_label.pack(pady=5)
        
        self.color_label = tk.Label(self.display_frame, text="", width=20, height=3, bg="gray")
        self.color_label.pack(pady=5)

    def set_neighbors(self, agents):
        self.neighboring_agents = agents
    
    def adjust_light_duration(self):
        # Adjust light duration based on local traffic density
        if self.traffic_density > 7:
            self.green_light_duration += 5
        elif self.traffic_density < 3:
            self.green_light_duration -= 3
        
        # Ensure green light duration stays within reasonable bounds
        self.green_light_duration = max(5, min(self.green_light_duration, 20))
    
    def communicate_with_neighbors(self):
        # Adjust neighbor's green light durations based on the traffic conditions
        for neighbor in self.neighboring_agents:
            # If traffic density is high, ask neighbors to increase their green light duration
            if self.traffic_density > 7:
                neighbor.green_light_duration += 2
                neighbor.green_light_duration = min(neighbor.green_light_duration, 20)
            # If traffic density is low, ask neighbors to reduce their green light duration
            elif self.traffic_density < 3:
                neighbor.green_light_duration -= 2
                neighbor.green_light_duration = max(neighbor.green_light_duration, 5)
    
    def operate(self):
        # Simulate traffic density change
        self.traffic_density = random.randint(1, 10)
        self.adjust_light_duration()
        self.communicate_with_neighbors()
        
        # Update display with current information
        self.info_label.config(text=f"Traffic Density: {self.traffic_density}\nGreen Light: {self.green_light_duration}s")
        
        # Update color to represent the light status based on traffic density
        if self.traffic_density > 7:
            self.color_label.config(bg="green", text="Green")
        elif self.traffic_density > 3:
            self.color_label.config(bg="orange", text="Orange")
        else:
            self.color_label.config(bg="red", text="Red")

class TrafficSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Signal Simulator - 4 Intersections")
        
        # Create the layout grid
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create frames for each traffic signal agent
        self.agent1_frame = ttk.Frame(self.frame, borderwidth=2, relief="sunken")
        self.agent1_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        self.agent2_frame = ttk.Frame(self.frame, borderwidth=2, relief="sunken")
        self.agent2_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        self.agent3_frame = ttk.Frame(self.frame, borderwidth=2, relief="sunken")
        self.agent3_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        self.agent4_frame = ttk.Frame(self.frame, borderwidth=2, relief="sunken")
        self.agent4_frame.grid(row=1, column=1, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        # Create traffic signal agents
        self.agent1 = TrafficSignalAgent("Intersection 1", self.agent1_frame)
        self.agent2 = TrafficSignalAgent("Intersection 2", self.agent2_frame)
        self.agent3 = TrafficSignalAgent("Intersection 3", self.agent3_frame)
        self.agent4 = TrafficSignalAgent("Intersection 4", self.agent4_frame)
        
        # Set neighboring relationships
        self.agent1.set_neighbors([self.agent2, self.agent3])
        self.agent2.set_neighbors([self.agent1, self.agent4])
        self.agent3.set_neighbors([self.agent1, self.agent4])
        self.agent4.set_neighbors([self.agent2, self.agent3])
        
        # Start button
        self.start_button = ttk.Button(self.frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.running = False
    
    def start_simulation(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        threading.Thread(target=self.run_simulation).start()

    def run_simulation(self):
        for cycle in range(5):  # Simulate 5 cycles
            if not self.running:
                break
            
            # Update each agent in the simulation
            self.agent1.operate()
            self.agent2.operate()
            self.agent3.operate()
            self.agent4.operate()
            
            # Pause to simulate real-time operation
            time.sleep(2)
        
        self.running = False
        self.start_button.config(state=tk.NORMAL)

# Initialize the Tkinter window
root = tk.Tk()
app = TrafficSimulatorApp(root)

# Start the Tkinter event loop
root.mainloop()
