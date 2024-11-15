
class Utility():

    def user_to_dict(self, users):
        users_data = {}
        data = []
        for user in users:
            users_data['id'] = user.id
            users_data['full_name'] = user.full_name
            users_data['email'] = user.email
            users_data['phone_number'] = user.phone_number
            users_data['is_active'] = user.is_active
            users_data['is_church'] = user.is_church
            users_data['is_admin'] = user.is_admin
            users_data['is_bouncer'] = user.is_bouncer

            data.append(users_data)
            users_data = {}

        return data