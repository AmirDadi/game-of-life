#!/usr/bin/env python

#  An implementation of Conway's Game of Life in Python.

#  Copyright (C) 2013 Christian Jacobs.

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import pylab
import random
from scipy.ndimage import convolve

class Rule:
   def __init__(self, current_state = 0, minimum_live_neighbores=-1, maximum_live_neighbors=np.iinfo(np.int32).max, probability=1, next_state=1):
      self.current_state = current_state
      self.minimum_live_neighbores = minimum_live_neighbores
      self.maximum_live_neighbors = maximum_live_neighbors
      self.probability = probability
      self.next_state = next_state

default_game_of_life_rules = [
      Rule(current_state = 1, maximum_live_neighbors = 2,  next_state = 0),
      Rule(current_state = 1, minimum_live_neighbores = 1, maximum_live_neighbors = 4, next_state = 1),
      Rule(current_state = 1, minimum_live_neighbores = 3, next_state = 0),
      Rule(current_state = 0, minimum_live_neighbores = 2, maximum_live_neighbors = 4, next_state = 1),     
   ]

class GameOfLife:

   def __init__(self, N=100, maximum_number_of_generation=200, initialize_array=[], write_frequency = 5, rules=default_game_of_life_rules):
    
      self.N = N
      self.grid = np.zeros(N*N, dtype='i').reshape(N,N)
      self.write_frequency = write_frequency
      self.maximum_number_of_generation = maximum_number_of_generation 
      self.iteration = 0
      self.rules = rules
      # Set up a random initial configuration for the grid if no input is given
      if (np.array(initialize_array).size == 0):
         for i in range(0, self.N):
            for j in range(0, self.N):
               if(random.randint(0, 100) < 15):
                  self.grid[i][j] = 1
               else:
                  self.grid[i][j] = 0
      else:
         shape = np.shape(initialize_array)
         grid_start_x = int(np.ceil(N/2) - np.ceil(shape[0]/2))
         grid_end_x = grid_start_x + shape[0]
         grid_start_y = int(np.ceil(N/2) - np.ceil(shape[1]/2))
         grid_end_y = grid_start_y + shape[1]
         self.grid[grid_start_x:grid_end_x, grid_start_y:grid_end_y] = initialize_array

      self.neighbours = self.live_neighbours()

   def plot(self):
      pylab.pcolormesh(self.grid, cmap="gray_r",
                           edgecolors='cadetblue', linewidths=0.1)
      pylab.savefig("generation%d.png" % self.iteration)

   def live_neighbours(self):
      kernel = np.array([ [1, 1, 1],
                     [1, 0, 1],
                     [1, 1, 1]])
      return convolve(self.grid, kernel, mode='constant')

   def apply_rules_on_element(self, i, j):
      live = self.neighbours[i][j]
      for rule in self.rules:
         if (self.grid[i][j] == rule.current_state and
            live < rule.maximum_live_neighbors and
            live > rule.minimum_live_neighbores) and np.random.rand() < rule.probability:      
            self.grid[i][j] = rule.next_state
            return

   def play(self):

      self.plot()
      
      self.iteration = 1 
      while self.iteration <= self.maximum_number_of_generation: 
         print("At time level %d" % self.iteration)

         
         self.neighbours = self.live_neighbours()
         for i in range(self.N):
            for j in range(self.N):
               self.apply_rules_on_element(i, j)
                        

         
         if(self.iteration % self.write_frequency == 0):
            self.plot()

         self.iteration += 1




if(__name__ == "__main__"):
   input_array = [
      [1, 1, 1, 1, 1, 0, 0],
      [1, 0, 1, 0, 0, 0, 1],
      [1, 1, 1, 0, 1, 0, 1],
   ]
   # input_array = [
   # [1,1],
   # [1,1]]
   # default_game_of_life_rules = [
   #    Rule(current_state = 1, maximum_live_neighbors = 2,  next_state = 0),
   #    Rule(current_state = 1, minimum_live_neighbores = 1, maximum_live_neighbors = 4, next_state = 1),
   #    Rule(current_state = 1, minimum_live_neighbores = 3, next_state = 0),
   #    Rule(current_state = 0, minimum_live_neighbores = 2, maximum_live_neighbors = 4, next_state = 1),
   # ]
   game = GameOfLife(N = 20, maximum_number_of_generation = 100, initialize_array=input_array, write_frequency = 5, rules = default_game_of_life_rules)
   game.play()

