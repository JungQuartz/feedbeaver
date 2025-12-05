from config_loader import load_config
from feed_checker import monitor_feeds


def main():
    config = load_config()
    monitor_feeds(config)


if __name__ == "__main__":
    main()