"""
Main menu scene.
"""
import pygame

from pkm_sim.ui.game import Scene
from pkm_sim.ui.ui_components import TextLabel, Color, Button


class MenuScene(Scene):
    """Main menu of the game"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

        # Get screen dimensions
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Create UI elements
        self._create_ui()

    def _create_ui(self):
        """Create all UI elements"""
        # Title
        self.title = TextLabel(
            self.width // 2,
            100,
            "POKÉMON BATTLE SIMULATOR",
            font_size=64,
            color=Color.WHITE,
            center=True,
            bold=True
        )

        # Buttons
        button_width = 300
        button_height = 60
        button_x = (self.width - button_width) // 2
        start_y = 300
        spacing = 80

        self.buttons = []

        # Team Builder button
        self.team_builder_btn = Button(
            button_x,
            start_y,
            button_width,
            button_height,
            "TEAM BUILDER",
            callback=self._on_team_builder_click,
            font_size=32,
            bg_color=Color.BLUE
        )
        self.buttons.append(self.team_builder_btn)

        # Quick Battle button
        self.quick_battle_btn = Button(
            button_x,
            start_y + spacing,
            button_width,
            button_height,
            "QUICK BATTLE",
            callback=self._on_quick_battle_click,
            font_size=32,
            bg_color=Color.GREEN
        )
        self.buttons.append(self.quick_battle_btn)

        # Options button (for future use)
        self.options_btn = Button(
            button_x,
            start_y + spacing * 2,
            button_width,
            button_height,
            "OPTIONS",
            callback=self._on_options_click,
            font_size=32,
            bg_color=Color.ORANGE
        )
        self.options_btn.enabled = False  # Not implemented yet
        self.buttons.append(self.options_btn)

        # Exit button
        self.exit_btn = Button(
            button_x,
            start_y + spacing * 3,
            button_width,
            button_height,
            "EXIT",
            callback=self._on_exit_click,
            font_size=32,
            bg_color=Color.RED
        )
        self.buttons.append(self.exit_btn)

    def _on_team_builder_click(self):
        """Handle team builder button click"""
        if self.manager:
            self.manager.set_scene("team_builder")

    def _on_quick_battle_click(self):
        """Handle quick battle button click"""
        # TODO: Generate random teams and start battle
        if self.manager:
            self.manager.set_scene("battle")

    def _on_options_click(self):
        """Handle options button click"""
        # TODO: Implement options menu
        pass

    def _on_exit_click(self):
        """Handle exit button click"""
        import sys
        pygame.quit()
        sys.exit()

    def on_enter(self, **kwargs):
        """Called when scene becomes active"""
        pass

    def on_exit(self):
        """Called when scene becomes inactive"""
        pass

    def update(self, dt: float):
        """Update menu logic"""
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            button.update(mouse_pos)

    def handle_event(self, event: pygame.event.Event):
        """Handle input events"""
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, screen: pygame.Surface):
        """Draw the menu"""
        # Draw gradient background
        self._draw_gradient_background(screen)

        # Draw title
        self.title.draw(screen)

        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

        # Draw version info
        version_label = TextLabel(
            self.width - 10,
            self.height - 10,
            "v0.1.0 - Alpha",
            font_size=20,
            color=Color.LIGHT_GRAY
        )
        version_label.rect.bottomright = (self.width - 10, self.height - 10)
        version_label.draw(screen)

    def _draw_gradient_background(self, screen: pygame.Surface):
        """Draw a gradient background"""
        # Simple two-color gradient from top to bottom
        color_top = (20, 30, 50)
        color_bottom = (60, 80, 120)

        for y in range(self.height):
            ratio = y / self.height
            color = tuple(
                int(color_top[i] + (color_bottom[i] - color_top[i]) * ratio)
                for i in range(3)
            )
            pygame.draw.line(screen, color, (0, y), (self.width, y))