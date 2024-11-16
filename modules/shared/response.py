

class Response():

    def success(self, status_code:int = 200, message:str = "success", data:dict = None):
        return {
            "status_code": status_code,
            "message": message, 
            "data": data
        }
    
    # def failure(self, message, error_code=500):

    def bad_request(self, message, error_code=403):
        return {
            "status_code": error_code,
            "message": message
        }
    
    def server_error(self, message, error_code=500):
        return {
            "status_code": error_code,
            "message": message
        }
    
    def not_found(self, message, error_code=404):
        return {
            "status_code": error_code,
            "message": message
        }