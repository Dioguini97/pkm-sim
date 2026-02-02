"""
Main game entry point with scene management system.
"""
import pygame
import sys
from typing import Optional, Dict, Any


class SceneManager:
    """Manages different game scenes (Menu, Team Builder, Battle, etc.)"""

    def __init__(self):
        self.scenes: Dict[str, 'Scene'] = {}
        self.current_scene: Optional['Scene'] = None
        self.next_scene: Optional[str] = None

    def add_scene(self, name: str, scene: 'Scene'):
        """Add a scene to the manager"""
        self.scenes[name] = scene
        scene.manager = self

    def set_scene(self, name: str, **kwargs):
        """Switch to a different scene"""
        if name not in self.scenes:
            raise ValueError(f"Scene '{name}' not found")

        if self.current_scene:
            self.current_scene.on_exit()

        self.current_scene = self.scenes[name]
        self.current_scene.on_enter(**kwargs)

    def update(self, dt: float):
        """Update current scene"""
        if self.current_scene:
            self.current_scene.update(dt)

    def handle_event(self, event: pygame.event.Event):
        """Handle event in current scene"""
        if self.current_scene:
            self.current_scene.handle_event(event)

    def draw(self, screen: pygame.Surface):
        """Draw current scene"""
        if self.current_scene:
            self.current_scene.draw(screen)


class Scene:
    """Base class for all game scenes"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.manager: Optional[SceneManager] = None

    def on_enter(self, **kwargs):
        """Called when scene becomes active"""
        pass

    def on_exit(self):
        """Called when scene becomes inactive"""
        pass

    def update(self, dt: float):
        """Update scene logic"""
        pass

    def handle_event(self, event: pygame.event.Event):
        """Handle input events"""
        pass

    def draw(self, screen: pygame.Surface):
        """Draw scene"""
        pass


class Game:
    """Main game class"""

    def __init__(self, width: int = 1280, height: int = 720):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pokémon Battle Simulator")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60

        # Initialize scene manager
        self.scene_manager = SceneManager()
        self._setup_scenes()

    def _setup_scenes(self):
        """Initialize all game scenes"""
        from scenes.menu_scene import MenuScene
        from scenes.team_builder_scene import TeamBuilderScene
        from scenes.battle_scene import BattleScene

        # Create scenes
        menu = MenuScene(self.screen)
        team_builder = TeamBuilderScene(self.screen)
        battle = BattleScene(self.screen)

        # Add scenes to manager
        self.scene_manager.add_scene("menu", menu)
        self.scene_manager.add_scene("team_builder", team_builder)
        self.scene_manager.add_scene("battle", battle)

        # Start with menu
        self.scene_manager.set_scene("menu")

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            # Pass event to current scene
            self.scene_manager.handle_event(event)

    def update(self):
        """Update game logic"""
        dt = self.clock.get_time() / 1000.0  # Convert to seconds
        self.scene_manager.update(dt)

    def draw(self):
        """Draw everything"""
        self.screen.fill((0, 0, 0))  # Clear screen
        self.scene_manager.draw(self.screen)
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()