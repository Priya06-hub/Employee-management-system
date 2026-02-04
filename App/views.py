from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.hashers import make_password,check_password
from .models import Employee,Task,monthly_attendance,attendance,performance,Salary,leave
from .forms import Emp_form,Emp_edit_form
from django.contrib import admin
from datetime import date
from django.utils import timezone
import random
from datetime import datetime
from django.core.mail import send_mail
import ems.settings
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect

admin.site.register(Employee)
def index(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def features(request):
    return render(request, 'features.html')
def contact(request):
    return render(request, 'contact.html')
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def emp_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'Emp_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def mark_absent(request):
    today = timezone.now().date()
    employees = Employee.objects.all()

    for emp in employees:
        attendance_exists = monthly_attendance.objects.filter(
            Emp_id=emp,
            date=today
        ).exists()

        if not attendance_exists:
            monthly_attendance.objects.create(
                Emp_id=emp,
                date=today,
                status='ABSENT',
                check_in=None,
                check_out=None
            )
from django.shortcuts import render, get_object_or_404, redirect
from .models import monthly_attendance

def modify_att(request):
    attendance = None
    message = ""
    
    # 1️⃣ HR first searches Emp ID + Date
    if request.method == 'POST' and 'search' in request.POST:
        emp_id = request.POST.get('emp_id')
        date = request.POST.get('date')
        try:
            attendance = monthly_attendance.objects.get(Emp_id_id=emp_id, date=date)
        except monthly_attendance.DoesNotExist:
            message = "No attendance found for this employee on this date."
    elif request.method == 'POST' and 'update' in request.POST:
        attendance_id = request.POST.get('attendance_id')
        attendance = get_object_or_404(monthly_attendance, id=attendance_id)
        attendance.check_in = request.POST.get("check_in")
        attendance.check_out = request.POST.get("check_out")
        attendance.status = request.POST.get("status")
        attendance.save()
        message = "Attendance updated successfully!"

    return render(request, 'modify_attendance.html', {
        'attendance': attendance,
        'message': message
    })

def login_view(request):
    if request.method == "POST":
        emp_id = request.POST.get('empid')
        pwd = request.POST.get('pwd')

        # ---------------- ADMIN LOGIN (auth_user table) ----------------
        user = authenticate(request, username=emp_id, password=pwd)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')

        # ---------------- EMP / MANAGER / HR LOGIN (Employee table) ----------------
        try:
            emp = Employee.objects.get(
                Emp_id=emp_id,
                status='Active'
            )
        except Employee.DoesNotExist:
            return render(request, 'login.html', {
                'error': 'Invalid emp id or inactive account'
            })

        # Check password
        if not check_password(pwd, emp.Password):
            return render(request, 'login.html', {
                'error': 'Invalid credentials'
            })

        # Store session
        request.session['Emp_id'] = emp.Emp_id
        request.session['role'] = emp.Designation
        mark_absent(request)

        # ---------------- ROLE BASED REDIRECTION ----------------
        print(emp.Emp_id,emp.Designation)
        if emp.Designation == 'Employee':
            return redirect('emp_dashboard')

        elif emp.Designation == 'Manager':
            return redirect('manager_dashboard')

        elif emp.Designation == 'HR':
            return redirect('hr_dashboard')

        else:
            return render(request, 'login.html', {
                'error': 'Unauthorized role'})



    return render(request, 'login.html')

@login_required
def create_profile(request):
    # if request.user.is_superuser:
    if request.method=='POST':
            f_name=request.POST['f_name']
            l_name=request.POST['l_name']
            address=request.POST['address']
            email=request.POST['mail']
            contact_no=request.POST['contact']
            Gender=request.POST['gender']
            status=request.POST['status']
            dob=request.POST['dob']
            doj=request.POST['doj']
            designation=request.POST['des']
            department=request.POST['dep']
            Salary=request.POST['sal']
            emp_type=request.POST['emp_type']
            raw_pwd=request.POST['pwd']
            emp=Employee(
                F_name=f_name,
                L_name=l_name,
                Address=address,
                Contact_no=contact_no,
                Email=email,
                Gender=Gender,
                Emp_type=emp_type,
                status=status,
                Dob=dob,
                doj=doj,
                Designation=designation,
                Department=department,
                salary=Salary,
                Password=make_password(raw_pwd)
            )
            emp.save()
            
        # Send email
            send_mail(
                subject="Your Employee Login Credentials",
                message=f"""
                Hello {emp.F_name},

                Your employee account has been created.

                Employee ID: {emp.Emp_id}
                Password: {raw_pwd}

                Please login and change your password after first login.

                Regards,
                Admin Team
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[emp.Email],
                fail_silently=False
            )

            print("Profile created successfully")
            return redirect('admin_dashboard')
        
            # else:
            # return redirect('login')
    
    return render(request,'create_profile.html',{'success':'Profile created successfully'})
   

def forgot_password(request):
    if request.method == "POST":
        emp_id = request.POST.get('emp_id')
        email = request.POST.get('email')

        otp=random.randint(100000,900000)
        otp=str(otp)
        print(otp)

        try:
            emp = Employee.objects.get(Emp_id=emp_id, Email=email)
            request.session["reset_otp"]=otp
            request.session["reset_email"]=emp.Email
            request.session.set_expiry(120)
                    # redirect to reset password page
            send_mail(
                subject="RESET PASSWORD",
                message=f"""
                you requested to reset your pasword.

                otp: {otp}

                if you did not request this , please ignore this email.

                Regards,
                Admin Team
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[emp.Email],
                fail_silently=False
            )

            return redirect('verify_otp')
        except Employee.DoesNotExist:
            return render(request, 'forgot_password.html', {
                'error': 'Invalid User ID or Email'
            })
        
    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        confirm_pwd=request.POST.get("con_pwd")

        session_otp = request.session.get("reset_otp")
        email = request.session.get("reset_email")

        if not session_otp or not email:
            return render(request, "verify_otp.html", {
                "error": "OTP expired"
            })

        if entered_otp != session_otp:
            return render(request, "verify_otp.html", {
                "error": "Invalid OTP"
            })
        
        if confirm_pwd != new_password:
            return render(request,"verify_otp.html",{
                "error": "not match the new password and confirm password"
            })
        
        emp = Employee.objects.get(Email=email)
        emp.Password=make_password(new_password)
        emp.save()
        # user.set_password(new_password)
        # user.save()

        del request.session["reset_otp"]
        del request.session["reset_email"]

        return redirect("login")

    return render(request, "verify_otp.html")

@emp_login_required
def change_password(request):
    emp_id = request.session.get('Emp_id')
    if not emp_id:
        return redirect('login')

    employee = get_object_or_404(Employee, Emp_id=emp_id)

    if request.method == "POST":
        old_password = request.POST.get('old_pwd')
        new_password = request.POST.get('new_pwd')
        confirm_password = request.POST.get('con_pwd')

        if not check_password(old_password, employee.Password):
            return render(request, 'change_password.html', {
                'error': 'Old password is incorrect'
            })

        if new_password != confirm_password:
            return render(request, 'change_password.html', {
                'error': 'New password and confirm password do not match'
            })

        employee.Password = make_password(new_password)
        employee.save()
        return redirect('login')
    return render(request, 'change_password.html')

@emp_login_required
def apply_leave(request):
    emp_id=request.session.get("Emp_id")
    employee=Employee.objects.get(Emp_id=emp_id)
        # emp_id = request.POST.get("emp_id")
    if request.method == "POST":
        leave_type = request.POST.get("leave_type")
        current_month = date.today().replace(day=1)
        start_date = request.POST.get("start")
        end_date = request.POST.get("end")
        # leave_days = att.leave_days if att else 0
        # present_days = att.Present_days if att else 0
        # absent_days = att.absent_days if att else 0
        # total_days = att.Total_days if att else 0
        att = attendance.objects.filter(
        Emp_id=employee,
        month=current_month
        ).first()

        emp = Employee.objects.get(Emp_id=emp_id)

        # calculate total days
        sd = datetime.strptime(start_date, "%Y-%m-%d").date()
        ed = datetime.strptime(end_date, "%Y-%m-%d").date()
        total_days = (ed - sd).days + 1

        leave.objects.create(
            Emp_id=employee,
            leave_type=leave_type,
            start_date=sd,
            end_date=ed,
            status="Pending",
            Total_days=total_days
        )
        # return redirect("manager_dashboard")
        return redirect("leave_list")  

    return render(request, "apply_leave.html",{'employee':employee})
        # 'present_days': present_days,
        # 'absent_days': absent_days, 

def leave_list(request):
    # emp=Employee.objects.all(emp_id=Emp_id)
    leaves = leave.objects.all()
    return render(request, 'leave_approval.html', {'leaves': leaves})

@emp_login_required
def add_daily_attendance(request):
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        status = request.POST.get("status")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        emp = Employee.objects.get(id=emp_id)

        monthly_attendance.objects.create(
            Emp_id=emp,
            date=date.today(),
            status=status,
            check_in=check_in,
            check_out=check_out
        )

        # 👆 YAHI PAR SIGNAL AUTO CALL HO JATA HAI

        return redirect("attendance_list")

    return render(request, "add_attendance.html")

@emp_login_required
def mn_attendance(request):
    emp_id=request.session.get('Emp_id')
    records=monthly_attendance.objects.filter(Emp_id=emp_id)
    today = date.today()
    current_month = today.month
    current_year = today.year

    attendance_data = attendance.objects.filter(
        Emp_id__Emp_id=emp_id,
        month__month=current_month,
        month__year=current_year
    )

    return render(request, 'mn_attendance.html',{'records':records})

# from django.shortcuts import get_object_or_404

# from django.shortcuts import get_object_or_404, render
# from .models import leave

@emp_login_required
def mark_attendance(request):
    # emp = request.user.Employee 
    # if request.method !="POST":
        # return {'error':'Invalid request method'}

    session_emp_id = request.session.get('Emp_id')
    emp = get_object_or_404(Employee, Emp_id=session_emp_id)
    today = date.today()
    now_time = timezone.localtime().time()

    att, created = monthly_attendance.objects.get_or_create(
        Emp_id=emp,
        date=today,
        defaults={
            'check_in': now_time,
            'status': 'Present'
        }
    )
    return render(request,'mark_attendance.html')

def leave_approval(request, leave_id):
    lv = get_object_or_404(leave, leave_id=leave_id)

    if request.method == "POST":
        action = request.POST.get('action')

        if action == "approve":
            lv.status = "Approved"
        elif action == "reject":
            lv.status = "Rejected"
        elif action == "Update":
            if action == "approve":
                lv.status = "Approved"
            elif action == "reject":
                lv.status = "Rejected"


        lv.save()
        
        return redirect('leave_list')

    # return render(request, 'leave_approval.html', {'leave': lv})



def mn_leave(request):
    session_emp_id=request.session.get('emp_id')
    emp = Employee.objects.get()

    if request.method=="POST":
        leave_type=request.POST.get('leave_type')
        sd=request.POST.get('start')
        ed=request.POST.get('end')
        status=request.POST.get('status')

    

    return render(request,'mn_leave.html')
def mn_salary(request):
    return render(request,'mn_salary.html')



# @login_required
def manage_profile(request, emp_id=None):

    # ADMIN
    if request.user.is_superuser and emp_id:
        is_admin = True
        emp = get_object_or_404(Employee, Emp_id=emp_id)
        return render(request, 'admin_profile.html', {'employee': emp})

    # HR / MANAGER / EMPLOYEE
    session_emp_id = request.session.get('Emp_id')

    if not session_emp_id:
        return redirect('login')  # 🔐 session expired or invalid

    emp = Employee.objects.filter(Emp_id=session_emp_id).first()

    if not emp:
        return redirect('login')  # 🔐 no such employee


    if request.method == "POST":
            # ---------------- Personal info (editable by everyone) ----------------
            emp.F_name = request.POST.get('f_name')
            emp.L_name = request.POST.get('l_name')
            emp.Gender = request.POST.get('gender')
            emp.Emp_type = request.POST.get('emp_type')
            emp.Email = request.POST.get('email')
            emp.Contact_no = request.POST.get('phone')
            emp.Address = request.POST.get('address')
            emp.Dob = request.POST.get('dob')
            emp.doj = request.POST.get('doj')

            # ---------------- Official info (editable only by admin) ----------------
            if request.user.is_superuser:
                emp.Designation = request.POST.get('designation')
                emp.Department = request.POST.get('department')
                emp.Salary = request.POST.get('salary')
                emp.status = request.POST.get('status')

            emp.save()
            print("profile updated")
            return render(request,'manager_dashboard.html',{"succes":"YOUR PROFILE UPDATAED SUCCESSFULLY......"})

    return render(request, 'profile.html', {'employee': emp})

def mn_performance(request):
    return render(request,'mn_performance.html')
def mn_salary(request):
    return render(request,'mn_salary.html')
def emp_dashboard(request): 
    return render(request, 'emp_dashboard.html')
def manager_dashboard(request): 
    return render(request, 'manager_dashboard.html')
def hr_dashboard(request):
    return render(request, 'hr_dashboard.html')
def logout_view(request):
    logout(request)
    return redirect('home')
def task_list(request):
    # Show all tasks or manager-specific tasks
    tasks = Task.objects.filter(manager_id=request.session.get('Emp_id'))
    return render(request, 'task_list.html', {'tasks': tasks})
def mn_task(request):
    manager_id = request.session.get('Emp_id')
    if request.method == "POST":
        task_title = request.POST.get('task_title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        assign_date = request.POST.get('assign_date')
        remark = request.POST.get('remark')

        try:
            manager= Employee.objects.get(Emp_id=manager_id)
            assigned_to = Employee.objects.get(Emp_id=assigned_to_id)
            if manager.Department!= assigned_to.Department:
                messages.error(request, f"Cannot assign task. Employee '{assigned_to.F_name}' is in a different department.")
                employees = Employee.objects.all()
                return render(request, 'mn_tasks.html', {'employees': employees, 'error': f"Cannot assign task. Employee '{assigned_to.F_name}' is in a different department."})


            Task.objects.create(
                task_title=task_title,
                description=description,
                Emp_id=assigned_to,          # FK object
                due_date=due_date,
                manager_id=manager_id,      # FK id
                start_date=assign_date,
                remark=remark
            )

        
            return redirect('task_list')

        except Employee.DoesNotExist:
            return render(request, 'mn_tasks.html', {
                'error': 'Assigned employee does not exist.'
            })

    employees = Employee.objects.all()
    return render(request, 'mn_tasks.html', {'employees': employees})

def employee_task_list(request):
    emp_id = request.session.get('Emp_id')

    if not emp_id:
        messages.error(request, "Please login first.")
        return redirect('login')

    if request.method == "POST":
        task_id = request.POST.get('task_id')

        task = Task.objects.get(task_id=task_id, Emp_id_id=emp_id)
        # get_object_or_404(
        #     Task,
        #     task_id=task_id,
        #     Emp_id_id=emp_id   # security: only own task
        # )

        if task.status != "Completed":
            task.status = "Completed"
            task.completed_date = date.today()
            task.save()
            messages.success(request, "Task marked as completed.")

        return redirect('employee_task_list')

    # 📋 SHOW TASK LIST
    tasks = Task.objects.filter(Emp_id__Emp_id=emp_id)

    return render(request, 'emp_task_list.html', {'tasks': tasks})


# def assign_Task(request):
#     mng_id=request.session.get('Emp_id')
#     if request.method == "POST":
#         task_title = request.POST.get('task_title')
#         description = request.POST.get('description')
#         assigned_to_id = request.POST.get('assigned_to')
#         priority = request.POST.get('priority')
#         due_date = request.POST.get('due_date')
#         manager=mng_id
#         assign_date=request.POST.get('assign_date')
#         # due_date=request.POST.get('due_date')
#         complted_date=request.POST.get('com_date')
#         remark=request.POST.get('remark')

#         # Get the assigned employeeBN
#         assigned_to = Employee.objects.get(id=assigned_to_id)

#         # Create the task
#         Task.objects.create(
#             task_title=task_title,
#             description=description,
#             Emp_id_id=assigned_to,
#             priority=priority,
#             due_date=due_date,
#             manager_id=manager,
#             start_date=assign_date,
#             complted_date=complted_date,
#             remark=remark
#         )

#         # return redirect('task_list')  # Redirect to a task list page or any other page

#     employees = Employee.objects.all()  # Fetch all employees for the dropdown
#     return render(request, 'mn_tasks.html', {'employees': employees})