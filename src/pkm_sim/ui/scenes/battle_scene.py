"""
Battle scene where the actual pokemon battle takes place.
"""
import pygame
from typing import List, Optional, Dict, Any

from pkm_sim.ui.game import Scene
from pkm_sim.ui.ui_components import *


class BattleScene(Scene):
    """Battle scene for pokemon battles"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

        self.width = screen.get_width()
        self.height = screen.get_height()

        # Battle state
        self.player_team: List[Dict[str, Any]] = []
        self.opponent_team: List[Dict[str, Any]] = []
        self.player_active_pokemon: Optional[Dict[str, Any]] = None
        self.opponent_active_pokemon: Optional[Dict[str, Any]] = None

        # Battle log
        self.battle_log: List[str] = []
        self.max_log_entries = 5

        # UI state
        self.action_menu_visible = True
        self.move_menu_visible = False
        self.pokemon_menu_visible = False

        # Create UI
        self._create_ui()

    def _create_ui(self):
        """Create all UI elements"""
        # Battle field panels
        self._create_battle_field()

        # Action menu (Fight, Pokemon, Run)
        self._create_action_menu()

        # Move selection menu
        self._create_move_menu()

        # Pokemon switch menu
        self._create_pokemon_menu()

        # Battle log panel
        self._create_battle_log()

    def _create_battle_field(self):
        """Create the battle field display"""
        # Opponent pokemon display (top)
        self.opponent_panel = Panel(
            50,
            50,
            400,
            200,
            bg_color=(240, 240, 255)
        )

        # Player pokemon display (bottom right)
        self.player_panel = Panel(
            self.width - 450,
            self.height - 350,
            400,
            200,
            bg_color=(255, 240, 240)
        )

    def _create_action_menu(self):
        """Create the main action menu"""
        menu_width = 600
        menu_height = 200
        menu_x = (self.width - menu_width) // 2
        menu_y = self.height - menu_height - 20

        self.action_menu_panel = Panel(
            menu_x,
            menu_y,
            menu_width,
            menu_height,
            bg_color=Color.WHITE
        )

        # Action buttons
        button_width = 180
        button_height = 70
        spacing = 20

        # Fight button
        self.fight_btn = Button(
            menu_x + spacing,
            menu_y + spacing,
            button_width,
            button_height,
            "FIGHT",
            callback=self._on_fight_click,
            font_size=28,
            bg_color=Color.RED
        )

        # Pokemon button
        self.pokemon_btn = Button(
            menu_x + spacing,
            menu_y + spacing + button_height + 10,
            button_width,
            button_height,
            "POKÉMON",
            callback=self._on_pokemon_click,
            font_size=28,
            bg_color=Color.GREEN
        )

        # Bag button (disabled for now)
        self.bag_btn = Button(
            menu_x + spacing + button_width + spacing,
            menu_y + spacing,
            button_width,
            button_height,
            "BAG",
            callback=self._on_bag_click,
            font_size=28,
            bg_color=Color.BLUE
        )
        self.bag_btn.enabled = False

        # Run button
        self.run_btn = Button(
            menu_x + spacing + button_width + spacing,
            menu_y + spacing + button_height + 10,
            button_width,
            button_height,
            "RUN",
            callback=self._on_run_click,
            font_size=28,
            bg_color=Color.ORANGE
        )

        self.action_buttons = [self.fight_btn, self.pokemon_btn, self.bag_btn, self.run_btn]

    def _create_move_menu(self):
        """Create the move selection menu"""
        menu_width = 600
        menu_height = 200
        menu_x = (self.width - menu_width) // 2
        menu_y = self.height - menu_height - 20

        self.move_menu_panel = Panel(
            menu_x,
            menu_y,
            menu_width,
            menu_height,
            bg_color=Color.WHITE
        )

        # Move buttons (4 moves)
        button_width = 280
        button_height = 70
        spacing = 20

        self.move_buttons = []
        for i in range(4):
            row = i // 2
            col = i % 2

            btn = Button(
                menu_x + spacing + col * (button_width + spacing),
                menu_y + spacing + row * (button_height + 10),
                button_width,
                button_height,
                f"Move {i + 1}",
                callback=lambda idx=i: self._on_move_click(idx),
                font_size=24,
                bg_color=Color.BLUE
            )
            self.move_buttons.append(btn)

        # Back button
        self.move_back_btn = Button(
            menu_x + menu_width - 100,
            menu_y + menu_height - 50,
            80,
            40,
            "Back",
            callback=self._on_move_back_click,
            font_size=20,
            bg_color=Color.RED
        )

    def _create_pokemon_menu(self):
        """Create the pokemon switch menu"""
        menu_width = 600
        menu_height = 400
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2

        self.pokemon_menu_panel = Panel(
            menu_x,
            menu_y,
            menu_width,
            menu_height,
            bg_color=Color.WHITE
        )

        # Pokemon slot buttons (max 6)
        self.pokemon_slot_buttons = []
        button_width = 260
        button_height = 60
        spacing = 20

        for i in range(6):
            row = i // 2
            col = i % 2

            btn = Button(
                menu_x + spacing + col * (button_width + spacing),
                menu_y + 50 + row * (button_height + 10),
                button_width,
                button_height,
                f"Pokémon {i + 1}",
                callback=lambda idx=i: self._on_switch_pokemon(idx),
                font_size=20,
                bg_color=Color.GREEN
            )
            self.pokemon_slot_buttons.append(btn)

        # Title
        self.pokemon_menu_title = TextLabel(
            menu_x + menu_width // 2,
            menu_y + 20,
            "Choose a Pokémon",
            font_size=28,
            color=Color.BLACK,
            center=True,
            bold=True
        )

        # Close button
        self.pokemon_close_btn = Button(
            menu_x + menu_width - 100,
            menu_y + menu_height - 50,
            80,
            40,
            "Close",
            callback=self._on_pokemon_close_click,
            font_size=20,
            bg_color=Color.RED
        )

    def _create_battle_log(self):
        """Create the battle log panel"""
        self.battle_log_panel = Panel(
            50,
            self.height - 350,
            self.width - 500,
            150,
            bg_color=(250, 250, 250)
        )

    # Callback methods
    def _on_fight_click(self):
        """Show move selection menu"""
        self.action_menu_visible = False
        self.move_menu_visible = True

    def _on_pokemon_click(self):
        """Show pokemon switch menu"""
        self.pokemon_menu_visible = True

    def _on_bag_click(self):
        """Open bag menu (not implemented)"""
        self.add_log_entry("Bag is not available yet!")

    def _on_run_click(self):
        """Attempt to run from battle"""
        self.add_log_entry("Can't run from a trainer battle!")
        # TODO: Implement run logic

    def _on_move_click(self, move_index: int):
        """Execute selected move"""
        if self.player_active_pokemon:
            moves = self.player_active_pokemon.get('moves', [])
            if move_index < len(moves):
                move = moves[move_index]
                self.add_log_entry(f"{self.player_active_pokemon['name']} used {move['name']}!")

                # TODO: Call backend to execute move
                # self.battle_engine.execute_move(move)

                # Return to action menu
                self.move_menu_visible = False
                self.action_menu_visible = True

    def _on_move_back_click(self):
        """Return to action menu from move menu"""
        self.move_menu_visible = False
        self.action_menu_visible = True

    def _on_switch_pokemon(self, pokemon_index: int):
        """Switch to selected pokemon"""
        if pokemon_index < len(self.player_team):
            new_pokemon = self.player_team[pokemon_index]
            if new_pokemon != self.player_active_pokemon:
                self.player_active_pokemon = new_pokemon
                self.add_log_entry(f"Go, {new_pokemon['name']}!")

                # TODO: Call backend to switch pokemon

                self.pokemon_menu_visible = False

    def _on_pokemon_close_click(self):
        """Close pokemon menu"""
        self.pokemon_menu_visible = False

    def add_log_entry(self, message: str):
        """Add a message to the battle log"""
        self.battle_log.append(message)
        if len(self.battle_log) > self.max_log_entries:
            self.battle_log.pop(0)

    def _draw_pokemon_display(
            self,
            surface: pygame.Surface,
            panel: Panel,
            pokemon: Optional[Dict[str, Any]],
            is_player: bool
    ):
        """Draw a pokemon's display panel"""
        panel.draw(surface)

        if not pokemon:
            return

        # Pokemon name
        name_y = panel.rect.y + 15
        name_label = TextLabel(
            panel.rect.x + 15,
            name_y,
            pokemon.get('name', 'Unknown'),
            font_size=28,
            color=Color.BLACK,
            bold=True
        )
        name_label.draw(surface)

        # Level
        level_label = TextLabel(
            panel.rect.right - 15,
            name_y,
            f"Lv.{pokemon.get('level', 50)}",
            font_size=24,
            color=Color.DARK_GRAY
        )
        level_label.rect.topright = (panel.rect.right - 15, name_y)
        level_label.draw(surface)

        # HP bar
        hp_bar_y = panel.rect.y + 60
        hp_bar_width = panel.rect.width - 30

        hp_label = TextLabel(
            panel.rect.x + 15,
            hp_bar_y,
            "HP",
            font_size=20,
            color=Color.BLACK,
            bold=True
        )
        hp_label.draw(surface)

        current_hp = pokemon.get('current_hp', 100)
        max_hp = pokemon.get('max_hp', 100)

        hp_bar = ProgressBar(
            panel.rect.x + 50,
            hp_bar_y,
            hp_bar_width - 40,
            25,
            max_hp,
            current_hp,
            show_text=is_player
        )
        hp_bar.draw(surface)

        # Status condition if any
        status = pokemon.get('status')
        if status:
            status_colors = {
                'BRN': Color.ORANGE,
                'PSN': Color.PURPLE,
                'PAR': Color.YELLOW,
                'SLP': Color.GRAY,
                'FRZ': Color.ICE
            }
            status_color = status_colors.get(status, Color.RED)

            status_label = TextLabel(
                panel.rect.x + 15,
                hp_bar_y + 35,
                status,
                font_size=18,
                color=Color.WHITE
            )

            # Draw status background
            status_bg = pygame.Rect(
                status_label.rect.x - 5,
                status_label.rect.y - 2,
                status_label.rect.width + 10,
                status_label.rect.height + 4
            )
            pygame.draw.rect(surface, status_color, status_bg, border_radius=3)
            status_label.draw(surface)

        # Pokemon sprite placeholder
        sprite_size = 120
        sprite_x = panel.rect.centerx - sprite_size // 2
        sprite_y = panel.rect.y + 100 if not is_player else panel.rect.y + 90

        # Draw a placeholder circle for now (replace with actual sprite)
        pygame.draw.circle(
            surface,
            Color.LIGHT_GRAY,
            (sprite_x + sprite_size // 2, sprite_y + sprite_size // 2),
            sprite_size // 2
        )

        # Draw pokemon initial as placeholder
        initial = pokemon.get('name', 'P')[0]
        initial_label = TextLabel(
            sprite_x + sprite_size // 2,
            sprite_y + sprite_size // 2,
            initial,
            font_size=60,
            color=Color.DARK_GRAY,
            center=True,
            bold=True
        )
        initial_label.draw(surface)

    def on_enter(self, **kwargs):
        """Called when scene becomes active"""
        # Get team data passed from team builder
        self.player_team = kwargs.get('team', [])

        # Set active pokemon
        if self.player_team:
            self.player_active_pokemon = self.player_team[0]

            # Add moves to pokemon (mock data for now)
            for pokemon in self.player_team:
                if 'moves' not in pokemon:
                    pokemon['moves'] = [
                        {'name': 'Tackle', 'type': 'Normal', 'power': 40},
                        {'name': 'Quick Attack', 'type': 'Normal', 'power': 40},
                        {'name': 'Thunder Shock', 'type': 'Electric', 'power': 40},
                        {'name': 'Iron Tail', 'type': 'Steel', 'power': 100},
                    ]
                if 'current_hp' not in pokemon:
                    pokemon['current_hp'] = 100
                if 'max_hp' not in pokemon:
                    pokemon['max_hp'] = 100

        # Generate opponent team (mock)
        self.opponent_team = [
            {
                'name': 'Mewtwo',
                'level': 70,
                'current_hp': 150,
                'max_hp': 150,
                'moves': [
                    {'name': 'Psychic', 'type': 'Psychic', 'power': 90},
                ]
            }
        ]
        self.opponent_active_pokemon = self.opponent_team[0]

        # Update move buttons with actual moves
        if self.player_active_pokemon:
            moves = self.player_active_pokemon.get('moves', [])
            for i, btn in enumerate(self.move_buttons):
                if i < len(moves):
                    btn.text = moves[i]['name']
                    btn.text_surface = btn.font.render(btn.text, True, btn.text_color)
                    btn.text_rect = btn.text_surface.get_rect(center=btn.rect.center)
                    btn.enabled = True
                else:
                    btn.enabled = False

        # Update pokemon slot buttons
        for i, btn in enumerate(self.pokemon_slot_buttons):
            if i < len(self.player_team):
                pokemon = self.player_team[i]
                btn.text = f"{pokemon['name']} - Lv.{pokemon['level']}"
                btn.text_surface = btn.font.render(btn.text, True, btn.text_color)
                btn.text_rect = btn.text_surface.get_rect(center=btn.rect.center)
                btn.enabled = pokemon != self.player_active_pokemon
            else:
                btn.enabled = False

        self.add_log_entry(f"A wild {self.opponent_active_pokemon['name']} appeared!")
        self.add_log_entry(f"Go, {self.player_active_pokemon['name']}!")

    def on_exit(self):
        """Called when scene becomes inactive"""
        pass

    def update(self, dt: float):
        """Update battle logic"""
        mouse_pos = pygame.mouse.get_pos()

        # Update action menu buttons
        if self.action_menu_visible:
            for btn in self.action_buttons:
                btn.update(mouse_pos)

        # Update move menu buttons
        if self.move_menu_visible:
            for btn in self.move_buttons:
                btn.update(mouse_pos)
            self.move_back_btn.update(mouse_pos)

        # Update pokemon menu buttons
        if self.pokemon_menu_visible:
            for btn in self.pokemon_slot_buttons:
                btn.update(mouse_pos)
            self.pokemon_close_btn.update(mouse_pos)

    def handle_event(self, event: pygame.event.Event):
        """Handle input events"""
        # Action menu
        if self.action_menu_visible:
            for btn in self.action_buttons:
                btn.handle_event(event)

        # Move menu
        if self.move_menu_visible:
            for btn in self.move_buttons:
                btn.handle_event(event)
            self.move_back_btn.handle_event(event)

        # Pokemon menu
        if self.pokemon_menu_visible:
            for btn in self.pokemon_slot_buttons:
                btn.handle_event(event)
            self.pokemon_close_btn.handle_event(event)

    def draw(self, screen: pygame.Surface):
        """Draw the battle scene"""
        # Background (simple gradient)
        screen.fill((135, 206, 235))  # Sky blue

        # Draw ground
        ground_rect = pygame.Rect(0, self.height // 2, self.width, self.height // 2)
        pygame.draw.rect(screen, (34, 139, 34), ground_rect)  # Green ground

        # Draw pokemon displays
        self._draw_pokemon_display(screen, self.opponent_panel, self.opponent_active_pokemon, False)
        self._draw_pokemon_display(screen, self.player_panel, self.player_active_pokemon, True)

        # Draw battle log
        self.battle_log_panel.draw(screen)
        log_y = self.battle_log_panel.rect.y + 15
        for i, entry in enumerate(self.battle_log):
            log_label = TextLabel(
                self.battle_log_panel.rect.x + 15,
                log_y + i * 25,
                entry,
                font_size=20,
                color=Color.BLACK
            )
            log_label.draw(screen)

        # Draw active menu
        if self.action_menu_visible:
            self.action_menu_panel.draw(screen)
            for btn in self.action_buttons:
                btn.draw(screen)

        if self.move_menu_visible:
            self.move_menu_panel.draw(screen)
            for btn in self.move_buttons:
                btn.draw(screen)
            self.move_back_btn.draw(screen)

        if self.pokemon_menu_visible:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill(Color.BLACK)
            screen.blit(overlay, (0, 0))

            self.pokemon_menu_panel.draw(screen)
            self.pokemon_menu_title.draw(screen)
            for btn in self.pokemon_slot_buttons:
                btn.draw(screen)
            self.pokemon_close_btn.draw(screen)