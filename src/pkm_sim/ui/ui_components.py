"""
Reusable UI components for the game.
"""
import pygame
from typing import Callable, Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class Color:
    """Common colors used in the UI"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (64, 64, 64)
    RED = (220, 53, 69)
    GREEN = (40, 167, 69)
    BLUE = (0, 123, 255)
    YELLOW = (255, 193, 7)
    ORANGE = (253, 126, 20)
    PURPLE = (111, 66, 193)

    # Pokemon type colors
    NORMAL = (168, 167, 122)
    FIRE = (238, 129, 48)
    WATER = (99, 144, 240)
    ELECTRIC = (247, 208, 44)
    GRASS = (122, 199, 76)
    ICE = (150, 217, 214)
    FIGHTING = (194, 46, 40)
    POISON = (163, 62, 161)
    GROUND = (226, 191, 101)
    FLYING = (169, 143, 243)
    PSYCHIC = (249, 85, 135)
    BUG = (166, 185, 26)
    ROCK = (182, 161, 54)
    GHOST = (115, 87, 151)
    DRAGON = (111, 53, 252)
    DARK = (112, 87, 70)
    STEEL = (183, 183, 206)
    FAIRY = (214, 133, 173)


class Button:
    """A clickable button component"""

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            text: str,
            callback: Optional[Callable] = None,
            font_size: int = 24,
            bg_color: Tuple[int, int, int] = Color.BLUE,
            text_color: Tuple[int, int, int] = Color.WHITE,
            hover_color: Optional[Tuple[int, int, int]] = None,
            border_radius: int = 5
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color or self._darken_color(bg_color)
        self.border_radius = border_radius
        self.is_hovered = False
        self.is_pressed = False
        self.enabled = True

        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def _darken_color(self, color: Tuple[int, int, int], factor: float = 0.8) -> Tuple[int, int, int]:
        """Darken a color by a factor"""
        return tuple(int(c * factor) for c in color)

    def update(self, mouse_pos: Tuple[int, int]):
        """Update button state"""
        self.is_hovered = self.rect.collidepoint(mouse_pos) and self.enabled

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events. Returns True if button was clicked."""
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_pressed = True
                return False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.is_hovered:
                self.is_pressed = False
                if self.callback:
                    self.callback()
                return True
            self.is_pressed = False

        return False

    def draw(self, surface: pygame.Surface):
        """Draw the button"""
        # Choose color based on state
        if not self.enabled:
            color = Color.GRAY
        elif self.is_pressed:
            color = self._darken_color(self.bg_color, 0.7)
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.bg_color

        # Draw button background
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)

        # Draw border
        border_color = Color.WHITE if self.is_hovered else Color.DARK_GRAY
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=self.border_radius)

        # Draw text
        surface.blit(self.text_surface, self.text_rect)


class Panel:
    """A rectangular panel for grouping UI elements"""

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            bg_color: Tuple[int, int, int] = Color.LIGHT_GRAY,
            border_color: Optional[Tuple[int, int, int]] = Color.DARK_GRAY,
            border_width: int = 2,
            border_radius: int = 10,
            padding: int = 10
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.padding = padding

    def draw(self, surface: pygame.Surface):
        """Draw the panel"""
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.border_radius)

        # Draw border
        if self.border_color:
            pygame.draw.rect(
                surface,
                self.border_color,
                self.rect,
                width=self.border_width,
                border_radius=self.border_radius
            )


class TextLabel:
    """A text label component"""

    def __init__(
            self,
            x: int,
            y: int,
            text: str,
            font_size: int = 24,
            color: Tuple[int, int, int] = Color.BLACK,
            center: bool = False,
            bold: bool = False
    ):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.center = center

        self.font = pygame.font.Font(None, font_size)
        if bold:
            self.font.set_bold(True)

        self._update_surface()

    def _update_surface(self):
        """Update the text surface"""
        self.surface = self.font.render(self.text, True, self.color)
        if self.center:
            self.rect = self.surface.get_rect(center=(self.x, self.y))
        else:
            self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def set_text(self, text: str):
        """Update the text"""
        self.text = text
        self._update_surface()

    def draw(self, surface: pygame.Surface):
        """Draw the label"""
        surface.blit(self.surface, self.rect)


