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

class GameOfLife:

   def __init__(self, N=100, maximum_number_of_generation=200, initialize_array=[], write_frequency = 5):
    
      self.N = N
      self.grid = np.zeros(N*N, dtype='i').reshape(N,N)
      self.write_frequency = 5
      self.maximum_number_of_generation = maximum_number_of_generation 
      self.iteration = 0
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

   def apply_default_rules_on_element(self, i, j):
      live = self.neighbours[i][j]
      if(self.grid[i][j] == 1 and  live < 2):
         self.grid[i][j] = 0 # Dead from starvation.
      elif(self.grid[i][j] == 1 and (live == 2 or live == 3)):
         self.grid[i][j] = 1 # Continue living.
      elif(self.grid[i][j] == 1 and live > 3):
         self.grid[i][j] = 0 # Dead from overcrowding.
      elif(self.grid[i][j] == 0 and live == 3):
         self.grid[i][j] = 1 # Alive from reproduction.

   def play(self):

      self.plot()
      
      self.iteration = 1 
      while self.iteration <= self.maximum_number_of_generation: 
         print("At time level %d" % self.iteration)

         
         self.neighbours = self.live_neighbours()
         for i in range(self.N):
            for j in range(self.N):
               self.apply_default_rules_on_element(i, j)
                        

         
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
   game = GameOfLife(N = 20, maximum_number_of_generation = 200, initialize_array=input_array, write_frequency = 5)
   game.play()

