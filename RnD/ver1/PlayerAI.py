from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World

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
        nest_tile = get_closest_enemy_nest_from(point, excluding_points)
        if nest_tile:
            world.move(unit, nest_tile.position)

    def attack_enemy(self, world):
        '''
        '''
    
    # DEFEND NEST BEGIN ********************************************************
        
    def defend_nest_move(self, unit, world, nest_pos, enemy_units):
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
        
        
        
    def is_defending_nest(self, unit, world):
        '''
        Return True if a unit is currently defending a nest
        If so, it probably shouldn't move
        '''
        point = unit.position
        if is_adjacent(point, get_closest_friendly_nest_from(point, excluding_points).position):
            return True
        return False
     
         
    def is_defended(self, world, point):
        '''
        return the number of squares adjacent to point that are held by friendly units
        '''
        return len(world.get_friendly_tiles_around(point))
    
    # DEFEND NEST END **********************************************************
    
        
    def acquire_tiles(self, unit, world):
        '''
        Pick a neutral/enemy tile at random and move onto (or towards) it. 
        Preference given to closer tiles, and then to enemy tiles
        '''
        point = unit.position
        capt_tile = world.get_closest_capturable_tile_from(point)
        # Account for preference to (1) closer and (2) enemy tiles
        while True:
            alt_capt_tile = get_closest_capturable_tile_from(point, capt_pos) # next closest tile
            if world.get_shortest_path(point, capt_tile.position) == world.get_shortest_path(point, alt_capt_tile.position): # If both tiles are equidistant from self
                if capt_tile.is_neutral() and alt_capt_tile.is_enemy(): # And if one is an enemy tile
                    capt_tile = alt_capt_tile # Then go for the enemy tile
                    break
            else: # Just stick with the original (nearsest) tile
                break
        world.move(unit, capt_tile.position)
        
            
    def is_adjacent(self, pos1, pos2):
        '''
        Return True iff position1  and position2 are adjacent
        Note: tiles wrapping around the board are considered adjacent too
        '''
        x1 = pos1[0]
        x2 = pos2[0]
        y1 = pos2[1]
        y1 = pos2[1]
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
        return
        # Fly away to freedom, daring fireflies
        # Build thou nests
        # Grow, become stronger
        # Take over the world
        #for unit in friendly_units:
            #path = world.get_shortest_path(unit.position,
                                           #world.get_closest_capturable_tile_from(unit.position, None).position,
                                           #None)
            #if path: world.move(unit, path[0])
            
        