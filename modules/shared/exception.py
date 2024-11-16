from fastapi import HTTPException


class Exceptions():

    def not_found(self, item_not_found: str = ""):
        raise HTTPException(status_code=404, detail=f"{item_not_found} not found")
    
    def server_error(self, message: str = "Internal Server Error"):
        raise HTTPException(status_code=500, detail=message)
    
    def bad_request(self, message: str = "Bad Request"):
        raise HTTPException(status_code=400, detail=message)
    

