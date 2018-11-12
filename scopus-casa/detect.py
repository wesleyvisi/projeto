# -*- coding: utf-8 -*-

from camera import Camera
from settings import Settings
from status import Status


    
def main():
        
    settings = Settings()

    listaCam = []
    
    status = Status()
        
        
    for item in settings.cameras:
            listaCam.append(Camera(item[0],item[1],item[2],item[3],item[4],item[5],item[6],status))

if __name__ == "__main__":
    main()

    

