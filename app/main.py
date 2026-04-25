import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.agent.agent import SingleAgent
from app.tools.data_manager import DataManager
from app.core.logger import setup_logger

logger = setup_logger(__name__)


def print_help():
    """Display help message with available commands."""
    print("""
╔════════════════════════════════════════════════════════════╗
║           📊 AI Data Analyst Agent - Help                  ║
╚════════════════════════════════════════════════════════════╝

COMMANDS:
  - Type any question to analyze the current data
  - load <file>    : Load a CSV or Excel file
  - files          : List available data files
  - info           : Show current data file info
  - help           : Display this help message
  - exit           : Quit the application

EXAMPLES:
  ask: What is the average salary?
  ask: load data/my_data.csv
  ask: files
  ask: info
  ask: exit

SUPPORTED FORMATS:
  - CSV (.csv)
  - Excel (.xlsx, .xls)

TIP: Use relative paths from project root (e.g., 'data/my_file.csv')
     or absolute paths (e.g., 'C:\\Users\\...\\data.csv')
""")


def main():
    """Main entry point for the AI Data Analyst Agent."""
    
    print("""
╔════════════════════════════════════════════════════════════╗
║         🤖 Welcome to AI Data Analyst Agent                ║
║                                                            ║
║  An intelligent agent that analyzes data using AI         ║
║  Type 'help' for commands or start asking questions       ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize components
    agent = SingleAgent()
    data_manager = DataManager()
    
    # Display current data info
    print("\n📁 Current Data File:")
    print(data_manager.get_info_text())
    print()
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("\n❓ Ask: ").strip()
            
            # Handle empty input
            if not user_input:
                print("Please enter a question or command.")
                continue
            
            # Handle commands
            if user_input.lower() == "exit":
                print("\n👋 Thank you for using AI Data Analyst Agent. Goodbye!")
                break
            
            elif user_input.lower() == "help":
                print_help()
            
            elif user_input.lower() == "info":
                print("\n📊 Current Data File Information:")
                print(data_manager.get_info_text())
                
                # Show column types
                columns = data_manager.get_column_info()
                if columns:
                    print("\n📋 Column Data Types:")
                    for col, dtype in columns.items():
                        print(f"   - {col}: {dtype}")
            
            elif user_input.lower() == "files":
                available_files = data_manager.list_available_files()
                if available_files:
                    print("\n📂 Available Data Files:")
                    for i, file in enumerate(available_files, 1):
                        print(f"   {i}. {file}")
                else:
                    print("\n⚠️  No data files found in 'data' directory")
            
            elif user_input.lower().startswith("load "):
                # Extract file path
                file_path = user_input[5:].strip()
                
                # Try to load the file
                if data_manager.load_file(file_path):
                    print(f"\n✅ Successfully loaded data file!")
                    print(data_manager.get_info_text())
                    
                    # Update agent's reference to the file
                    agent.current_data_file = data_manager.get_file_path()
                    logger.info(f"Agent now analyzing: {agent.current_data_file}")
                else:
                    print(f"\n❌ Failed to load file: {file_path}")
                    print("   Make sure the file exists and is a valid CSV or Excel file.")
            
            else:
                # Treat as a data analysis question
                print("\n🧠 Analyzing...")
                
                # Pass the current data file to the agent
                agent.current_data_file = data_manager.get_file_path()
                
                # Run the agent
                answer = agent.run(user_input)
                
                # Display the answer
                print(f"\n✅ Final Answer:\n{answer}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            print(f"\n❌ An error occurred: {e}")
            print("   Please check the logs for more details.")


if __name__ == "__main__":
    main()