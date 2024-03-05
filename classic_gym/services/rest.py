import frappe
from datetime import datetime, timedelta,time
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
        total = sum(float(number) for number in numbers)  # Calculate the total directly using sum()
        index = len(numbers)  # Calculate the length of the numbers list
        if index == 0:
            index = 1  # Ensure index is not zero to avoid division by zero
        average = total / index if total != 0 else 0  # Calculate average, handling zero division case
        return total,  average



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
def calculate_age(dateOfBirth):
    current_date = datetime.now()
    if datetime.strptime(dateOfBirth, "%Y-%m-%d"):
        dob = datetime.strptime(dateOfBirth, "%Y-%m-%d")
        
        age = current_date - dob
        age = age.days // 365
    
        return age

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
    ratings=frappe.db.get_all('Trainer Ratings',{'trainer_name':trainer},{'trainer_name','rating'})
    numbers = [rating.rating for rating in ratings]
   
    total=gymMember.float_addition(numbers)
    index = len(numbers) if numbers else 0
    average=total[1]
    query = f"""
            UPDATE `tabGym Trainer`
            SET total_ratings="{index}",
             average_ratings="{average}"
            WHERE full_name= "{trainer}";
        """

    frappe.db.sql(query)
    frappe.db.commit()
    return


@frappe.whitelist(allow_guest=True)
def check_locker_number(locker_number):
    details=frappe.db.get_all('Gym Locker Booking',{'locker_number':locker_number},{'book_date','start_time','book_end_date','end_time','name'})
    exist=None
    for detail in details:
        name=detail.name

        book_date=detail.book_date if detail.book_date else None
        if book_date:
            book_date = datetime.strptime(str(book_date), '%Y-%m-%d').date()
            book_date = datetime.combine(book_date, datetime.min.time())

        start=detail.start_time if detail.start_time else None
        start_time=book_date if book_date else start
        
        book_end_date=detail.book_end_date if detail.book_end_date else None
        if book_end_date:
            book_end_date = datetime.strptime(str(book_end_date), '%Y-%m-%d').date()
            book_end_date = datetime.combine(book_end_date, datetime.min.time())
        end_time=detail.end_time if detail.end_time else None
        stop_time=book_end_date if book_end_date else end_time
    
        today = datetime.now()
        future = ( stop_time-today).total_seconds() if stop_time else float('inf')
        past  = (start_time-today).total_seconds()  if start_time else float('inf')

        if future >0 and past <0:
            exist=locker_number
        else:
            exist=None

   
    return exist








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
def endDate(startDate_str,number_of_days):
    endDate = locker.bookEndDate(startDate_str,number_of_days)
    number_of_days=int(number_of_days)
    unitPrice=30
    totalPrice=number_of_days*unitPrice
    return endDate, totalPrice

@frappe.whitelist(allow_guest=True)
def totalHours(start_time_str,end_time_str):
    if start_time_str and end_time_str:

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
def machineAvailabilityReset():
    machines = frappe.get_all('Gym Cardio Machines',{},{'machine_name', 'current_status','assigned_user', 'next_available_time'})
    for machine in machines:
        machine_name=machine.machine_name
        exist = frappe.db.exists('Cardio Machine Booking', {'machine_name':machine_name})
        if machine.next_available_time:
            machine.next_available_time= machine.next_available_time.strip()
            machine.next_available_time=datetime.strptime(machine.next_available_time,'%Y-%m-%d %H:%M:%S')
            future = (machine.next_available_time-datetime.now()).total_seconds()
        else:
            future=0
            
        checks=frappe.db.get_all('Cardio Machine Booking',{'machine_name':machine_name},{'stop_time'})
        exist2=0
        for check in checks:
            if check.stop_time==machine.next_available_time:
                exist2=1

        if not exist or exist2==0 or future<0:                   
            
            query = f"""
                UPDATE `tabGym Cardio Machines`
                SET current_status = 'Available',
                    assigned_user=NULL,
                next_available_time=NULL
                WHERE machine_name = "{machine_name}";
            """

            frappe.db.sql(query)

    frappe.db.commit()

    return

