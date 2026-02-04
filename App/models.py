from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.db.models.functions import ExtractMonth

gender_choices=[('M','Male'),('F','Female'),('O','other')]
status_choice=[('Active','Active'),('Inactive','Inactive')]
choice=[('Pending','Pending'),('Completed','Completed'),('InProgress','InProgress')]
# Create your models here.
class Employee(models.Model):
    Emp_id=models.AutoField(primary_key=True)
    F_name=models.CharField(max_length=50)
    L_name=models.CharField(max_length=50)
    Address=models.CharField(max_length=155)
    Contact_no=models.CharField(max_length=15)
    Email=models.EmailField(max_length=50,unique=True)
    Gender=models.CharField(max_length=10,choices=gender_choices)
    Emp_type=models.CharField(max_length=30)
    status=models.CharField(max_length=20,choices=status_choice)
    Dob=models.DateField()
    doj=models.DateField()
    Designation=models.CharField(max_length=255)
    Department=models.CharField(max_length=30)
    Password = models.CharField(max_length=255)
    Salary=models.DecimalField(max_digits=10,decimal_places=2,null=True,default=0.00)
    def check_password(self, raw_password):
        return check_password(raw_password, self.Password)
    

class Department(models.Model):
    dept_id=models.AutoField(primary_key=True)
    dept_name=models.CharField(max_length=50)
    Manager_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    status=models.CharField(max_length=15,choices=status_choice)

class Salary(models.Model):
    salary_id=models.AutoField(primary_key=True)
    emp_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    pay_date=models.DateField()
    Basic_salary=models.DecimalField(max_digits=10,decimal_places=2)
    Bonus=models.DecimalField(max_digits=10,decimal_places=2)
    Deduction=models.DecimalField(max_digits=10,decimal_places=2)
    net_salary=models.DecimalField(max_digits=10,decimal_places=2,editable=False)
    # pay_date=models.DateField()
    status=models.CharField(max_length=15,choices=status_choice)
    def save(self,*args,**kwargs):
        self.net_salary=self.Basic_salary + self.Bonus - self.Deduction
        super().save(*args,**kwargs)


class Designation(models.Model):
    designation_id=models.AutoField(primary_key=True)
    designation_name=models.CharField(max_length=50)
    dept_id=models.ForeignKey(Department,on_delete=models.CASCADE)

class Task(models.Model):
    task_id=models.AutoField(primary_key=True)
    task_title=models.CharField(max_length=100,null=False)
    description=models.CharField(max_length=255,null=False)
    status=models.CharField(max_length=20,default='Pending',choices=choice)
    Emp_id=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='tasks')
    manager=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='assigned_tasks')
    start_date=models.DateField()
    due_date=models.DateField()
    completed_date=models.DateField(null=True,blank=True)
    remark=models.CharField(max_length=255)

# from django.db import models

class monthly_attendance(models.Model):
    Emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='mn_attendance')
    date = models.DateField()
    status = models.CharField(max_length=20)  # Present / Absent
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)


class attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    Emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance")
    
    month = models.DateField()  # store 1st day of month
    Present_days = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)
    leave_days = models.IntegerField(default=0)
    Total_days = models.IntegerField(default=0)


class leave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    Emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave")
    leave_type = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)  # Pending / Approved
    Total_days = models.IntegerField()

class performance(models.Model):
    p_id=models.AutoField(primary_key=True)
    Emp_id=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="performance")
    Attendance_id=models.ForeignKey(attendance,on_delete=models.CASCADE,related_name="attendance")
    task_id=models.ForeignKey(Task,on_delete=models.CASCADE,related_name="task")
    manager_id=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="emp")
    reviewd_date=models.DateField()




    







