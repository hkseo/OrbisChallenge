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
        nest_tile = world.get_closest_enemy_nest_from(point, excluding_points)
        if nest_tile:
            world.move(unit, nest_tile.position)

    def attack_enemy(self, world, unit, excluding_points = ()):
        '''
        '''
        point = unit.position
        enemy_unit = world.get_closest_enemy_from(point, excluding_points)
        if enemy_unit:
            world.move(unit, enemy_unit.position)
    
    def do_move(self, world, friendly_units, enemy_units):
        """
        This method will get called every turn.
        
        :param world: World object reflecting current game state
        :param friendly_units: list of FriendlyUnit objects
        :param enemy_units: list of EnemyUnit objects
        """
        #for unit in friendly_units:
            #self.attack_enemy(world, unit)
        
        
    
        # Fly away to freedom, daring fireflies
        # Build thou nests
        # Grow, become stronger
        # Take over the world
        #for unit in friendly_units:
            #path = world.get_shortest_path(unit.position,
                                           #world.get_closest_capturable_tile_from(unit.position, None).position,
                                           #None)
            #if path: world.move(unit, path[0])
            
        