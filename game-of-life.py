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

class GameOfLife:

   def __init__(self, N=100, T=200, initialize_array=[]):
      """ Set up Conway's Game of Life. """
      # Here we create two grids to hold the old and new configurations.
      # This assumes an N*N grid of points.
      # Each point is either alive or dead, represented by integer values of 1 and 0, respectively.
      self.N = N
      self.old_grid = np.zeros(N*N, dtype='i').reshape(N,N)
      self.new_grid = np.zeros(N*N, dtype='i').reshape(N,N)
      self.T = T # The maximum number of generations
      self.iteration = 0
      # Set up a random initial configuration for the grid.
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
         old_grid_end_x = int(np.ceil(N/2) + np.ceil(shape[0]/2)-1)
         old_grid_start_y = int(np.ceil(N/2) - np.ceil(shape[1]/2))
         old_grid_end_y = int(np.ceil(N/2) + np.ceil(shape[1]/2)-1)
         self.old_grid[old_grid_start_x:old_grid_end_x, old_grid_start_y:old_grid_end_y]=initialize_array
      
   def plot(self):
      pylab.pcolormesh(self.old_grid, cmap="gray_r",
                           edgecolors='cadetblue', linewidths=0.1)
      pylab.colorbar()
      pylab.savefig("generation%d.png" % self.iteration)

   def live_neighbours(self, i, j):
      """ Count the number of live neighbours around point (i, j). """
      s = 0 # The total number of live neighbours.
      # Loop over all the neighbours.
      for x in [i-1, i, i+1]:
         for y in [j-1, j, j+1]:
            if(x == i and y == j):
               continue # Skip the current point itself - we only want to count the neighbours!
            if(x != self.N and y != self.N):
               s += self.old_grid[x][y]
            # The remaining branches handle the case where the neighbour is off the end of the grid.
            # In this case, we loop back round such that the grid becomes a "toroidal array".
            elif(x == self.N and y != self.N):
               s += self.old_grid[0][y]
            elif(x != self.N and y == self.N):
               s += self.old_grid[x][0]
            else:
               s += self.old_grid[0][0]
      return s

   def play(self):
      """ Play Conway's Game of Life. """

      # Write the initial configuration to file.
      self.plot()
      
      pylab.savefig("generation0.png")

      self.iteration = 1 # Current time level
      write_frequency = 5 # How frequently we want to output a grid configuration.
      while self.iteration <= self.T: # Evolve!
         print("At time level %d" % self.iteration)

         # Loop over each cell of the grid and apply Conway's rules.
         for i in range(self.N):
            for j in range(self.N):
               live = self.live_neighbours(i, j)
               if(self.old_grid[i][j] == 1 and live < 2):
                  self.new_grid[i][j] = 0 # Dead from starvation.
               elif(self.old_grid[i][j] == 1 and (live == 2 or live == 3)):
                  self.new_grid[i][j] = 1 # Continue living.
               elif(self.old_grid[i][j] == 1 and live > 3):
                  self.new_grid[i][j] = 0 # Dead from overcrowding.
               elif(self.old_grid[i][j] == 0 and live == 3):
                  self.new_grid[i][j] = 1 # Alive from reproduction.

         # Output the new configuration.
         if(self.iteration % write_frequency == 0):
            self.plot()

         # The new configuration becomes the old configuration for the next generation.
         self.old_grid = self.new_grid.copy()

         # Move on to the next time level
         self.iteration += 1

if(__name__ == "__main__"):
   input_array = [
      [1, 1, 1, 1, 1, 0, 0],
      [1, 0, 1, 0, 0, 0, 1],
      [1, 1, 1, 0, 1, 0, 1],
   ]
   game = GameOfLife(N = 20, T = 200, initialize_array=input_array)
   game.play()