class ProgressBar:
    """A progress bar component (e.g., for HP)"""

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            max_value: float,
            current_value: float,
            fg_color: Tuple[int, int, int] = Color.GREEN,
            bg_color: Tuple[int, int, int] = Color.DARK_GRAY,
            border_color: Tuple[int, int, int] = Color.BLACK,
            show_text: bool = True
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.current_value = current_value
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.show_text = show_text
        self.font = pygame.font.Font(None, 20)

    def update(self, current_value: float):
        """Update the current value"""
        self.current_value = max(0, min(current_value, self.max_value))

    def get_color(self) -> Tuple[int, int, int]:
        """Get color based on percentage"""
        percentage = self.current_value / self.max_value if self.max_value > 0 else 0

        if percentage > 0.5:
            return Color.GREEN
        elif percentage > 0.25:
            return Color.YELLOW
        else:
            return Color.RED

    def draw(self, surface: pygame.Surface):
        """Draw the progress bar"""
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)

        # Draw foreground (progress)
        percentage = self.current_value / self.max_value if self.max_value > 0 else 0
        fill_width = int(self.rect.width * percentage)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, self.get_color(), fill_rect)

        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, width=2)

        # Draw text
        if self.show_text:
            text = f"{int(self.current_value)}/{int(self.max_value)}"
            text_surface = self.font.render(text, True, Color.WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)

            # Draw text shadow for better visibility
            shadow_rect = text_rect.copy()
            shadow_rect.x += 1
            shadow_rect.y += 1
            shadow_surface = self.font.render(text, True, Color.BLACK)
            surface.blit(shadow_surface, shadow_rect)
            surface.blit(text_surface, text_rect)


class Dropdown:
    """A dropdown selection menu"""

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            options: List[str],
            selected_index: int = 0,
            font_size: int = 20
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_index = selected_index
        self.is_open = False
        self.font = pygame.font.Font(None, font_size)

        # Calculate dropdown menu rect
        self.dropdown_rect = pygame.Rect(
            x, y + height, width, height * len(options)
        )

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events. Returns True if selection changed."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            if self.rect.collidepoint(mouse_pos):
                self.is_open = not self.is_open
                return False

            if self.is_open and self.dropdown_rect.collidepoint(mouse_pos):
                # Calculate which option was clicked
                relative_y = mouse_pos[1] - self.dropdown_rect.y
                clicked_index = int(relative_y / self.rect.height)

                if 0 <= clicked_index < len(self.options):
                    old_index = self.selected_index
                    self.selected_index = clicked_index
                    self.is_open = False
                    return old_index != self.selected_index

            # Close dropdown if clicked outside
            if self.is_open:
                self.is_open = False

        return False

    def draw(self, surface: pygame.Surface):
        """Draw the dropdown"""
        # Draw main button
        pygame.draw.rect(surface, Color.DARK_GRAY, self.rect)
        pygame.draw.rect(surface, Color.BLACK, self.rect, width=2)

        # Draw selected text
        text = self.options[self.selected_index]
        text_surface = self.font.render(text, True, Color.BLACK)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(text_surface, text_rect)

        # Draw arrow
        arrow = "▼" if not self.is_open else "▲"
        arrow_surface = self.font.render(arrow, True, Color.BLACK)
        arrow_rect = arrow_surface.get_rect(midright=(self.rect.right - 10, self.rect.centery))
        surface.blit(arrow_surface, arrow_rect)

        # Draw dropdown menu if open
        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.dropdown_rect.x,
                    self.dropdown_rect.y + i * self.rect.height,
                    self.dropdown_rect.width,
                    self.rect.height
                )

                # Highlight selected option
                if i == self.selected_index:
                    pygame.draw.rect(surface, Color.LIGHT_GRAY, option_rect)
                else:
                    pygame.draw.rect(surface, Color.WHITE, option_rect)

                pygame.draw.rect(surface, Color.BLACK, option_rect, width=1)

                # Draw option text
                text_surface = self.font.render(option, True, Color.BLACK)
                text_rect = text_surface.get_rect(midleft=(option_rect.x + 10, option_rect.centery))
                surface.blit(text_surface, text_rect)