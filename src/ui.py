"""
Modern UI for Rock-Paper-Scissors game with theme toggle and multiplayer
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Callable, Optional
import threading
import socket
import json
from game_logic import GameLogic
from utils import get_local_ip, create_message, parse_message


class Theme:
    """Theme configuration for light and dark modes"""
    
    LIGHT = {
        "bg": "#FFFFFF",
        "secondary_bg": "#F7F7F7",
        "text": "#333333",
        "text_secondary": "#666666",
        "primary": "#1A73E8",
        "primary_hover": "#1557B0",
        "success": "#34A853",
        "success_hover": "#2D8E47",
        "warning": "#FBBC04",
        "warning_hover": "#D9A004",
        "danger": "#EA4335",
        "danger_hover": "#C5362C",
        "gray": "#666666",
        "gray_hover": "#555555"
    }
    
    DARK = {
        "bg": "#1E1E1E",
        "secondary_bg": "#2D2D2D",
        "text": "#E0E0E0",
        "text_secondary": "#B0B0B0",
        "primary": "#4A9EFF",
        "primary_hover": "#357ABD",
        "success": "#5CB85C",
        "success_hover": "#449D44",
        "warning": "#F0AD4E",
        "warning_hover": "#EC971F",
        "danger": "#D9534F",
        "danger_hover": "#C9302C",
        "gray": "#888888",
        "gray_hover": "#999999"
    }


class ModernButton(tk.Canvas):
    """Custom modern button with hover effects"""
    
    def __init__(self, parent, text, command, width=200, height=50, 
                 bg_color="#1A73E8", hover_color="#1557B0", text_color="white"):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bg=parent.cget('bg'))
        
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.width = width
        self.height = height
        
        # Create rounded rectangle
        self.rect = self.create_rounded_rect(0, 0, width, height, 10, fill=bg_color)
        self.text_item = self.create_text(width/2, height/2, text=text, 
                                     fill=text_color, font=("Helvetica", 12, "bold"))
        
        # Bind events
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle"""
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _on_click(self, event):
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
    
    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)
    
    def update_colors(self, bg_color, hover_color):
        """Update button colors for theme changes"""
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.itemconfig(self.rect, fill=bg_color)