@frappe.whitelist(allow_guest=True)
def weight(email):
    today = datetime.now()
    
    return email,today

@frappe.whitelist(allow_guest=True)
def machineAvailabity(email):
    machines=frappe.db.get_all('Cardio Machine Booking',{'parent':email},{'start_time','stop_time','machine_name'})

    for machine in machines:
        machine_name = machine.machine_name
        start_time=machine.start_time if machine.start_time else datetime.now
        stop_time= machine.stop_time if machine.stop_time else datetime.now

        future =(stop_time -datetime.now()).total_seconds()
        past=(start_time-datetime.now()).total_seconds()

  
        if future >0 and past <0:
            
            query = f"""
                                UPDATE `tabGym Cardio Machines`
                                SET current_status = 'In Use',
                                next_available_time =" {stop_time}",
                                assigned_user = "{email}"
                                WHERE machine_name = "{machine_name}";
                            """

            frappe.db.sql(query)
    
    frappe.db.commit()
    return 


@frappe.whitelist(allow_guest=True)
def lockerAvailability(email):

    details=frappe.db.get_all('Gym Locker Booking',{'parent':email,},{'book_date','start_time','book_end_date','end_time','locker_number'})
    message=[]
    for detail in details:
        locker_number=detail.locker_number

        if detail.book_date:
            detail.book_date = datetime.strptime(str(detail.book_date), '%Y-%m-%d').date()
            detail.book_date = datetime.combine(detail.book_date, datetime.min.time())

        start_time=detail.book_date if detail.book_date else detail.start_time

        if detail.book_end_date:
            detail.book_end_date = datetime.strptime(str(detail.book_end_date), '%Y-%m-%d').date()
            detail.book_end_date = datetime.combine(detail.book_end_date, datetime.min.time())
      
        stop_time=detail.book_end_date if detail.book_end_date else detail.end_time


        future = ( stop_time-datetime.now()).total_seconds()
        past  = (start_time-datetime.now()).total_seconds() 
        if future>0 and past<0:
            query = f"""
                    UPDATE `tabGym Lockers`
                    SET status = 'Occupied',
                    next_available_date="{stop_time}",
                    occupant="{email}"
                    WHERE name = "{locker_number}";
                """

            frappe.db.sql(query)
    frappe.db.commit()
    return 

@frappe.whitelist(allow_guest=True)
def lockerAvailabilityReset():
    # lockers = frappe.get_all('Gym Lockers', {}, {'name', 'status', 'occupant', 'next_available_date'})
    # for locker in lockers:
    #     locker_number = locker.name
    #     exists = frappe.db.exists('Gym Locker Booking', {'locker_number': locker_number})

       
    machines = frappe.get_all('Gym Cardio Machines',{},{'machine_name', 'current_status','assigned_user', 'next_available_time'})
    lockers = frappe.get_all('Gym Lockers', {}, {'name', 'status', 'occupant', 'next_available_date'})
    detail=[]
    future=0
    sure=False
    for locker in lockers:
        locker_number=locker.name
        check_bookings= frappe.db.exists('Gym Locker Booking', {'locker_number': locker_number})
        if check_bookings and locker.next_available_date:
            available=locker.next_available_date.strip()
            available=datetime.strptime(locker.next_available_date,'%Y-%m-%d %H:%M:%S')
            future=(available-datetime.now()).total_seconds()

            checks=frappe.db.get_all('Gym Locker Booking',{'locker_number':locker_number},{'book_end_date','end_time'})
            for check in checks:
                date=check.book_end_date if check.book_end_date else check.end_time

                if check.book_end_date:
                    date=datetime.combine(date, time.min)
                if date==available:
                    sure=True
        
        if not check_bookings or future<0 or not sure:
            query = f"""
                    UPDATE `tabGym Lockers`
                    SET status = 'Available',
                    next_available_date=NULL,
                    occupant=NULL
                    WHERE name = "{locker_number}";
                """

            frappe.db.sql(query)
    frappe.db.commit()


    return 