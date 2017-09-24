from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World
import random
import time

class PlayerAI:

    def __init__(self):
        """
            Any instantiation code goes here
        """
        pass

    
    def break_enemy_nest(self, world, unit, excluding_points = ()):
        '''
        '''
        point = unit.position
        nest_tile = world.get_closest_enemy_nest_from(point, excluding_points)
        if nest_tile:
            world.move(unit, nest_tile)#.position)

    def attack_enemy(self, world, unit, excluding_points = ()):
        '''
        '''
        point = unit.position
        enemy_unit = world.get_closest_enemy_from(point, excluding_points)
        if enemy_unit:
            world.move(unit, enemy_unit.position)
    
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
                                      
    
            
        