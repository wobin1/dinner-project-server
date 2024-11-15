from modules.shared.models import User, session


class Utility():
    def get_user(self, id):
        user = session.query(User).filter(User.id == id).first()
        return user
    def guest_to_dict(self, guests):
        guests_data = {}
        data = []
        for guest in guests:
            guests_data['id'] = guest.id
            guests_data['full_name'] = guest.full_name
            guests_data['email'] = guest.email
            guests_data['phone_number'] = guest.phone_number
            guests_data['church'] = self.get_user(guest.church)
            guests_data['attendance_status'] = guest.attendance_status

            data.append(guests_data)
            guests_data = {}

        return data