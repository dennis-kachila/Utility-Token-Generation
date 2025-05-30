"""
Modern, interactive GUI interface for the Utility Token Generation project
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import subprocess
import io
from contextlib import redirect_stdout
from PIL import Image, ImageTk
import time
import importlib
from typing import Dict, Any, Optional, List, Tuple, Union
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for matplotlib

class RedirectText:
    """Redirect stdout to a tkinter Text widget"""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""

    def write(self, string):
        self.buffer += string
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)  # Auto-scroll to the end
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass

class UtilityTokenApp:
    """Main application class for the Utility Token GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Utility Token Generator")
        self.root.geometry("1000x700")  # Larger window
        self.root.minsize(900, 600)
        
        # Create a theme
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a theme that looks good on Windows
        
        # Configure modern colors
        primary_color = "#4CAF50"
        secondary_color = "#2E7D32"
        bg_color = "#f5f5f5"
        text_color = "#212121"
        accent_color = "#FF9800"
        
        # Configure button styles
        self.style.configure(
            "TButton", 
            padding=8, 
            relief="flat",
            background=primary_color,
            foreground="white",
            font=('Arial', 10, 'bold')
        )
        self.style.map(
            "TButton",
            background=[('active', secondary_color), ('pressed', secondary_color)]
        )
        
        # Input field styles
        self.style.configure(
            "TEntry", 
            padding=8,
            relief="flat",
            fieldbackground="white"
        )
        
        # Frame styles
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("Card.TFrame", background="white", relief="raised")
        
        # Label styles
        self.style.configure("TLabel", background=bg_color, foreground=text_color, font=('Arial', 10))
        self.style.configure("Header.TLabel", background=bg_color, foreground=text_color, font=('Arial', 18, 'bold'))
        self.style.configure("SubHeader.TLabel", background=bg_color, foreground=text_color, font=('Arial', 14, 'bold'))
        self.style.configure("Status.TLabel", background=accent_color, foreground="white", font=('Arial', 10))

        # Store form inputs
        self.input_vars = {}
        
        # Store visualization images
        self.current_images = []
        
        # Store current view (for swapping content)
        self.current_content_frame = None
        self.content_frames = {}
        
        # Create the main layout
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange all the widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header bar
        header_bar = ttk.Frame(main_frame, style="TFrame", padding="10")
        header_bar.pack(fill=tk.X, side=tk.TOP)
        
        header_label = ttk.Label(header_bar, 
                               text="Utility Token Generation Tool", 
                               style="Header.TLabel")
        header_label.pack(side=tk.LEFT)
        
        # Main content area with sidebar and content
        content_container = ttk.Frame(main_frame, style="TFrame")
        content_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Sidebar on the left
        self.sidebar = ttk.Frame(content_container, width=220, style="Card.TFrame", padding="10")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.sidebar.pack_propagate(False)
        
        # Create sidebar sections
        self.create_sidebar_section("Operations", [
            ("Generate Token", self.show_token_generator),
            ("Generate Decoder Key", self.show_decoder_key_generator),
            ("Decrypt Token", self.show_token_decrypter),
            ("Process Raw Data", self.show_data_cleaning),
            ("Run Tests", self.show_tests)
        ])
        
        self.create_sidebar_section("Visualization", [
            ("View Token Data", self.show_visualizer)
        ])
        
        # Add spacer
        ttk.Frame(self.sidebar, height=20).pack(fill=tk.X)
        
        # Exit button at the bottom
        exit_button = ttk.Button(self.sidebar, 
                               text="Exit", 
                               command=self.root.destroy,
                               style="TButton")
        exit_button.pack(fill=tk.X, pady=5)
        
        # Main content area on the right
        self.content_area = ttk.Frame(content_container, style="TFrame")
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Initialize content frames but don't display them yet
        self.initialize_content_frames()
        
        # Show the welcome frame initially
        self.show_welcome_screen()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, 
                             textvariable=self.status_var, 
                             relief=tk.SUNKEN, 
                             anchor=tk.W,
                             style="Status.TLabel")
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
    def create_sidebar_section(self, title, buttons):
        """Create a section in the sidebar with a title and buttons"""
        # Section container
        section_frame = ttk.Frame(self.sidebar)
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Section title
        title_label = ttk.Label(section_frame, 
                              text=title, 
                              style="SubHeader.TLabel")
        title_label.pack(fill=tk.X, pady=(0, 5))
        
        # Separator
        separator = ttk.Separator(section_frame, orient="horizontal")
        separator.pack(fill=tk.X, pady=5)
        
        # Buttons
        for button_text, command in buttons:
            self.create_button(section_frame, button_text, command)
    
    def create_button(self, parent, text, command):
        """Helper method to create a styled button"""
        button = ttk.Button(parent, 
                          text=text, 
                          command=command,
                          style="TButton")
        button.pack(fill=tk.X, pady=3)
        return button
    
    def update_status(self, message):
        """Update the status bar message"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def initialize_content_frames(self):
        """Initialize all content frames but don't display them yet"""
        # Welcome frame
        welcome_frame = ttk.Frame(self.content_area, style="Card.TFrame", padding=20)
        self.content_frames["welcome"] = welcome_frame
        
        welcome_title = ttk.Label(welcome_frame, 
                                text="Welcome to Utility Token Generator", 
                                style="Header.TLabel")
        welcome_title.pack(pady=(0, 20))
        
        welcome_text = ttk.Label(welcome_frame, 
                               text="Select an operation from the sidebar to get started.",
                               wraplength=500)
        welcome_text.pack()
        
        # Token Generator frame
        token_frame = self.create_form_frame("token_generator", "Generate Token")
        self.add_form_field(token_frame, "meter_number", "Meter Number:", "37194275246")
        self.add_form_field(token_frame, "amount", "Amount (KSh):", "100")
        self.add_submit_button(token_frame, "Generate Token", self.run_token_generator)
        self.add_output_area(token_frame)
        
        # Decoder Key Generator frame
        decoder_frame = self.create_form_frame("decoder_key", "Generate Decoder Key")
        self.add_form_field(decoder_frame, "key_type", "Key Type:", "2")
        self.add_form_field(decoder_frame, "supply_group", "Supply Group Code:", "123456")
        self.add_form_field(decoder_frame, "tariff_index", "Tariff Index:", "7")
        self.add_form_field(decoder_frame, "key_revision", "Key Revision Number:", "1")
        self.add_form_field(decoder_frame, "decoder_reference", "Decoder Reference Number:", "37194275246")
        self.add_submit_button(decoder_frame, "Generate Decoder Key", self.run_decoder_key_generator)
        self.add_output_area(decoder_frame)
        
        # Token Decrypter frame
        decrypt_frame = self.create_form_frame("token_decrypter", "Decrypt Token")
        self.add_form_field(decrypt_frame, "decrypt_meter_number", "Meter Number:", "37194275246")
        self.add_form_field(decrypt_frame, "token", "Token:", "1865-3776-4842-2132-9404")
        self.add_submit_button(decrypt_frame, "Decrypt Token", self.run_token_decrypter)
        self.add_output_area(decrypt_frame)
        
        # Data Cleaning frame
        clean_frame = self.create_form_frame("data_cleaning", "Process Raw Data")
        self.add_submit_button(clean_frame, "Process Raw Token Data", self.run_data_cleaning)
        self.add_output_area(clean_frame)
        
        # Visualizer frame
        viz_frame = self.create_form_frame("visualizer", "Visualize Token Data")
        
        # Add visualization options
        viz_options_frame = ttk.Frame(viz_frame)
        viz_options_frame.pack(fill=tk.X, pady=10)
        
        viz_option_label = ttk.Label(viz_options_frame, text="Select Visualization:")
        viz_option_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.viz_option = tk.StringVar(value="all")
        options = [
            ("All Visualizations", "all"),
            ("Units Over Time", "units_over_time"),
            ("Amount Distribution", "amount_distribution"),
            ("Units per Amount", "units_per_amount"),
            ("Monthly Spending", "monthly_spending"),
            ("Dashboard", "dashboard")
        ]
        
        option_menu = ttk.OptionMenu(viz_options_frame, self.viz_option, options[0][0], *[o[0] for o in options])
        option_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add visualization button
        self.add_submit_button(viz_frame, "Generate Visualizations", self.run_visualizer)
        
        # Add area to display visualizations
        viz_display_frame = ttk.Frame(viz_frame)
        viz_display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Canvas for displaying visualizations
        viz_canvas = tk.Canvas(viz_display_frame, bg="white", highlightthickness=0)
        viz_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        viz_scrollbar = ttk.Scrollbar(viz_display_frame, orient="vertical", command=viz_canvas.yview)
        viz_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        viz_canvas.configure(yscrollcommand=viz_scrollbar.set)
        viz_canvas.bind("<Configure>", lambda e: viz_canvas.configure(scrollregion=viz_canvas.bbox("all")))
        
        # Create frame inside canvas for images
        self.viz_images_frame = ttk.Frame(viz_canvas)
        viz_canvas.create_window((0, 0), window=self.viz_images_frame, anchor="nw")
        
        # Test frame
        test_frame = self.create_form_frame("test", "Run Component Tests")
        self.add_submit_button(test_frame, "Run Tests", self.run_tests)
        self.add_output_area(test_frame)
    
    def create_form_frame(self, name, title):
        """Create a form frame with a title"""
        frame = ttk.Frame(self.content_area, style="Card.TFrame", padding=20)
        self.content_frames[name] = frame
        
        title_label = ttk.Label(frame, text=title, style="Header.TLabel")
        title_label.pack(fill=tk.X, pady=(0, 20))
        
        return frame
    
    def add_form_field(self, parent, var_name, label_text, default=""):
        """Add a form field with label and entry"""
        field_frame = ttk.Frame(parent)
        field_frame.pack(fill=tk.X, pady=5)
        
        label = ttk.Label(field_frame, text=label_text, width=20)
        label.pack(side=tk.LEFT)
        
        var = tk.StringVar(value=default)
        self.input_vars[var_name] = var
        
        entry = ttk.Entry(field_frame, textvariable=var, width=40)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        return field_frame
    
    def add_submit_button(self, parent, text, command):
        """Add a submit button to a form"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=15)
        
        button = ttk.Button(button_frame, text=text, command=command, style="TButton")
        button.pack(side=tk.RIGHT)
        
        return button
    
    def add_output_area(self, parent):
        """Add an output text area to a frame"""
        output_frame = ttk.Frame(parent)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        output_label = ttk.Label(output_frame, text="Output:")
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        output_text = scrolledtext.ScrolledText(output_frame, 
                                               wrap=tk.WORD, 
                                               width=50, 
                                               height=15)
        output_text.pack(fill=tk.BOTH, expand=True)
        output_text.configure(state="disabled")
        
        # Store reference to the output text widget in the parent frame
        parent.output_text = output_text
        
        return output_text
    
    def show_content_frame(self, name):
        """Show a specific content frame and hide the current one"""
        # Hide current frame if any
        if self.current_content_frame:
            self.current_content_frame.pack_forget()
        
        # Show the requested frame
        frame = self.content_frames.get(name)
        if frame:
            frame.pack(fill=tk.BOTH, expand=True)
            self.current_content_frame = frame
        
        # Update status
        self.update_status(f"Ready - {name.replace('_', ' ').title()}")
    
    def show_welcome_screen(self):
        """Show the welcome screen"""
        self.show_content_frame("welcome")
    
    def show_token_generator(self):
        """Show the token generator form"""
        self.show_content_frame("token_generator")
    
    def show_decoder_key_generator(self):
        """Show the decoder key generator form"""
        self.show_content_frame("decoder_key")
    
    def show_token_decrypter(self):
        """Show the token decrypter form"""
        self.show_content_frame("token_decrypter")
    
    def show_data_cleaning(self):
        """Show the data cleaning form"""
        self.show_content_frame("data_cleaning")
    
    def show_visualizer(self):
        """Show the visualizer form"""
        self.show_content_frame("visualizer")
        self.clear_visualizations()
    
    def show_tests(self):
        """Show the test form"""
        self.show_content_frame("test")
    
    def clear_output(self):
        """Clear the output text area of the current frame"""
        if self.current_content_frame and hasattr(self.current_content_frame, 'output_text'):
            output_text = self.current_content_frame.output_text
            output_text.configure(state="normal")
            output_text.delete(1.0, tk.END)
            output_text.configure(state="disabled")
    
    def display_output(self, text):
        """Display text in the output area of the current frame"""
        if self.current_content_frame and hasattr(self.current_content_frame, 'output_text'):
            output_text = self.current_content_frame.output_text
            output_text.configure(state="normal")
            output_text.insert(tk.END, text)
            output_text.see(tk.END)  # Auto-scroll to the end
            output_text.configure(state="disabled")
    
    def clear_visualizations(self):
        """Clear all visualizations from the visualization frame"""
        for widget in self.viz_images_frame.winfo_children():
            widget.destroy()
        
        # Clear image references to prevent memory leaks
        self.current_images = []
        
    def run_script_with_input(self, module_name, function_name=None, inputs=None):
        """Run a Python module with specified inputs and capture its output"""
        self.clear_output()
        self.update_status(f"Running {module_name}...")
        
        # Create a buffer to capture output
        output_buffer = io.StringIO()
        old_stdout = sys.stdout
        old_stdin = sys.stdin
        
        try:
            # Import the module dynamically
            if module_name.endswith(".py"):
                module_name = module_name[:-3]  # Remove .py extension
            
            # Prefix with src. for proper import
            if not module_name.startswith("src."):
                module_name = f"src.{module_name}"
                
            if inputs:
                # Replace stdin with a StringIO object containing the inputs
                input_str = "\n".join(str(inp) for inp in inputs)
                sys.stdin = io.StringIO(input_str)
            
            # Redirect stdout to our buffer
            sys.stdout = output_buffer
            
            # Import or reload the module
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)
            
            # If a specific function is provided, call it
            if function_name:
                func = getattr(module, function_name)
                result = func(*inputs) if inputs else func()
                return result
            
            # Run the script and capture output
            output = output_buffer.getvalue()
            self.display_output(output)
            
            self.update_status(f"Completed {module_name}")
            return output
            
        except Exception as e:
            error_msg = f"Error running {module_name}: {str(e)}"
            self.display_output(error_msg)
            self.update_status(f"Error running {module_name}")
            return None
        finally:
            sys.stdout = old_stdout
            sys.stdin = old_stdin
    
    def run_in_thread(self, func, *args, **kwargs):
        """Run a function in a separate thread"""
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    
    def display_images(self, image_paths):
        """Display images in the visualization frame"""
        # Clear existing images
        self.clear_visualizations()
        
        for i, img_path in enumerate(image_paths):
            try:
                # Skip if image doesn't exist
                if not os.path.exists(img_path):
                    self.display_output(f"Warning: Image not found: {img_path}\n")
                    continue
                    
                # Create a frame for this image
                img_frame = ttk.Frame(self.viz_images_frame, padding=10)
                img_frame.pack(fill=tk.X, pady=10)
                
                # Extract image name from path for the title
                img_name = os.path.basename(img_path).replace('_', ' ').replace('.png', '').title()
                
                # Add image title
                title_label = ttk.Label(img_frame, text=img_name, style="SubHeader.TLabel")
                title_label.pack(pady=(0, 10))
                
                # Load and display the image
                pil_img = Image.open(img_path)
                
                # Resize if too large while maintaining aspect ratio
                max_width = 800
                if pil_img.width > max_width:
                    ratio = max_width / pil_img.width
                    new_width = max_width
                    new_height = int(pil_img.height * ratio)
                    pil_img = pil_img.resize((new_width, new_height), Image.LANCZOS)
                
                tk_img = ImageTk.PhotoImage(pil_img)
                
                # Keep a reference to prevent garbage collection
                self.current_images.append(tk_img)
                
                # Create and pack the image label
                img_label = ttk.Label(img_frame, image=tk_img)
                img_label.pack()
                
                # Add separator except for the last image
                if i < len(image_paths) - 1:
                    separator = ttk.Separator(self.viz_images_frame, orient="horizontal")
                    separator.pack(fill=tk.X, pady=10)
                    
            except Exception as e:
                self.display_output(f"Error loading image {img_path}: {str(e)}\n")
    
    # Button command handlers
    def run_token_generator(self):
        """Generate a token using user input"""
        meter_number = self.input_vars["meter_number"].get()
        amount = self.input_vars["amount"].get()
        
        if not meter_number or not amount:
            messagebox.showerror("Input Error", "Please provide both meter number and amount")
            return
        
        self.update_status("Generating token...")
        self.run_in_thread(self.run_script_with_input, "Token", None, [meter_number, amount])
    
    def run_decoder_key_generator(self):
        """Generate a decoder key using user input"""
        key_type = self.input_vars["key_type"].get()
        supply_group = self.input_vars["supply_group"].get()
        tariff_index = self.input_vars["tariff_index"].get()
        key_revision = self.input_vars["key_revision"].get()
        decoder_reference = self.input_vars["decoder_reference"].get()
        
        if not all([key_type, supply_group, tariff_index, key_revision, decoder_reference]):
            messagebox.showerror("Input Error", "Please provide all required fields")
            return
        
        self.update_status("Generating decoder key...")
        self.run_in_thread(self.run_script_with_input, "DKGA02", None, 
                           [key_type, supply_group, tariff_index, key_revision, decoder_reference])
    
    def run_token_decrypter(self):
        """Decrypt a token using user input"""
        meter_number = self.input_vars["decrypt_meter_number"].get()
        token = self.input_vars["token"].get()
        
        if not meter_number or not token:
            messagebox.showerror("Input Error", "Please provide both meter number and token")
            return
        
        self.update_status("Decrypting token...")
        self.run_in_thread(self.run_script_with_input, "TokenDecrypter", None, [meter_number, token])
    
    def run_data_cleaning(self):
        """Run data cleaning on raw token data"""
        self.update_status("Processing raw token data...")
        
        def process_and_update():
            output = self.run_script_with_input("data_cleaning")
            self.update_status("Data processed successfully!")
            
            # Check if files were created and show confirmation
            base_dir = os.path.dirname(os.path.dirname(__file__))
            csv_path = os.path.join(base_dir, "resources", "data", "cleaned_meter_data.csv")
            excel_path = os.path.join(base_dir, "resources", "data", "cleaned_meter_data.xlsx")
            
            if os.path.exists(csv_path) and os.path.exists(excel_path):
                self.display_output("\nFiles created successfully:\n")
                self.display_output(f"- CSV: {csv_path}\n")
                self.display_output(f"- Excel: {excel_path}\n")
                
                # Ask if user wants to view the data
                if messagebox.askyesno("Success", "Data processed successfully! Would you like to visualize the data now?"):
                    self.show_visualizer()
                    self.run_visualizer()
        
        self.run_in_thread(process_and_update)
    
    def run_visualizer(self):
        """Run visualization on processed data"""
        self.update_status("Generating visualizations...")
        
        def generate_and_display():
            # Run the visualizer script
            self.run_script_with_input("TokenVisualizer")
            
            # Determine which images to display based on selection
            viz_type = self.viz_option.get()
            image_paths = []
            
            # Map visualization names to file names
            viz_file_names = [
                "units_over_time.png", 
                "amount_distribution.png", 
                "units_per_amount.png", 
                "monthly_spending.png", 
                "token_data_dashboard.png"
            ]
            
            # Base directory for images
            base_dir = os.path.dirname(os.path.dirname(__file__))
            image_dir = os.path.join(base_dir, "resources", "images")
            
            # Get the correct paths for the image files
            all_image_paths = [os.path.join(image_dir, file) for file in viz_file_names]
            
            # Filter based on selection
            if viz_type == "all":
                image_paths = [path for path in all_image_paths if os.path.exists(path)]
            else:
                # Get the filename for the selected visualization
                selected_type_map = {
                    "Units Over Time": "units_over_time.png",
                    "Amount Distribution": "amount_distribution.png",
                    "Units per Amount": "units_per_amount.png",
                    "Monthly Spending": "monthly_spending.png",
                    "Dashboard": "token_data_dashboard.png"
                }
                selected_file = selected_type_map.get(viz_type)
                if selected_file:
                    selected_path = os.path.join(image_dir, selected_file)
                    if os.path.exists(selected_path):
                        image_paths = [selected_path]
            
            if image_paths:
                self.display_images(image_paths)
                self.update_status("Visualizations generated successfully!")
            else:
                self.display_output("No visualization images found. Please make sure data has been processed first.")
                self.update_status("Visualization failed - no images found")
        
        self.run_in_thread(generate_and_display)
    
    def run_tests(self):
        """Run component tests"""
        self.update_status("Running component tests...")
        self.run_in_thread(self.run_script_with_input, "test_components")

if __name__ == "__main__":
    # Set up high DPI awareness for Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass  # Not on Windows or not supported
    
    root = tk.Tk()
    root.title("Utility Token Generator")
    
    # Set app icon if available
    try:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except:
        pass
    
    # Center the window on screen
    window_width = 1000
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    app = UtilityTokenApp(root)
    
    # Handle window close event gracefully
    def on_closing():
        if messagebox.askokcancel("Quit", "Are you sure you want to exit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Set minimum size for the window
    root.minsize(900, 600)
    
    root.mainloop()
