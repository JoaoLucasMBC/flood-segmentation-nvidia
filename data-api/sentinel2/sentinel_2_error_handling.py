from datetime import datetime, timedelta

class Sentinel2ErrorHandler:

    @staticmethod  
    def coordinate_error_handling(coords: tuple, step: float):
        if coords[0] > coords[2] or coords[1] < coords[3]:
            raise ValueError("Invalid coordinates, the first two values must be the northwest corner (latitude and longitude) and the last two values must be the southeast corner (latitude and longitude) of the captured area.")
        if not (-90 <= coords[0] <= 90 and -180 <= coords[1] <= 180 and -90 <= coords[2] <= 90 and -180 <= coords[3] <= 180):
            raise ValueError("Invalid coordinates, latitude value must be between -90 and 90 and longitude value must be between -180 and 180.")
        if abs(abs(coords[0]) - abs(coords[2])) > 0.15:
            if not step:
                raise ValueError("The area is too big, please specify a step value for it to be divided.")
            if (step <= 0 or step > 0.15):
                raise ValueError("Invalid step value, it must be between 0 (exclusive) and 0.15 (inclusive).") 
    
    @staticmethod
    def time_interval_error_handling(time_interval: tuple):
        try:
            time_interval = (datetime.strptime(time_interval[0], "%Y-%m-%d"), datetime.strptime(time_interval[1], "%Y-%m-%d"))
            if time_interval[0] > time_interval[1]:
                raise ValueError("Invalid time interval, the first date must be before the second date.")
        except:
            raise ValueError("Invalid date format, it must be in the format 'YYYY-MM-DD'.")