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

   def __init__(self, N=100, maximum_number_of_generation=200, initialize_array=[]):
    
      self.N = N
      self.old_grid = np.zeros(N*N, dtype='i').reshape(N,N)
      self.maximum_number_of_generation = maximum_number_of_generation # The maximum number of generations
      self.iteration = 0
      # Set up a random initial configuration for the grid if no input is given
      if (np.array(initialize_array).size == 0):
         for i in range(0, self.N):
            for j in range(0, self.N):
               if(random.randint(0, 100) < 15):
                  self.old_grid[i][j] = 1
               else:
                  self.old_grid[i][j] = 0
      else:
         shape = np.shape(initialize_array)
         old_grid_start_x = int(np.ceil(N/2) - np.ceil(shape[0]/2))
         old_grid_end_x = old_grid_start_x + shape[0]
         old_grid_start_y = int(np.ceil(N/2) - np.ceil(shape[1]/2))
         old_grid_end_y = old_grid_start_y + shape[1]
         self.old_grid[old_grid_start_x:old_grid_end_x, old_grid_start_y:old_grid_end_y]=initialize_array

      self.neighbours = self.live_neighbours()

   def plot(self):
      pylab.pcolormesh(self.old_grid, cmap="gray_r",
                           edgecolors='cadetblue', linewidths=0.1)
      pylab.savefig("generation%d.png" % self.iteration)

   def live_neighbours(self):
      kernel = np.array([ [1, 1, 1],
                     [1, 0, 1],
                     [1, 1, 1]])
      return convolve(self.old_grid, kernel, mode='constant')

   def apply_default_rules_on_element(self, i, j):
      live = self.neighbours[i][j]
      if(self.old_grid[i][j] == 1 and  live < 2):
         self.old_grid[i][j] = 0 # Dead from starvation.
      elif(self.old_grid[i][j] == 1 and (live == 2 or live == 3)):
         self.old_grid[i][j] = 1 # Continue living.
      elif(self.old_grid[i][j] == 1 and live > 3):
         self.old_grid[i][j] = 0 # Dead from overcrowding.
      elif(self.old_grid[i][j] == 0 and live == 3):
         self.old_grid[i][j] = 1 # Alive from reproduction.

   def play(self):

      self.plot()
      
      self.iteration = 1 
      write_frequency = 5 
      while self.iteration <= self.maximum_number_of_generation: 
         print("At time level %d" % self.iteration)

         
         self.neighbours = self.live_neighbours()
         for i in range(self.N):
            for j in range(self.N):
               self.apply_default_rules_on_element(i, j)
                        

         
         if(self.iteration % write_frequency == 0):
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
   game = GameOfLife(N = 20, maximum_number_of_generation = 200, initialize_array=input_array)
   game.play()

