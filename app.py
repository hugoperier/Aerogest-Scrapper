from src.scrapper import DailyScrapper
import configparser

def main():
    config = getConfig()
    scrapper = DailyScrapper(config)
    scrapper.extract()

def getConfig():
    config = configparser.ConfigParser()
    config.read('default.conf')
    return config

if __name__ == "__main__":
    main()