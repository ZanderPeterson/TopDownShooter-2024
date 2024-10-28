from math import pi
from random import randint
from typing import Any, Dict, List, override, Tuple, TypeAlias

import pygame

from .game_state import GameState
from src.objects import GameObject, PlayerObject, BulletObject, WallObject, EnemyObject
from src.utils import check_collision, find_radius_of_square, find_vector_between, move_by_vector, orbit_around_circle

Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction


class PlayGameState(GameState):

    def __init__(self, game) -> None:
        super().__init__(game)
        self.track_keys: Dict[int, bool] = {
            pygame.K_w: False,
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_d: False,
        }
        self.track_clicks: Dict[int, bool] = {
            1: False, #Left Click
            2: False, #Middle Click
            3: False, #Right Click
        }
        self.constants: Dict[str, Any] = {
            "forward_speed": 4,
            "backward_speed": 4,
            "sideways_speed": 4,
            "bullet_speed": 8,
            "fire_rate": 30,
            "enemy_fire_rate": 60*2.5,
            "spawn_rate": 60*3,
        }
        self.game_variables: Dict[str, Any] = {}
        self.enemy_spawn_locations: List[Tuple[bool, coords]] = []
        self.entities: Dict[str, GameObject] = {}
        self.bullets: List[BulletObject] = []
        self.walls: List[WallObject] = []
        self.font: pygame.font.FontType = pygame.font.Font(None, 50)

        #Corners
        self.walls.append(WallObject(start_pos=(0, 0)))
        self.walls.append(WallObject(start_pos=(0, 608)))
        self.walls.append(WallObject(start_pos=(768, 0)))
        self.walls.append(WallObject(start_pos=(768, -608)))

        #Main Walls
        self.walls.append(WallObject(start_pos=(0, -768),
                                     image="wall_800x800.png"))
        self.walls.append(WallObject(start_pos=(0, 608),
                                     image="wall_800x800.png"))
        self.walls.append(WallObject(start_pos=(768, 0),
                                     image="wall_800x800.png"))
        self.walls.append(WallObject(start_pos=(-768, 0),
                                     image="wall_800x800.png"))

        #Middle Island/Wall
        self.walls.append(WallObject(start_pos=(250, 270),
                                     image="wall_100x100.png"))
        self.walls.append(WallObject(start_pos=(350, 270),
                                     image="wall_100x100.png"))
        self.walls.append(WallObject(start_pos=(450, 270),
                                     image="wall_100x100.png"))

    @override
    def enter(self) -> None:
        for key in self.track_keys.keys():
            self.track_keys[key] = False

        for click in self.track_clicks.keys():
            self.track_clicks[click] = False

        self.game_variables = {
            "score": 0,
            "time_before_next_shot": 0,
            "time_before_next_spawn": 0,
            "health": 8,
        }

        self.enemy_spawn_locations = [
            (False, (200-16, 160-16)),
            (False, (400-16, 160-16)),
            (False, (600-16, 160-16)),
            (False, (200-16, 480-16)),
            (False, (400-16, 480-16)),
            (False, (600-16, 480-16))
        ]

        self.entities = {}
        self.bullets = []

        self.entities["player"] = PlayerObject(start_pos=(100 - 16, 100 - 16),
                                               forward_speed=self.constants["forward_speed"],
                                               backward_speed=self.constants["backward_speed"],
                                               sideways_speed=self.constants["sideways_speed"],
                                               image="player.png")

    @override
    def exit(self) -> None:
        pass

    @override
    def update(self) -> None | str:
        #Updates the score
        self.game_variables["score"] += 1

        #Gets position of the mouse, and finds the Vector from the centre of the player to it.
        mouse_pos = pygame.mouse.get_pos()
        vector_to_cursor: Vector = find_vector_between(self.entities["player"].centre, mouse_pos)

        #Rotates the player to look at the mouse.
        self.entities["player"].set_rotation(vector_to_cursor[1])

        #Code that backs the player away from the cursor if the cursor is too close to the player's centre.
        if vector_to_cursor[0] < 10:
            self.entities["player"].move_backward(vector_to_cursor, move_by=10-vector_to_cursor[0])

        #A & D Movement Code
        if not (self.track_keys[pygame.K_a] and self.track_keys[pygame.K_d]):
            if self.track_keys[pygame.K_a]:
                self.entities["player"].move_leftward(vector_to_cursor)
            elif self.track_keys[pygame.K_d]:
                self.entities["player"].move_rightward(vector_to_cursor)

        #W & S Movement Code
        if not (self.track_keys[pygame.K_w] and self.track_keys[pygame.K_s]):
            if self.track_keys[pygame.K_w]:
                self.entities["player"].move_forward(vector_to_cursor)
            elif self.track_keys[pygame.K_s]:
                self.entities["player"].move_backward(vector_to_cursor)

        #Checks for collision between the player and the walls.
        for wall in self.walls:
            move_by: Vector = (0, 0)
            move_by = check_collision(wall.centre,
                                      lambda theta: find_radius_of_square(wall.img_size[0], theta-(wall.rotation)),
                                      self.entities["player"].centre,
                                      lambda theta: self.entities["player"].img_size[0]/2)
            self.entities["player"].move_by_amount(move_by_vector((0, 0), move_by))

        #Countdown the time before next shot.
        if self.game_variables["time_before_next_shot"] > 0:
            self.game_variables["time_before_next_shot"] -= 1

        #Spawn Player's Projectiles Code
        if self.track_clicks[1]:
            if self.game_variables["time_before_next_shot"] <= 0:
                new_bullet: BulletObject = BulletObject(rotation=self.entities["player"].rotation,
                                                        speed=self.constants["bullet_speed"],
                                                        shot_by="player",
                                                        grace_period=10,
                                                        image="bullet.png")
                new_bullet.set_position_by_centre(self.entities["player"].centre)
                self.bullets.append(new_bullet)
                self.game_variables["time_before_next_shot"] = self.constants["fire_rate"]

        #Update Enemies Code (and spawn the Enemies' Projectiles)
        for enemy in self.entities.values():
            if enemy.tag != "enemy":
                #Enemy is actually something else, like the player
                continue
            enemy.update()
            enemy.aim_in_direction(self.entities["player"].position)
            if enemy.check_if_shot_allowed():
                new_bullet: BulletObject = BulletObject(rotation=enemy.find_direction_to_shoot(),
                                                        speed=self.constants["bullet_speed"],
                                                        shot_by=None,
                                                        grace_period=10,
                                                        image="bullet.png")
                new_bullet.set_position_by_centre(enemy.get_centre_position())
                self.bullets.append(new_bullet)


        #Updates all bullet positions.
        for bullet in self.bullets:
            hit_targets: List[GameObject | PlayerObject | EnemyObject] = bullet.update(self.walls, list(self.entities.values()))
            for target in hit_targets:
                #Something got hit
                self.bullets.pop(self.bullets.index(bullet))
                if target.tag == "player":
                    #Player got hit
                    self.game_variables["health"] -= 1
                elif target.tag == "enemy":
                    #An enemy got hit
                    target.health -= 1

        #Remove Enemies
        entities_to_remove: List[str] = []
        for key, entity in self.entities.items():
            if entity.tag != "enemy":
                # Enemy is actually something else, like the player
                continue
            enemy: EnemyObject | GameObject = entity
            #Check if enemy is dead
            if enemy.health <= 0:
                for i, location in enumerate(self.enemy_spawn_locations):
                    if location[1] == enemy.position:
                        self.enemy_spawn_locations[int(key)] = (False, location[1])
                entities_to_remove.append(key)
        for entity in entities_to_remove:
            self.entities.pop(entity)

        # Countdown the time before next spawn
        if self.game_variables["time_before_next_spawn"] > 0:
            self.game_variables["time_before_next_spawn"] -= 1

        if self.game_variables["time_before_next_spawn"] <= 0:
            self.game_variables["time_before_next_spawn"] = self.constants["spawn_rate"]
            #Spawn Enemies
            available_spots: List[int] = []
            for i, spot in enumerate(self.enemy_spawn_locations):
                if not spot[0]:
                    #Spot is unoccupied
                    available_spots.append(i)
            if len(available_spots) > 0:
                chosen_spot: int = available_spots[randint(0, len(available_spots) - 1)]
                self.enemy_spawn_locations[chosen_spot] = (True, self.enemy_spawn_locations[chosen_spot][1])
                self.entities[str(chosen_spot)] = EnemyObject(start_pos=self.enemy_spawn_locations[chosen_spot][1],
                                                              start_hp=3,
                                                              cooldown=self.constants["enemy_fire_rate"],
                                                              accuracy=0.5,
                                                              image="enemy.png")

        # Check player health
        if self.game_variables["health"] <= 0:
            return "GameOver"

    @override
    def render(self, window) -> None:
        #Renders the background.
        window.fill((0, 0, 0))

        #Loops through all the entities and renders them to the screen.
        for entity in self.entities.values():
            window.blit(entity.render_image(), entity.get_image_position())

        # Loops through all the bullets and renders them to the screen.
        for bullet in self.bullets:
            window.blit(bullet.render_image(), bullet.get_image_position())

        # Loops through all the bullets and renders them to the screen.
        for wall in self.walls:
            window.blit(wall.render_image(), wall.get_image_position())

        score_text = self.font.render(f"Score: {self.game_variables["score"]}", True, (254, 255, 240))
        health_text = self.font.render(f"Health: {self.game_variables["health"]}", True, (254, 255, 240))
        window.blit(score_text, (400 - score_text.get_size()[0]/2, 300 - score_text.get_size()[1]/2))
        window.blit(health_text, (400 - health_text.get_size()[0] / 2, 340 - health_text.get_size()[1] / 2))

    @override
    def handle_event(self, event) -> None | str:
        #Record down keypresses.
        if event.type == pygame.KEYDOWN and event.key in self.track_keys:
            self.track_keys[event.key] = True
        elif event.type == pygame.KEYUP and event.key in self.track_keys:
            self.track_keys[event.key] = False

        #Record down mouse clicks.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button in self.track_clicks:
            self.track_clicks[event.button] = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button in self.track_clicks:
            self.track_clicks[event.button] = False
        return None