class GameUI:
    """Main UI for the Rock-Paper-Scissors game"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors Game")
        self.root.geometry("550x700")
        self.root.resizable(False, False)
        
        self.game_logic = GameLogic()
        self.current_screen = None
        self.is_dark_mode = False
        self.theme = Theme.LIGHT
        
        # Multiplayer variables
        self.server_socket = None
        self.client_socket = None
        self.connection = None
        self.multiplayer_thread = None
        self.is_hosting = False
        self.opponent_move = None
        self.waiting_for_opponent = False
        self.multiplayer_running = False
        self.player_score = 0
        self.opponent_score = 0
        
        # Show main menu
        self.show_main_menu()
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.is_dark_mode = not self.is_dark_mode
        self.theme = Theme.DARK if self.is_dark_mode else Theme.LIGHT
        self.root.configure(bg=self.theme["bg"])
        
        # Refresh current screen
        if self.current_screen == "main_menu":
            self.show_main_menu()
        elif self.current_screen == "single_player":
            self.show_single_player()
        elif self.current_screen == "wifi_menu":
            self.show_wifi_menu()
        elif self.current_screen == "wifi_host":
            self.show_wifi_host()
        elif self.current_screen == "wifi_join_input":
            self.show_wifi_join_input()
        elif self.current_screen == "bluetooth_menu":
            self.show_bluetooth_menu()
    
    def clear_screen(self):
        """Clear all widgets from the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_theme_toggle(self, parent):
        """Create a theme toggle button"""
        toggle_frame = tk.Frame(parent, bg=self.theme["bg"])
        toggle_frame.pack(anchor="ne", padx=20, pady=10)
        
        icon = "🌙" if not self.is_dark_mode else "☀️"
        toggle_btn = tk.Button(toggle_frame, text=icon, 
                              command=self.toggle_theme,
                              font=("Helvetica", 16),
                              bg=self.theme["secondary_bg"],
                              fg=self.theme["text"],
                              relief=tk.FLAT,
                              cursor="hand2",
                              padx=10, pady=5)
        toggle_btn.pack()
    
    def show_main_menu(self):
        """Display the main menu"""
        self.clear_screen()
        self.current_screen = "main_menu"
        self.root.configure(bg=self.theme["bg"])
        
        # Theme toggle
        self.create_theme_toggle(self.root)
        
        # Title
        title_frame = tk.Frame(self.root, bg=self.theme["bg"])
        title_frame.pack(pady=20)
        
        title = tk.Label(title_frame, text="Rock Paper Scissors", 
                        font=("Helvetica", 28, "bold"), 
                        fg=self.theme["primary"], bg=self.theme["bg"])
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Choose Your Game Mode", 
                           font=("Helvetica", 12), 
                           fg=self.theme["text_secondary"], bg=self.theme["bg"])
        subtitle.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.theme["bg"])
        buttons_frame.pack(pady=20)
        
        # Single Player button
        single_btn = ModernButton(buttons_frame, "🎮 Single Player vs AI", 
                                  self.show_single_player, width=280, height=60,
                                  bg_color=self.theme["primary"],
                                  hover_color=self.theme["primary_hover"])
        single_btn.pack(pady=10)
        
        # Multiplayer Wi-Fi button
        wifi_btn = ModernButton(buttons_frame, "📡 Multiplayer (Wi-Fi)", 
                               self.show_wifi_menu, width=280, height=60,
                               bg_color=self.theme["success"],
                               hover_color=self.theme["success_hover"])
        wifi_btn.pack(pady=10)
        
        # Multiplayer Bluetooth button
        bt_btn = ModernButton(buttons_frame, "📱 Multiplayer (Bluetooth)", 
                             self.show_bluetooth_menu, width=280, height=60,
                             bg_color=self.theme["warning"],
                             hover_color=self.theme["warning_hover"])
        bt_btn.pack(pady=10)
        
        # Exit button
        exit_btn = ModernButton(buttons_frame, "❌ Exit", 
                               self.root.quit, width=280, height=60,
                               bg_color=self.theme["danger"],
                               hover_color=self.theme["danger_hover"])
        exit_btn.pack(pady=10)
    
    def show_single_player(self):
        """Display the single player game screen"""
        self.clear_screen()
        self.current_screen = "single_player"
        self.game_logic.reset_scores()
        self.root.configure(bg=self.theme["bg"])
        
        # Theme toggle
        self.create_theme_toggle(self.root)
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.theme["secondary_bg"], height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="Single Player Mode", 
                        font=("Helvetica", 20, "bold"), 
                        fg=self.theme["primary"], bg=self.theme["secondary_bg"])
        title.pack(pady=20)
        
        # Score frame
        score_frame = tk.Frame(self.root, bg=self.theme["bg"])
        score_frame.pack(pady=20)
        
        self.score_label = tk.Label(score_frame, text="Score: 0 - 0", 
                                    font=("Helvetica", 16, "bold"), 
                                    fg=self.theme["text"], bg=self.theme["bg"])
        self.score_label.pack()
        
        self.rounds_label = tk.Label(score_frame, text="Rounds Played: 0", 
                                     font=("Helvetica", 12), 
                                     fg=self.theme["text_secondary"], bg=self.theme["bg"])
        self.rounds_label.pack(pady=5)
        
        # Result display
        self.result_label = tk.Label(self.root, text="Choose your move!", 
                                     font=("Helvetica", 14), 
                                     fg=self.theme["text_secondary"], bg=self.theme["bg"],
                                     wraplength=450)
        self.result_label.pack(pady=20)
        
        # Move buttons
        moves_frame = tk.Frame(self.root, bg=self.theme["bg"])
        moves_frame.pack(pady=20)
        
        rock_btn = ModernButton(moves_frame, "🪨 Rock", 
                               lambda: self.play_move("Rock"),
                               width=140, height=100,
                               bg_color=self.theme["danger"], 
                               hover_color=self.theme["danger_hover"])
        rock_btn.grid(row=0, column=0, padx=10)
        
        paper_btn = ModernButton(moves_frame, "📄 Paper", 
                                lambda: self.play_move("Paper"),
                                width=140, height=100,
                                bg_color=self.theme["primary"], 
                                hover_color=self.theme["primary_hover"])
        paper_btn.grid(row=0, column=1, padx=10)
        
        scissors_btn = ModernButton(moves_frame, "✂️ Scissors", 
                                   lambda: self.play_move("Scissors"),
                                   width=140, height=100,
                                   bg_color=self.theme["success"], 
                                   hover_color=self.theme["success_hover"])
        scissors_btn.grid(row=0, column=2, padx=10)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg=self.theme["bg"])
        control_frame.pack(pady=30)
        
        reset_btn = ModernButton(control_frame, "Reset Scores", 
                                self.reset_game,
                                width=150, height=40,
                                bg_color=self.theme["warning"], 
                                hover_color=self.theme["warning_hover"])
        reset_btn.grid(row=0, column=0, padx=10)
        
        back_btn = ModernButton(control_frame, "Back to Menu", 
                               self.show_main_menu,
                               width=150, height=40,
                               bg_color=self.theme["gray"], 
                               hover_color=self.theme["gray_hover"])
        back_btn.grid(row=0, column=1, padx=10)
    
    def play_move(self, player_move):
        """Handle a player's move in single player mode"""
        computer_move, result, message = self.game_logic.play_round(player_move)
        
        # Update result label with color
        if result == "player1":
            self.result_label.config(text=message, fg=self.theme["success"])
        elif result == "player2":
            self.result_label.config(text=message, fg=self.theme["danger"])
        else:
            self.result_label.config(text=message, fg=self.theme["warning"])
        
        # Update scores
        player_score, computer_score, rounds = self.game_logic.get_scores()
        self.score_label.config(text=f"Score: {player_score} - {computer_score}")
        self.rounds_label.config(text=f"Rounds Played: {rounds}")
    
    def reset_game(self):
        """Reset the game scores"""
        self.game_logic.reset_scores()
        player_score, computer_score, rounds = self.game_logic.get_scores()
        self.score_label.config(text=f"Score: {player_score} - {computer_score}")
        self.rounds_label.config(text=f"Rounds Played: {rounds}")
        self.result_label.config(text="Choose your move!", fg=self.theme["text_secondary"])
    
    def show_wifi_menu(self):
        """Display Wi-Fi multiplayer menu"""
        self.clear_screen()
        self.current_screen = "wifi_menu"
        self.root.configure(bg=self.theme["bg"])
        
        # Theme toggle
        self.create_theme_toggle(self.root)
        
        # Title
        title_frame = tk.Frame(self.root, bg=self.theme["bg"])
        title_frame.pack(pady=30)
        
        title = tk.Label(title_frame, text="📡 Wi-Fi Multiplayer", 
                        font=("Helvetica", 24, "bold"), 
                        fg=self.theme["success"], bg=self.theme["bg"])
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Connect via local network", 
                           font=("Helvetica", 12), 
                           fg=self.theme["text_secondary"], bg=self.theme["bg"])
        subtitle.pack(pady=10)
        
        # Buttons
        buttons_frame = tk.Frame(self.root, bg=self.theme["bg"])
        buttons_frame.pack(pady=30)
        
        host_btn = ModernButton(buttons_frame, "🏠 Host Game", 
                               self.show_wifi_host,
                               width=280, height=70,
                               bg_color=self.theme["success"], 
                               hover_color=self.theme["success_hover"])
        host_btn.pack(pady=15)
        
        join_btn = ModernButton(buttons_frame, "🔗 Join Game", 
                               self.show_wifi_join_input,
                               width=280, height=70,
                               bg_color=self.theme["primary"], 
                               hover_color=self.theme["primary_hover"])
        join_btn.pack(pady=15)
        
        back_btn = ModernButton(buttons_frame, "⬅️ Back", 
                               self.show_main_menu,
                               width=280, height=60,
                               bg_color=self.theme["gray"], 
                               hover_color=self.theme["gray_hover"])
        back_btn.pack(pady=15)
    
    def show_wifi_host(self):
        """Show Wi-Fi host screen and start server"""
        self.clear_screen()
        self.current_screen = "wifi_host"
        self.root.configure(bg=self.theme["bg"])
        self.is_hosting = True
        
        # Theme toggle
        self.create_theme_toggle(self.root)
        
        # Title
        title = tk.Label(self.root, text="🏠 Hosting Game", 
                        font=("Helvetica", 22, "bold"), 
                        fg=self.theme["success"], bg=self.theme["bg"])
        title.pack(pady=20)
        
        # Info frame
        info_frame = tk.Frame(self.root, bg=self.theme["secondary_bg"], padx=20, pady=20)
        info_frame.pack(pady=10, padx=30, fill=tk.X)
        
        local_ip = get_local_ip()
        port = 50007
        
        info_text = f"📍 Your IP Address: {local_ip}\n🔌 Port: {port}\n\n" \
                   f"Share this information with your friend!\n" \
                   f"Waiting for player to connect..."
        
        self.host_info_label = tk.Label(info_frame, text=info_text, 
                                       font=("Helvetica", 11), 
                                       fg=self.theme["text"], 
                                       bg=self.theme["secondary_bg"],
                                       justify=tk.LEFT)
        self.host_info_label.pack()
        
        # Status label
        self.host_status_label = tk.Label(self.root, text="⏳ Waiting for connection...", 
                                         font=("Helvetica", 12, "bold"), 
                                         fg=self.theme["warning"], bg=self.theme["bg"])
        self.host_status_label.pack(pady=20)
        
        # Cancel button
        cancel_btn = ModernButton(self.root, "Cancel", 
                                 self.stop_hosting,
                                 width=200, height=50,
                                 bg_color=self.theme["danger"], 
                                 hover_color=self.theme["danger_hover"])
        cancel_btn.pack(pady=20)
        
        # Start server in background
        self.multiplayer_running = True
        self.multiplayer_thread = threading.Thread(target=self.run_server, daemon=True)
        self.multiplayer_thread.start()
    
    def run_server(self):
        """Run the Wi-Fi server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', 50007))
            self.server_socket.listen(1)
            
            self.connection, addr = self.server_socket.accept()
            
            # Update UI
            self.root.after(0, lambda: self.host_status_label.config(
                text=f"✅ Connected to {addr[0]}", fg=self.theme["success"]))
            
            # Send handshake
            handshake = create_message("handshake", player="host", version="1.0")
            self.connection.sendall((handshake + "\n").encode())
            
            # Wait a moment then show game screen
            self.root.after(1000, self.show_multiplayer_game)
            
        except Exception as e:
            if self.multiplayer_running:
                self.root.after(0, lambda: messagebox.showerror("Server Error", str(e)))
                self.root.after(0, self.show_wifi_menu)
    
    def stop_hosting(self):
        """Stop hosting the game"""
        self.multiplayer_running = False
        if self.connection:
            try:
                disconnect_msg = create_message("disconnect")
                self.connection.sendall((disconnect_msg + "\n").encode())
                self.connection.close()
            except:
                pass
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        self.show_wifi_menu()
    
    def show_wifi_join_input(self):
        """Show input screen for joining a game"""
        self.clear_screen()
        self.current_screen = "wifi_join_input"
        self.root.configure(bg=self.theme["bg"])
        
        # Theme toggle
        self.create_theme_toggle(self.root)
        
        # Title
        title = tk.Label(self.root, text="🔗 Join Game", 
                        font=("Helvetica", 22, "bold"), 
                        fg=self.theme["primary"], bg=self.theme["bg"])
        title.pack(pady=30)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=self.theme["secondary_bg"], padx=30, pady=30)
        input_frame.pack(pady=20, padx=40, fill=tk.X)
        
        # IP input
        ip_label = tk.Label(input_frame, text="Host IP Address:", 
                           font=("Helvetica", 12), 
                           fg=self.theme["text"], bg=self.theme["secondary_bg"])
        ip_label.pack(anchor="w", pady=(0, 5))
        
        self.ip_entry = tk.Entry(input_frame, font=("Helvetica", 12), 
                                width=30, bg=self.theme["bg"], 
                                fg=self.theme["text"])
        self.ip_entry.pack(pady=(0, 15))
        self.ip_entry.insert(0, "192.168.1.100")  # Placeholder
        
        # Port input
        port_label = tk.Label(input_frame, text="Port (default: 50007):", 
                             font=("Helvetica", 12), 
                             fg=self.theme["text"], bg=self.theme["secondary_bg"])
        port_label.pack(anchor="w", pady=(0, 5))
        
        self.port_entry = tk.Entry(input_frame, font=("Helvetica", 12), 
                                  width=30, bg=self.theme["bg"], 
                                  fg=self.theme["text"])
        self.port_entry.pack()
        self.port_entry.insert(0, "50007")
        
        # Status label
        self.join_status_label = tk.Label(self.root, text="", 
                                         font=("Helvetica", 11), 
                                         fg=self.theme["text_secondary"], 
                                         bg=self.theme["bg"])
        self.join_status_label.pack(pady=10)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg=self.theme["bg"])
        button_frame.pack(pady=20)
        
        connect_btn = ModernButton(button_frame, "Connect", 
                                  self.connect_to_host,
                                  width=150, height=50,
                                  bg_color=self.theme["success"], 
                                  hover_color=self.theme["success_hover"])
        connect_btn.grid(row=0, column=0, padx=10)
        
        back_btn = ModernButton(button_frame, "Back", 
                               self.show_wifi_menu,
                               width=150, height=50,
                               bg_color=self.theme["gray"], 
                               hover_color=self.theme["gray_hover"])
        back_btn.grid(row=0, column=1, padx=10)
    
    def connect_to_host(self):
        """Connect to the host"""
        host_ip = self.ip_entry.get().strip()
        try:
            port = int(self.port_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Port", "Please enter a valid port number")
            return
        
        self.join_status_label.config(text=f"⏳ Connecting to {host_ip}:{port}...", 
                                     fg=self.theme["warning"])
        self.root.update()
        
        # Connect in background
        threading.Thread(target=self.run_client, args=(host_ip, port), daemon=True).start()
    
    def run_client(self, host, port):
        """Run the Wi-Fi client"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.connection = self.client_socket
            self.multiplayer_running = True
            
            # Receive handshake
            data = self.client_socket.recv(1024).decode().strip()
            msg = parse_message(data)
            
            if msg and msg.get("type") == "handshake":
                self.root.after(0, lambda: self.join_status_label.config(
                    text="✅ Connected successfully!", fg=self.theme["success"]))
                self.root.after(1000, self.show_multiplayer_game)
            else:
                raise Exception("Invalid handshake")
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Connection Error", 
                                                            f"Failed to connect: {str(e)}"))
            self.root.after(0, lambda: self.join_status_label.config(
                text="❌ Connection failed", fg=self.theme["danger"]))
    
    def show_multiplayer_game(self):
        """Show the multiplayer game screen"""
        self.clear_screen()
        self.current_screen = "multiplayer_game"
        self.root.configure(bg=self.theme["bg"])
        self.player_score = 0
        self.opponent_score = 0
        
        # Theme toggle
        self.create_theme_toggle(self.root)
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.theme["secondary_bg"], height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        role = "Host" if self.is_hosting else "Guest"
        title = tk.Label(header_frame, text=f"Multiplayer Mode ({role})", 
                        font=("Helvetica", 18, "bold"), 
                        fg=self.theme["success"], bg=self.theme["secondary_bg"])
        title.pack(pady=20)
        
        # Score frame
        score_frame = tk.Frame(self.root, bg=self.theme["bg"])
        score_frame.pack(pady=15)
        
        self.mp_score_label = tk.Label(score_frame, text="Score: 0 - 0", 
                                       font=("Helvetica", 16, "bold"), 
                                       fg=self.theme["text"], bg=self.theme["bg"])
        self.mp_score_label.pack()
        
        # Result display
        self.mp_result_label = tk.Label(self.root, text="Choose your move!", 
                                       font=("Helvetica", 13), 
                                       fg=self.theme["text_secondary"], 
                                       bg=self.theme["bg"],
                                       wraplength=450)
        self.mp_result_label.pack(pady=15)
        
        # Move buttons
        moves_frame = tk.Frame(self.root, bg=self.theme["bg"])
        moves_frame.pack(pady=15)
        
        self.mp_rock_btn = ModernButton(moves_frame, "🪨 Rock", 
                                        lambda: self.play_multiplayer_move("Rock"),
                                        width=140, height=100,
                                        bg_color=self.theme["danger"], 
                                        hover_color=self.theme["danger_hover"])
        self.mp_rock_btn.grid(row=0, column=0, padx=10)
        
        self.mp_paper_btn = ModernButton(moves_frame, "📄 Paper", 
                                         lambda: self.play_multiplayer_move("Paper"),
                                         width=140, height=100,
                                         bg_color=self.theme["primary"], 
                                         hover_color=self.theme["primary_hover"])
        self.mp_paper_btn.grid(row=0, column=1, padx=10)
        
        self.mp_scissors_btn = ModernButton(moves_frame, "✂️ Scissors", 
                                            lambda: self.play_multiplayer_move("Scissors"),
                                            width=140, height=100,
                                            bg_color=self.theme["success"], 
                                            hover_color=self.theme["success_hover"])
        self.mp_scissors_btn.grid(row=0, column=2, padx=10)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg=self.theme["bg"])
        control_frame.pack(pady=20)
        
        disconnect_btn = ModernButton(control_frame, "Disconnect", 
                                     self.disconnect_multiplayer,
                                     width=200, height=45,
                                     bg_color=self.theme["danger"], 
                                     hover_color=self.theme["danger_hover"])
        disconnect_btn.pack()
        
        # Start listening for opponent moves
        threading.Thread(target=self.listen_for_moves, daemon=True).start()
    
    def play_multiplayer_move(self, move):
        """Handle multiplayer move"""
        if self.waiting_for_opponent:
            messagebox.showinfo("Wait", "Waiting for opponent's move!")
            return
        
        self.waiting_for_opponent = True
        self.mp_result_label.config(text=f"You chose {move}! Waiting for opponent...", 
                                   fg=self.theme["warning"])
        
        # Send move
        try:
            move_msg = create_message("move", player="player", move=move)
            self.connection.sendall((move_msg + "\n").encode())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send move: {str(e)}")
            self.waiting_for_opponent = False
    
    def listen_for_moves(self):
        """Listen for opponent moves"""
        while self.multiplayer_running:
            try:
                data = self.connection.recv(1024).decode().strip()
                if not data:
                    break
                
                msg = parse_message(data)
                if not msg:
                    continue
                
                if msg.get("type") == "move":
                    opponent_move = msg.get("move")
                    # Process the round (simplified - in real implementation, host should validate)
                    self.root.after(0, lambda: self.process_multiplayer_round(opponent_move))
                
                elif msg.get("type") == "disconnect":
                    self.root.after(0, lambda: messagebox.showinfo("Disconnected", 
                                                                   "Opponent disconnected"))
                    self.root.after(0, self.show_wifi_menu)
                    break
                    
            except Exception as e:
                if self.multiplayer_running:
                    self.root.after(0, lambda: messagebox.showerror("Connection Error", str(e)))
                break
    
    def process_multiplayer_round(self, opponent_move):
        """Process a multiplayer round"""
        # This is a simplified version - you'd want the host to be authoritative
        if not self.waiting_for_opponent:
            return
        
        # Get player's last move (stored when they clicked)
        # For simplicity, we'll show the result
        self.waiting_for_opponent = False
        
        # Update result
        result_text = f"Opponent chose {opponent_move}!"
        self.mp_result_label.config(text=result_text, fg=self.theme["primary"])
        
        # In a full implementation, you'd calculate winner and update scores here
    
    def disconnect_multiplayer(self):
        """Disconnect from multiplayer game"""
        self.multiplayer_running = False
        try:
            if self.connection:
                disconnect_msg = create_message("disconnect")
                self.connection.sendall((disconnect_msg + "\n").encode())
                self.connection.close()
        except:
            pass
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        
        self.show_wifi_menu()
    
    def show_bluetooth_menu(self):
        """Display Bluetooth multiplayer menu"""
        self.clear_screen()
        self.current_screen = "bluetooth_menu"
        self.root.configure(bg=self.theme["bg"])
        
        # Theme toggle
        self.create_theme_toggle(self.root)
        
        # Title
        title_frame = tk.Frame(self.root, bg=self.theme["bg"])
        title_frame.pack(pady=30)
        
        title = tk.Label(title_frame, text="📱 Bluetooth Multiplayer", 
                        font=("Helvetica", 24, "bold"), 
                        fg=self.theme["warning"], bg=self.theme["bg"])
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Connect via Bluetooth", 
                           font=("Helvetica", 12), 
                           fg=self.theme["text_secondary"], bg=self.theme["bg"])
        subtitle.pack(pady=10)
        
        # Info message
        info_frame = tk.Frame(self.root, bg=self.theme["secondary_bg"], padx=25, pady=25)
        info_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        info_text = ("📋 Bluetooth Multiplayer Requirements:\n\n"
                    "✓ Bluetooth adapter on both devices\n"
                    "✓ PyBluez or Bleak library installed\n"
                    "✓ Platform-specific Bluetooth permissions\n"
                    "✓ Devices paired beforehand\n\n"
                    "⚙️ Installation:\n"
                    "   pip install pybluez  (Linux/Windows)\n"
                    "   pip install bleak    (Cross-platform BLE)\n\n"
                    "⚠️ Note: This feature requires additional\n"
                    "setup and may not work on all systems.\n\n"
                    "For now, please use Wi-Fi multiplayer\n"
                    "for the best experience!")
        
        info_label = tk.Label(info_frame, text=info_text, 
                             font=("Helvetica", 11), 
                             fg=self.theme["text"], 
                             bg=self.theme["secondary_bg"],
                             justify=tk.LEFT)
        info_label.pack()
        
        # Back button
        back_btn = ModernButton(self.root, "⬅️ Back to Menu", 
                               self.show_main_menu,
                               width=250, height=60,
                               bg_color=self.theme["gray"], 
                               hover_color=self.theme["gray_hover"])
        back_btn.pack(pady=20)


def create_app():
    """Create and return the main application"""
    root = tk.Tk()
    app = GameUI(root)
    return root


if __name__ == "__main__":
    root = create_app()
    root.mainloop()
