import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.agent.agent import SingleAgent

def main():
    agent = SingleAgent()

    while True:
        query = input("\nAsk: ")
        if query.lower() == "exit":
            break

        answer = agent.run(query)
        print("\n✅ Final Answer:", answer)

if __name__ == "__main__":
    main()