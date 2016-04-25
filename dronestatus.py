class DroneStatus:

    class DroneStatusImpl:
        def __init__(self):
            self.status = "Drone Online"
        
    __instance = None

    def __init__(self):
        if DroneStatus.__instance is None:
            DroneStatus.__instance = DroneStatus.DroneStatusImpl()

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
