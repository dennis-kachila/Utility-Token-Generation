#!/bin/bash
# Utility Token Generation runner script
# This script activates the virtual environment and provides a menu to run different components

cd "$(dirname "$0")"
source utility/Scripts/activate

clear
echo "=========================================="
echo "  Utility Token Generation Project Runner"
echo "=========================================="
echo

select option in \
    "Generate a Token" \
    "Generate a Decoder Key" \
    "Decrypt a Token" \
    "Process Raw Token Data" \
    "Visualize Token Data" \
    "Run Component Tests" \
    "Launch GUI Interface" \
    "Exit"; do
    case $option in
        "Generate a Token")
            echo -e "\nRunning Token Generator...\n"
            python main.py token
            echo -e "\nPress Enter to continue..."
            read
            break
            ;;
        "Generate a Decoder Key")
            echo -e "\nRunning Decoder Key Generator...\n"
            python main.py key
            echo -e "\nPress Enter to continue..."
            read
            break
            ;;
        "Decrypt a Token")
            echo -e "\nRunning Token Decrypter...\n"
            python main.py decrypt
            echo -e "\nPress Enter to continue..."
            read
            break
            ;;
        "Process Raw Token Data")
            echo -e "\nRunning Data Cleaning...\n"
            python main.py clean
            echo -e "\nData processed and saved to cleaned_meter_data.csv and cleaned_meter_data.xlsx\n"
            echo -e "Press Enter to continue..."
            read
            break
            ;;
        "Visualize Token Data")
            echo -e "\nRunning Token Visualizer...\n"
            python main.py visualize
            echo -e "\nVisualization complete. Check the generated image files.\n"
            echo -e "Press Enter to continue..."
            read
            break
            ;;
        "Run Component Tests")
            echo -e "\nRunning Component Tests...\n"
            python main.py test
            echo -e "\nPress Enter to continue..."
            read
            break
            ;;
        "Launch GUI Interface")
            echo -e "\nLaunching Modern GUI Interface...\n"
            python main.py gui
            break
            ;;
        "Exit")
            echo "Exiting..."
            # Kill any running Python processes started by this script
            pkill -f "python main.py" 2>/dev/null || true
            deactivate 2>/dev/null || true
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
done

# Run the script again
exec "$0"

# Run the script again
exec "$0"
