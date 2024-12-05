from modules.shared.models import User, TableType, session
from modules.shared.exception import Exceptions


exception= Exceptions()

class Utility():
    def get_user(self, id):
        print('user', id)
        user = session.query(User).filter(User.id == id).first()
        return user
    
    def get_table(self, table_id):
        print('getting table with id:', table_id)
        table = session.query(TableType).filter(TableType.id == table_id).first()
      
        print('table', table)
        return table
    
    def table_to_dict(self, tables):
        tables_data = {}
        data = []
        for table in tables:
            tables_data['id'] = table.id
            tables_data['type'] = table.type

            data.append(tables_data)
            tables_data = {}

        return data
    def guest_to_dict(self, guests):
        guests_data = {}
        data = []
        for guest in guests:
            guests_data['id'] = guest.id
            guests_data['full_name'] = guest.full_name
            guests_data['email'] = guest.email
            guests_data['phone_number'] = guest.phone_number
            guests_data['church'] = self.get_user(guest.church)
            guests_data['table'] = self.get_table(guest.table)
            guests_data['attendance_status'] = guest.attendance_status

            data.append(guests_data)
            guests_data = {}

        return data