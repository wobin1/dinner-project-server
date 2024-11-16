from fastapi import APIRouter, Depends
from modules.shared.models import session, Guest, User
from passlib.context import CryptContext
from .schemas import GuestModel
from modules.shared.response import Response
from modules.shared.exception import Exceptions
from modules.auth.utils import Utility as auth_utils
from modules.auth.service import AuthService
from .utils import Utility

guests_router = APIRouter(
    prefix=('/guests'),
    tags=['guests']
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
response = Response()
exception = Exceptions()
utility = Utility()
auth_utility = auth_utils()
auth_service = AuthService()

@guests_router.get('/')
def get_guests():
    # print('current guest:', current_guest)
    guests = session.query(Guest).all()
    
    data = utility.guest_to_dict(guests)

    return response.success(data=data)

@guests_router.post('/')
def create_guest(payload: GuestModel):

    guest_exist = session.query(Guest).filter(Guest.email==payload.email).first()

    if guest_exist:
        return exception.bad_request(message="guest with email already exists")

    new_guest = Guest(full_name = payload.full_name, email = payload.email, phone_number = payload.phone_number, church = payload.church, attendance_status = 1)
    session.add(new_guest)
    session.commit()
    session.refresh(new_guest)
    print(new_guest)

    return response.success(data=new_guest.id)

@guests_router.get('/guest-metrics')
def get_guest_metrics():
    all_guests = session.query(Guest).all()
    guest_pending = session.query(Guest).filter(Guest.attendance_status == 1).all()
    guest_checkedin = session.query(Guest).filter(Guest.attendance_status == 2).all()
    guest_checkedout = session.query(Guest).filter(Guest.attendance_status == 3).all()

    metrics = {
        "total_quests": len(all_guests),
        "total_quest_pending": len(guest_pending),
        "total_quest_checkedin": len(guest_checkedin),
        "total_quest_checkedout": len(guest_checkedout)
    }

   

    return response.success(data=metrics)


@guests_router.get('/{guest_id}')
def get_single_guest(guest_id):
    guest = session.query(Guest).filter(Guest.id == guest_id).first()


    guests_data = {}
    guests_data['id'] = guest.id
    guests_data['full_name'] = guest.full_name
    guests_data['email'] = guest.email
    guests_data['phone_number'] = guest.phone_number
    guests_data['church'] = utility.get_user(guest.id)
    guests_data['attendance_status'] = guest.attendance_status


    return response.success(data= [guests_data])


@guests_router.patch('/checkin/{guest_id}')
def verify_guest(guest_id):
    guest = session.query(Guest).filter(Guest.id == guest_id).first()
    print('guest', guest)
    if guest.attendance_status == 1:
        guest.attendance_status = 2
        session.commit()
        return response.success(data= "guest checked in successfully")
    elif guest.attendance_status == 2:
        return exception.bad_request('User has already checked in')
    elif guest.attendance_status == 3:
        guest.attendance_status = 2
        session.commit()
        return response.success(data= "guest checked in successfully")
    else:
        return response.success(data= "Nothing happened")



@guests_router.patch('/checkout/{guest_id}')
def verify_guest(guest_id):
    guest = session.query(Guest).filter(Guest.id == guest_id).first()
    print('guest', guest)
    if guest.attendance_status == 2:
        guest.attendance_status = 3
        session.commit()
        return exception.bad_request('Guest checked out successfully')
    else:
        return response.success(data= "Guest is not checked in yet")





@guests_router.delete('/{guest_id}')
def delete_guest(guest_id: int):
    guest = session.query(guest).filter(guest.id == guest_id).first()
    
    if not guest:
        return response.error(message="guest not found", status_code=404)

    session.delete(guest)
    session.commit()

    return response.success(data="guest deleted successfully")
