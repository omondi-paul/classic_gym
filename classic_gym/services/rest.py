import frappe
from datetime import datetime, timedelta
from frappe.utils import now, getdate




class GymMember():

    def __init__(self):
        self.membershipType = frappe.db.get_all('Gym Membership', {}, ['type','price','duration'])
        self.workoutPlans=frappe.db.get_all('Gym Work Out Plans', {}, ['plan_name','trainer','price'])
        self.lockerBookings=frappe.db.get_all('Gym Locker Booking',{}, ['email','total_price'])

    def validateEmail(self,email):
        exists = frappe.db.exists('Gym Member', {'email': email})
        return exists


    def calculateDays(self,membership,membership_date):
        days=1
        for type in self.membershipType:
            subscription = type.type
            if subscription==membership:
                days=type.duration
            
            #Convert date joined string to a datetime object
            membership_date = getdate(membership_date)
    
        #     # Get today's date
            today_date = getdate(now())
            
        #     # Calculate the number of days passed
            days_passed = (today_date - membership_date).days
            remaining_days=days-days_passed

        return remaining_days
    
    def trainers(self,workout):
        trainer=[]
        for workOut in self.workoutPlans:
            if workOut.plan_name==workout:
                trainer.append(workOut.trainer)
                trainer.append(workOut.price)
          
        return trainer
    def membershipCost(self,type):
        cost=[]
        for member in self.membershipType:
            if member.type==type:
                cost.append(member.price)
          
        return cost
    
    def lockerCost(self, email):
        total_cost = 0
        for lockerBooking in self.lockerBookings:
            if lockerBooking.email == email:
                price = float(lockerBooking.total_price) if lockerBooking.total_price is not None else 0
                total_cost += price
        return total_cost

    def float_addition(self,numbers):
        total=0
        index=0
        for number in numbers:
            total+=float(number)
            index+=1
        if index==0: 
            index=1 
        average=float(total/index)
        if average==0:
            index=0
        return total,index,average


gymMember=GymMember()
# @frappe.whitelist(allow_guest=True)
# def calculate_days():
#     remaining_days = gymMember.calculateDays()
#     return remaining_days

@frappe.whitelist(allow_guest=True)
def check_email(email):
    # Check if the email exists in the system
    exists = gymMember.validateEmail(email)
    return exists

@frappe.whitelist(allow_guest=True)
def expiry(membership,membership_date):
   
    remaining= gymMember.calculateDays(membership,membership_date)
    return remaining

@frappe.whitelist(allow_guest=True)
def trainer(workout):
    # Check the trainer for a specific plan
    trainer= gymMember.trainers(workout)
    return trainer

@frappe.whitelist(allow_guest=True)
def subscription(type):
    price= gymMember.membershipCost(type)
    # rise=print(type(price)) 
    return price

@frappe.whitelist(allow_guest=True)
def lockerCharges(email):
    lockerBookings=frappe.db.get_all('Gym Locker Booking',{'parent':email}, ['email','total_price'])
    numbers=[]
    for lockerBooking in lockerBookings:
        numbers.append(lockerBooking.total_price)
    total=gymMember.float_addition(numbers)
    return total[0]

@frappe.whitelist(allow_guest=True)
def totalCharges(member_ship_cost, subscribed_workout_cost, locker_charges):
    numbers = [member_ship_cost, subscribed_workout_cost, locker_charges]
    total = gymMember.float_addition(numbers)
    return total[0]

@frappe.whitelist(allow_guest=True)
def totalRating(trainer):
    ratings=frappe.db.get_all('Trainer Ratings',{'trainer_name':trainer},['trainer_name','rating'])
    numbers=[]
    for rating in ratings:
        numbers.append(rating.rating)
    total=gymMember.float_addition(numbers)
    totalRatings=total[1]
    average=total[2]
    query = f"""
            UPDATE `tabGym Trainer`
            SET total_ratings="{totalRatings}",
             average_ratings="{average}"
            WHERE full_name= "{trainer}";
        """

    frappe.db.sql(query)
    frappe.db.commit()
    return 






@frappe.whitelist(allow_guest=True)
def availabilityUpdate(occupant):
    email=occupant
    details=frappe.db.get_all('Gym Locker Booking',{'parent':occupant,},{'book_end_date','end_time','name'})
    details=frappe.db.get_all('Cardio Machine Booking',{'parent':email},{'start_time','end_time','machine_name'})
    

    for detail in details:

        date1=detail.book_end_date
        date2=detail.end_time
        name=detail.name
        date=None
        if date1:
            date=date1
        else:
            date=date2

        query = f"""
            UPDATE `tabGym Lockers`
            SET status = 'Occupied',
             next_available_date="{date}",
             occupant="{occupant}"
            WHERE name = "{name}";
        """

        frappe.db.sql(query)
    #This is for updating the cardio machine booking details
   
    for detail in details:
        machine=detail.machine_name
        if detail.end_time:
            end_time=detail.end_time
        else:
            end_time=None
           
        query = f"""
            UPDATE `tabGym Cardio Machines`
            SET current_status = 'In Use',
             next_available_time="{end_time}",
             assigned_user="{email}"
            WHERE name= "{machine}";
        """

        frappe.db.sql(query)
    frappe.db.commit()


    return 

