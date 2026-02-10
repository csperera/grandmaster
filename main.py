from src.engine.session import run_v01_session

if __name__ == "__main__":
    try:
        run_v01_session()
    except KeyboardInterrupt:
        print("\nSession ended.")
    except Exception as e:
        print(f"An error occurred: {e}")