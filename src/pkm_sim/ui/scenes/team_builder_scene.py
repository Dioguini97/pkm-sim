from typing import Optional, Dict, Any, List

import pygame

from pkm_sim.ui.game import Scene
from pkm_sim.ui.ui_components import Panel, Color, TextLabel, Button, Dropdown
from data import Cache

CACHE = Cache()

class Slot:
    def __init__(self, x: int, y: int, width: int, height: int, slot_number: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.slot_number = slot_number
        self.pokemon_data = None # Will store pokemon data from be
        self.is_selected = False
        self.is_active = False # for battle team (slots 1-4)


        # UI elements
        self.panel = Panel(x, y, width, height, bg_color=Color.LIGHT_GRAY)

    def set_pokemon(self, pokemon_data: Optional[Dict[str, Any]]):
        self.pokemon_data = pokemon_data

    def set_active(self, active: bool):
        """Set whether this pokemon is in the active battle team"""
        self.is_active = active

    def draw(self, surface: pygame.Surface):
        """Draw the pokemon slot"""
        # Change color based on state
        if self.is_active:
            self.panel.bg_color = Color.GREEN if self.pokemon_data else Color.LIGHT_GRAY
            self.panel.border_color = Color.DARK_GRAY
        else:
            self.panel.bg_color = Color.LIGHT_GRAY
            self.panel.border_color = Color.GRAY if self.pokemon_data else Color.LIGHT_GRAY

        if self.is_selected:
            self.panel.border_color = Color.BLUE
            self.panel.border_width = 4
        else:
            self.panel.border_width = 2

        self.panel.draw(surface)

        # Draw slot number
        slot_label = TextLabel(
            self.rect.x + 10,
            self.rect.y + 10,
            f"#{self.slot_number}",
            font_size=20,
            color=Color.BLACK,
            bold=True
        )
        slot_label.draw(surface)

        # Draw pokemon info if present
        if self.pokemon_data:
            # Pokemon name
            name_label = TextLabel(
                self.rect.centerx,
                self.rect.y + 40,
                self.pokemon_data.get('name', 'Unknown'),
                font_size=24,
                color=Color.BLACK,
                center=True,
                bold=True
            )
            name_label.draw(surface)

            # Pokemon level
            level_label = TextLabel(
                self.rect.centerx,
                self.rect.y + 70,
                f"Lv. {self.pokemon_data.get('level', 50)}",
                font_size=20,
                color=Color.DARK_GRAY,
                center=True
            )
            level_label.draw(surface)

            # Active indicator
            if self.is_active:
                active_label = TextLabel(
                    self.rect.centerx,
                    self.rect.bottom - 20,
                    "BATTLE TEAM",
                    font_size=16,
                    color=Color.GREEN,
                    center=True,
                    bold=True
                )
                active_label.draw(surface)
        else:
            # Empty slot
            empty_label = TextLabel(
                self.rect.centerx,
                self.rect.centery,
                "Empty Slot",
                font_size=20,
                color=Color.GRAY,
                center=True
            )
            empty_label.draw(surface)

class TeamBuilderScene(Scene):
    """Team builder scene for customizing pokemon teams"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

        self.width = screen.get_width()
        self.height = screen.get_height()

        # Team data
        self.team_slots: List[Slot] = []
        self.selected_slot: Optional[int] = None
        self.battle_team_slots: List[int] = [0, 1, 2, 3]  # First 4 slots are battle team by default

        # Create UI
        self._create_ui()

        # Mock data (replace with backend calls later)
        self._load_mock_data()

    def _create_ui(self):
        """Create all UI elements"""
        # Title
        self.title = TextLabel(
            self.width // 2,
            30,
            "TEAM BUILDER",
            font_size=48,
            color=Color.BLACK,
            center=True,
            bold=True
        )

        # Create 6 pokemon slots (2 rows of 3)
        slot_width = 200
        slot_height = 150
        slots_per_row = 3
        spacing_x = 40
        spacing_y = 40
        start_x = (self.width - (slot_width * slots_per_row + spacing_x * (slots_per_row - 1))) // 2
        start_y = 100

        for i in range(6):
            row = i // slots_per_row
            col = i % slots_per_row

            x = start_x + col * (slot_width + spacing_x)
            y = start_y + row * (slot_height + spacing_y)

            slot = Slot(x, y, slot_width, slot_height, i + 1)
            self.team_slots.append(slot)

        # Battle team order panel
        panel_y = start_y + 2 * (slot_height + spacing_y) + 20
        self.battle_order_panel = Panel(
            50,
            panel_y,
            self.width - 100,
            150,
            bg_color=Color.WHITE
        )

        # Battle order title
        self.battle_order_title = TextLabel(
            self.width // 2,
            panel_y + 20,
            "BATTLE TEAM ORDER (Choose 4 of 6)",
            font_size=28,
            color=Color.BLACK,
            center=True,
            bold=True
        )

        # Buttons for reordering
        button_width = 120
        button_height = 40
        button_y = panel_y + 60

        self.move_up_btn = Button(
            self.width // 2 - button_width - 10,
            button_y,
            button_width,
            button_height,
            "Move Up",
            callback=self._on_move_up,
            font_size=20,
            bg_color=Color.BLUE
        )

        self.move_down_btn = Button(
            self.width // 2 + 10,
            button_y,
            button_width,
            button_height,
            "Move Down",
            callback=self._on_move_down,
            font_size=20,
            bg_color=Color.BLUE
        )

        self.toggle_active_btn = Button(
            self.width // 2 - button_width // 2,
            button_y + button_height + 10,
            button_width,
            button_height,
            "Toggle Active",
            callback=self._on_toggle_active,
            font_size=20,
            bg_color=Color.GREEN
        )

        # Back button
        self.back_btn = Button(
            50,
            self.height - 80,
            150,
            50,
            "Back",
            callback=self._on_back_click,
            font_size=24,
            bg_color=Color.RED
        )

        # Start battle button
        self.start_battle_btn = Button(
            self.width - 200,
            self.height - 80,
            150,
            50,
            "Start Battle",
            callback=self._on_start_battle,
            font_size=24,
            bg_color=Color.GREEN
        )
        options = CACHE.get_all_pokemon_names()
        options.sort()
        self.dropdown = Dropdown(
            x=10, y=10, width=150, height=50,
            options=options
        )

    def _load_mock_data(self):
        """Load mock pokemon data (replace with backend calls)"""
        # TODO: Replace with actual backend calls

        # mock_pokemon = [
        #     {'name': 'Pikachu', 'level': 50, 'type': 'Electric'},
        #     {'name': 'Charizard', 'level': 55, 'type': 'Fire'},
        #     {'name': 'Blastoise', 'level': 52, 'type': 'Water'},
        #     {'name': 'Venusaur', 'level': 53, 'type': 'Grass'},
        #     {'name': 'Gengar', 'level': 51, 'type': 'Ghost'},
        #     {'name': 'Dragonite', 'level': 60, 'type': 'Dragon'},
        # ]
        #
        # for i, pokemon in enumerate(mock_pokemon):
        #     self.team_slots[i].set_pokemon(pokemon)

        # Set first 4 as active battle team
        self._update_active_slots()

    def _update_active_slots(self):
        """Update which slots are marked as active"""
        for i, slot in enumerate(self.team_slots):
            slot.set_active(i in self.battle_team_slots)

    def _on_move_up(self):
        """Move selected pokemon up in order"""
        if self.selected_slot is not None and self.selected_slot > 0:
            # Swap with previous slot
            prev_idx = self.selected_slot - 1
            current = self.team_slots[self.selected_slot]
            previous = self.team_slots[prev_idx]

            # Swap pokemon data
            current.pokemon_data, previous.pokemon_data = previous.pokemon_data, current.pokemon_data

            # Update selection
            self.selected_slot = prev_idx

    def _on_move_down(self):
        """Move selected pokemon down in order"""
        if self.selected_slot is not None and self.selected_slot < 5:
            # Swap with next slot
            next_idx = self.selected_slot + 1
            current = self.team_slots[self.selected_slot]
            next_slot = self.team_slots[next_idx]

            # Swap pokemon data
            current.pokemon_data, next_slot.pokemon_data = next_slot.pokemon_data, current.pokemon_data

            # Update selection
            self.selected_slot = next_idx

    def _on_toggle_active(self):
        """Toggle whether selected pokemon is in battle team"""
        if self.selected_slot is not None:
            if self.selected_slot in self.battle_team_slots:
                if len(self.battle_team_slots) > 1:  # Must have at least 1 active
                    self.battle_team_slots.remove(self.selected_slot)
            else:
                if len(self.battle_team_slots) < 4:  # Max 4 active
                    self.battle_team_slots.append(self.selected_slot)

            self._update_active_slots()

    def _on_back_click(self):
        """Return to main menu"""
        if self.manager:
            self.manager.set_scene("menu")

    def _on_start_battle(self):
        """Start battle with current team"""
        # TODO: Pass team data to battle scene
        if self.manager:
            # Prepare battle team data
            battle_team = [
                self.team_slots[i].pokemon_data
                for i in self.battle_team_slots
                if self.team_slots[i].pokemon_data is not None
            ]

            if len(battle_team) >= 1:  # Need at least 1 pokemon
                self.manager.set_scene("battle", team=battle_team)

    def on_enter(self, **kwargs):
        """Called when scene becomes active"""
        pass

    def on_exit(self):
        """Called when scene becomes inactive"""
        pass

    def update(self, dt: float):
        """Update team builder logic"""
        mouse_pos = pygame.mouse.get_pos()

        # Update buttons
        self.move_up_btn.update(mouse_pos)
        self.move_down_btn.update(mouse_pos)
        self.toggle_active_btn.update(mouse_pos)
        self.back_btn.update(mouse_pos)
        self.start_battle_btn.update(mouse_pos)

        # Enable/disable reorder buttons based on selection
        self.move_up_btn.enabled = self.selected_slot is not None and self.selected_slot > 0
        self.move_down_btn.enabled = self.selected_slot is not None and self.selected_slot < 5
        self.toggle_active_btn.enabled = self.selected_slot is not None

    def handle_event(self, event: pygame.event.Event):
        """Handle input events"""
        # Handle button clicks
        self.move_up_btn.handle_event(event)
        self.move_down_btn.handle_event(event)
        self.toggle_active_btn.handle_event(event)
        self.back_btn.handle_event(event)
        self.start_battle_btn.handle_event(event)
        self.dropdown.handle_event(event)

        # Handle slot selection
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            for i, slot in enumerate(self.team_slots):
                if slot.rect.collidepoint(mouse_pos):
                    # Toggle selection
                    if self.selected_slot == i:
                        self.selected_slot = None
                        slot.is_selected = False
                    else:
                        # Deselect previous
                        if self.selected_slot is not None:
                            self.team_slots[self.selected_slot].is_selected = False
                        # Select new
                        self.selected_slot = i
                        slot.is_selected = True
                    break

    def draw(self, screen: pygame.Surface):
        """Draw the team builder"""
        # Background
        screen.fill(Color.WHITE)

        # Title
        self.title.draw(screen)

        # Pokemon slots
        for slot in self.team_slots:
            slot.draw(screen)

        # Battle order panel
        self.battle_order_panel.draw(screen)
        self.battle_order_title.draw(screen)

        # Buttons
        self.move_up_btn.draw(screen)
        self.move_down_btn.draw(screen)
        self.toggle_active_btn.draw(screen)
        self.back_btn.draw(screen)
        self.start_battle_btn.draw(screen)

        self.dropdown.draw(screen)

        # Instructions
        if self.selected_slot is None:
            instruction = TextLabel(
                self.width // 2,
                self.height - 30,
                "Click on a Pokémon to select it",
                font_size=20,
                color=Color.GRAY,
                center=True
            )
            instruction.draw(screen)