@frappe.whitelist(allow_guest=True)
def availabilityReset():
    lockers = frappe.get_all('Gym Lockers',{},{'name', 'status', 'occupant', 'next_available_date'})
    # print(lockers)

    for locker in lockers:
        name = locker.name
        exists = frappe.db.exists('Gym Locker Booking', {'locker_number': name})

        if not exists:
            
            query = f"""
                UPDATE `tabGym Lockers`
                SET status = 'Available',
                    occupant=NULL,
                next_available_date=NULL
                WHERE name = "{name}";
            """

            frappe.db.sql(query)
            
    frappe.db.commit()
    return






@frappe.whitelist(allow_guest=True)
def availablePlans(parent='Fitness'):
    gymPlans = frappe.db.get_all('Gym Work Out Plans', {'parent': parent}, ['name', 'duration', 'requirements', 'trainer','price'])
    plans = []
    for gymPlan in gymPlans:
        plan_details = gymPlan['name'] + "   Trainer: " + gymPlan['trainer'] + " Duration: " + str(gymPlan['duration']) + " Price: " + str(gymPlan['price']) +"    "
        plans.append(plan_details)
    return plans


@frappe.whitelist(allow_guest=True)
def resetBookings():
    lockers = frappe.db.get_all('Gym Lockers', {}, ['name', 'status', 'occupant', 'next_available_date'])
    exists_list = []
    for locker in lockers:
        name = locker.name
        exists = frappe.db.exists('Gym Locker Booking', {'name': name})
        exists_list.append((name, exists))  # Storing the result for each locker
    return exists_list



#This is a class for doctype Gym Locker Bookings:

class GymLockerBooking():
    def __init__(self):
        self.members = frappe.db.get_all('Gym Member', {}, ['full_name', 'gender', 'email', 'membership_type'])
        self.lockers = frappe.db.get_all('Gym Lockers', {}, ['locker_number', 'status'])
        

    def habitant(self,email,name):
        #name='h'
        for member in self.members:
            if email==member.email:
                email=member.email 
                name=member.full_name
        return name
    
    def bookEndDate(self,startDate_str,number_of_days):
        startDate= getdate(startDate_str)

        today = datetime.now()
        duration=int(number_of_days)
        endDate = startDate + timedelta(days=duration)
            
        return endDate
    
    def calculate_hour_difference(self,start_time_str,end_time_str):
        # Convert the original date string to a datetime object
        start_time_str = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")

        # Format the datetime object in the desired format
        start_time_str= start_time_str.strftime("%d-%m-%Y %H:%M:%S")
        print(f"\n\n{start_time_str}\n\n\n")
        # Convert the original date string to a datetime object
        end_time_str = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

        # Format the datetime object in the desired format
        end_time_str= end_time_str.strftime("%d-%m-%Y %H:%M:%S")
        print(f"\n\n{end_time_str}\n\n\n")

        start_time = datetime.strptime(start_time_str, "%d-%m-%Y %H:%M:%S")
        end_time = datetime.strptime(end_time_str, "%d-%m-%Y %H:%M:%S")
        
        # Calculate the difference
        time_difference = end_time - start_time
        
        # Convert the difference to hours
        hours_difference = time_difference.total_seconds() / 3600
    
        return hours_difference
    
   
       
         
   

locker = GymLockerBooking()
@frappe.whitelist(allow_guest=True)
def booking(email):

    return email

@frappe.whitelist(allow_guest=True)
def check_locker_number(locker_number):
    exists = frappe.db.exists('Gym Locker Booking', {'locker_number': locker_number})
    return exists

    

@frappe.whitelist(allow_guest=True)
def endDate(startDate_str,number_of_days):
    endDate = locker.bookEndDate(startDate_str,number_of_days)
    number_of_days=int(number_of_days)
    unitPrice=30
    totalPrice=number_of_days*unitPrice
    return endDate, totalPrice

@frappe.whitelist(allow_guest=True)
def totalHours(start_time_str,end_time_str):

    hours_difference=locker.calculate_hour_difference(start_time_str,end_time_str)
    hours_difference=int(hours_difference)
    total_price=hours_difference*2.0
    total_price=int(total_price)
    return hours_difference,total_price    







@frappe.whitelist(allow_guest=True)
def check_machine_name(machine_name):
    exists = frappe.db.exists('Cardio Machine Booking', {'name': machine_name})
    return exists


@frappe.whitelist(allow_guest=True)
def machineAvailabilityUpdate():
    machines = frappe.get_all('Gym Cardio Machines',{},{'machine_name', 'current_status','assigned_user', 'next_available_time'})
    for machine in machines:
        name=machine.machine_name
        exists = frappe.db.exists('Cardio Machine Booking', {'machine_name':name})

        if not exists:
            
            query = f"""
                UPDATE `tabGym Cardio Machines`
                SET current_status = 'Available',
                    assigned_user=NULL,
                next_available_time=NULL
                WHERE machine_name = "{name}";
            """

            frappe.db.sql(query)
            
    frappe.db.commit()

    return


# @frappe.whitelist(allow_guest=True)
# def cardioMachineAvailability(email):
#     details=frappe.db.get_all('Cardio Machine Booking',{'parent':email},{'start_time','end_time','machine_name'})

    
   
#     for detail in details:

#         machine=detail.machine_name
#         if detail.end_time:
#             end_time=detail.end_time
#         else:
#             end_time=None
           
#         query = f"""
#             UPDATE `tabGym Cardio Machines`
#             SET current_status = 'In Use',
#              next_available_time="{end_time}",
#              assigned_user="{email}"
#             WHERE name= "{machine}";
#         """

#         frappe.db.sql(query)
#     frappe.db.commit()
#     return 




#  Gym Trainer Doc
def ratings():
    ratings=frappe.db.get_all('Trainer Ratings',{},['trainer_name','rating'])

