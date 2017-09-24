from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World
import random
import time
from random import *

class PlayerAI:

    def __init__(self):
        """
            Any instantiation code goes here
        """
        self.exclusion_list = []
        self.goal_tiles = []
    
    def break_enemy_cluster(self, world, unit):
        '''
        Move towards the cluster
        '''
        cluster_point_sets = world.get_enemy_nest_clusters()
        if cluster_point_sets:
            best_dist = {}
            for c_points in cluster_point_sets:
                for c_point in list(c_points):
                    best_dist[c_point] = world.get_shortest_path_distance(unit.position, list(c_point))
            
            point = min(best_dist, key = best_dist.get)
            world.move(unit, point)
        
    
    def break_enemy_nest(self, world, unit, excluding_points = ()):
        '''
        Move towards the enemy nest. 
        Unit will destroy enemy nest once it reaches the nest's adjacent tile.
        Prioritize the cluster.
        '''
        point = unit.position            
        nest_tile = world.get_closest_enemy_nest_from(point, excluding_points)
        if nest_tile:
            world.move(unit, nest_tile)#.position)

    def attack_enemy(self, world, unit, excluding_points = ()):
        '''
        Move towards the enemy 
        once moved into the enemy's position, enemy will lose its health point
        '''
        point = unit.position
        enemy_unit = world.get_closest_enemy_from(point, excluding_points)
        if enemy_unit:
            world.move(unit, enemy_unit.position)

    def build_nest(self, world, unit, excluding_points = ()):
        '''
        1) Avoids forming cluster.
        2) Create the nest space.
        3) Aim get_friendly_nest_clustersfor nests that are far away from the enemy.
        '''
        
        point = unit.position
        friendly_cluster_points = world.get_friendly_nest_clusters()
        friendly_nest_points = world.get_friendly_nest_positions()
        neutral_tiles = world.get_neutral_tiles()
        best_dist = {}
        if not self.goal_tiles:
            for neutral_tile in neutral_tiles:
                neutral_point = neutral_tile.position
                #if the neutral point is near the cluster point or the nest point, just acquire the tile
                if self.overlaps(world, neutral_point, friendly_nest_points, friendly_cluster_points):
                    continue
                else:
                    #Heuristics: find neutral point that is further away from enemy and also close to forming the nest.
                    length = world.get_shortest_path_distance(neutral_point, world.get_closest_enemy_nest_from(neutral_point, excluding_points))*(self.num_adjacent(world, neutral_point))
                    best_dist[neutral_point] = length

        if best_dist:
            dest_point = max(best_dist, key = best_dist.get)
            self.goal_tiles.append(dest_point)
        else:
            dest_point = self.goal_tiles[0]
        friendly_tiles = world.get_friendly_tiles_around(dest_point)
        neighbours = world.get_neighbours(dest_point)
        self.exclusion_list.append(dest_point)
        if friendly_tiles:
            for key, value in neighbours.items():
                if world.get_tile_at(value) not in friendly_tiles:
                    
                    #avoids the neutral tile
                    path = world.get_shortest_path(point, value, dest_point)
                    if path:
                        print("got path")
                        world.move(unit, path[0]);
                        return
                
        
               
    
    def num_adjacent(self, world, point):
        '''
        return number of friendly tiles around the specified tile
        '''
        length = len(world.get_friendly_tiles_around(point))
        
        if length == 0:
            return 1
        elif (length == 4):
            return 0
        else:
            return length
            
        
        
    def overlaps(self, world, neutral_point, nest_points, cluster_points):
        '''
        check to see if seizing the neutral point would create a cluster
        '''
        neighbours = world.get_neighbours(neutral_point)
        
        for key,value in neighbours.items():
            n_neighbours = world.get_neighbours(value)
            for n_key, n_value in n_neighbours.items():
                #see if the point is a nest or a cluster point
                for cluster_point_set in cluster_points:
                    if ((n_value in nest_points) or (n_value in list(cluster_point_set))):
                        #occupying this neutral point will result in a creation of a cluster
                        return False
        return True

    # DEFEND NEST BEGIN ********************************************************
        
    def defend_nest_move(self, unit, world, nest_pos):
        '''
        Move unit to one of the four tiles around a nest to defend it, if it is still open
        '''
        for direction in world.get_tiles_around(nest_pos):
            dest_tile = world.get_tiles_around(nest_pos)[direction]
            if not dest_tile.is_friendly:
                world.move(unit, dest_tile.position)
                return
        # At this point, all adjacent points around nest_pos are frienldy-owned
        # Move to one at random (later, modify to move to one with lowest health)
        world.move(unit, dest_tile.position)
        
        
        
    def is_defending_nest(self, unit, world, friendly_units):
        '''
        Return True if a unit is currently defending a nest
        If so, it probably shouldn't move
        '''
        point = unit.position
        nest_pos = world.get_closest_friendly_nest_from(point, ())#.position
        if self.is_adjacent(point, nest_pos):
            return self.how_many_defending_nest(world, nest_pos, friendly_units)
        return False
     
         
    def how_many_defending_nest(self, world, point, friendly_units):
        '''
        return the number of squares adjacent to point that are held by friendly units
        '''
        tiles = world.get_friendly_tiles_around(point)
        number = 0
        positions = [tile.position for tile in tiles]
        for unit in friendly_units:
            if unit.position in positions:
                number += 1
        return number
    
    # DEFEND NEST END **********************************************************
    
       
    def acquire_tiles(self, unit, world):
        '''
        Pick a neutral/enemy tile at **random** and move onto (or towards) it. 
        Preference given to closer tiles, and then to enemy tiles
        '''
        t = time.time()
        point = unit.position
        capt_tile = world.get_closest_capturable_tile_from(point, ())
        # Account for preference to (1) closer and (2) enemy tiles
        alt_capt_tile = world.get_closest_capturable_tile_from(point, capt_tile.position) # next closest tile
        if world.get_shortest_path(point, capt_tile.position,()) == world.get_shortest_path(point, alt_capt_tile.position,()): # If both tiles are equidistant from self
            if capt_tile.is_neutral() and alt_capt_tile.is_enemy(): # And if one is an enemy tile
                capt_tile = alt_capt_tile # Then go for the enemy tile
            elif capt_tile.is_enemy() and alt_capt_tile.is_neutral():
                pass
            elif random.choice([1,2])==1: capt_tile = alt_capt_tile
        world.move(unit, capt_tile.position)
        print(1000*(time.time() - t))
            
    def is_adjacent(self, pos1, pos2):
        '''
        Return True iff position1  and position2 are adjacent
        Note: tiles wrapping around the board are considered adjacent too
        '''
        x1 = pos1[0]
        x2 = pos2[0]
        y1 = pos2[1]
        y2 = pos2[1]
        if x1==x2 and abs(y1-y2)==1: return True
        if y1==y2 and abs(x1-x2)==1: return True
        # check for wrap-arounds
        if x1==x2 and sorted([y1,y2])==[0,18]: return True
        if y1==y2 and sorted([x1,x2])==[0,18]: return True
        return False

    def do_move(self, world, friendly_units, enemy_units):
        """
        This method will get called every turn.
        
        :param world: World object reflecting current game state
        :param friendly_units: list of FriendlyUnit objects
        :param enemy_units: list of EnemyUnit objects
        """
        #1: attack enemy
        #2: break enemy nest
        #3: acquire tiles
        #4: defend nest
        print('a')
        weights = [0, 0.1, 0.4, 0.2, 0.3]
       
        for unit in friendly_units: 
            choice = random.randrange(1000)            
            
            # First priority, attack enemy unit and capture tile in the process
            enemy_pos = world.get_closest_enemy_from(unit.position,()).position
            if self.is_adjacent(enemy_pos, unit.position):
                self.attack_enemy(world,unit)
            
            # Next priority, expand into open tiles
            capt_tile = world.get_closest_capturable_tile_from(unit.position, ())     
            if self.is_adjacent(capt_tile.position, unit.position):
                self.acquire_tiles(unit,world)
                continue
            
            # Next priority, hold defended nest
            elif self.is_defending_nest(unit, world,friendly_units) in [1,2,3]:
                world.move(unit,unit.position) # hold position
                print('a')
                continue
            elif choice < 25: 
                print('attack enemy')
                self.attack_enemy(world, unit)
                continue
            elif choice < 50: 
                print('break nest')
                self.break_enemy_nest(world, unit)
                continue
            else:
                print('acquire tiles')
                self.acquire_tiles(unit, world)
                continue
            '''else:
                path = world.get_shortest_path(unit.position,
                                               world.get_closest_capturable_tile_from(unit.position, None).position, None)
                if path: world.move(unit, path[0]) '''               
            '''
            elif choice <=1000:
                print('defending nest')
                nest_pos = world.get_closest_enemy_nest_from(unit.position,())
                self.defend_nest_move(unit, world, nest_pos)'''
                                      
    
        #for unit in friendly_units:
        #self.build_nest(world,friendly_units[0], self.exclusion_list)
            #self.break_enemy_cluster(world, unit, self.exclusion_list)
            #self.break_enemy_nest(world, unit, self.exclusion_list)
            #self.attack_enemy(world, unit, self.exclusion_list)
            
    
        # Fly away to freedom, daring fireflies
        # Build thou nests
        # Grow, become stronger, 
        # Take over the world
        #for unit in friendly_units:
            #path = world.get_shortest_path(unit.position,
                                           #world.get_closest_capturable_tile_from(unit.position, None).position,
                                           #None)
            #if path: world.move(unit, path[0])
            
        