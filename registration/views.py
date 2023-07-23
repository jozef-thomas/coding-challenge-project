import requests
from django.shortcuts import render, redirect
from .forms import RegistrationForm
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from bs4 import BeautifulSoup
from .models import UpdateForm


def home(request):
    if request.method == 'POST':
            name = request.POST.get('prereg_name')
            email = request.POST.get('prereg_email')
            mob = request.POST.get('prereg_mob')
            district = request.POST.get('districtd')

            url = "https://dev.yip.kerala.gov.in/yipapp/index.php/Idea2021/add_pre_reg"

            data = {
                "prereg_name": name,
                "prereg_email": email,
                "prereg_mob": mob,
                "districtd": district,
            }
            
             
            response = requests.post(url, data=data)
            print("Response Data:")
            print(response.text)
            data = response.json()
            if 'Success' in data:
                success_value = data["Success"]
                print(success_value)
                print(type(success_value))
                if success_value == '1': 
                    message = "OTP Send To The Registered Mobile Number"
                    context = {
                    "user_id": email,
                    "prereg_name": name,
                    "prereg_email": email,
                    "prereg_mob": mob,
                    "districtd": district,
                    "message" : message,
                #"note": note,
            }
                    print("Response Data:")
                    print(response.text)
                    return render(request, 'registration/otptest.html',context)
                
                if success_value == '5':
                    alert_message = "Some Error Occured...Please Try Again..."
                    return render(request, 'registration/registration.html',{'alert_message': alert_message})
            
            if 'validation' in data:
                validation_value = data["validation"]
                print(validation_value)
                print(type(validation_value)) 
                
                
                if validation_value == False:
                    error_msg = data["error_msg"]
                    print("error_msg")
                    print(error_msg)
                    email_error_html = error_msg['prereg_email']
                    # Parse the HTML using BeautifulSoup
                    soup = BeautifulSoup(email_error_html, 'html.parser')
                    # Find the label tag and extract its contents (the error message)
                    label_tag = soup.find('label')
                    error_message = label_tag.get_text(strip=True) if label_tag else None
                    print(error_message)
            
                if error_message == 'Mail Id already exist': 
                    # Handle error if needed
                    validation_message = "User Already Exists...Please Login"
                    return render(request, 'login/login.html', {'validation_message': validation_message})
                else:
                    alert_message = "Some Error Occured...Please Try Again..."
                    return render(request, 'registration/registration.html',{'alert_message': alert_message})
            
    
               
    else:
        return render(request, 'registration/registration.html')



#function for otp verification

def otp(request):
    if request.method == 'POST':
        d1 = request.POST.get('d1')
        d2 = request.POST.get('d2')
        d3 = request.POST.get('d3')
        d4 = request.POST.get('d4')
        d5 = request.POST.get('d5')
        d6 = request.POST.get('d6')
        print(d1,d2,d3,d4,d5,d6)
        combined_otp = (d1+d2+d3+d4+d5+d6)
        otp_code = combined_otp
        userid = request.POST.get('user_id')
        name = request.POST.get('prereg_name')
        email = request.POST.get('prereg_email')
        mob = request.POST.get('prereg_mob')
        district = request.POST.get('districtd')

        url = " https://dev.yip.kerala.gov.in/yipapp/index.php/Com_mobile_otp/checkotp"
        print(name)
        print(userid)
        data = {
                "otp_received":otp_code,
                "user_id":userid,
                "prereg_name": name,
                "prereg_email": email,
                "prereg_mob": mob,
                "districtd": district,
        }
        
        response = requests.post(url, data=data)
        print("Response Data:")
        print(response.text)
        data = response.json()
        success_value = data["Success"]
        print("Success Value:", success_value)
            # Check if the POST request was successful and handle accordingly
        if success_value == "1":
            password=""
            for x in range(0,6):
                password+=str(random.randint(0,9))
            #concatenate userid and password
            email_content = f"User ID: {userid}\nPassword: {password}"
            print(email_content)
            #request.session['user_id'] = userid
            #request.session['password'] = password
            User.objects.create_user(username=userid, password=password)
            send_mail("YIP User ID and Password",email_content,'jzftestmail@gmail.com',[userid])
            print("User Id and Password Send Successfully")

            #api for login
            """url = " https://dev.yip.kerala.gov.in/yipapp/index.php/init/login/1"

            data = {
                "user": "joseph@gmail.com",
                "pass": 123456,
                "feedbackval": 1,
            }

            response = requests.post(url, data=data)
            print("Response Data:")
            print(response.text) """
            #success_message = "User ID and Password send to the registered email..."
            message = "Registration Details Successfully Saved.Login Credentials shared to your registered Email ID.Now you can continue to complete the registration"
            context = {
                'message': message,
            }
            return render(request, 'login/login.html',context)
        else:
                error_message = "Wrong OTP. Please try again."
                # Error Handling
                context = {
                "user_id": email,
                "prereg_name": name,
                "prereg_email": email,
                "prereg_mob": mob,
                "districtd": district,
                "error_message": error_message
            }
               
                return render(request,'registration/otptest.html',context)
    else:
         
        #all_users = User.objects.all()
        #return render(request, 'login/user_list.html', {'all_users': all_users})
        #return render(request, 'login/login.html',context)
        return render(request, 'registration/registration.html')

            
    



#Login Authentication Function
def login(request):
    if request.method == 'POST':
        u_id = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=u_id, password=password)
        if user is not None:
    # User authentication successful
            print("Success")
            return render(request, 'updation/update.html')
        else:
    # User authentication failed
            print("Failed")
            validation_message = "Incorrect Username or Password.....Please Try Again"
            return render(request, 'login/login.html',{'validation_message': validation_message})

    else:
        return render(request,'login/login.html')
    
    
    
#Function for Form Updation
def updateform(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        district = request.POST.get('district')

        # Manually validate the data (you can add more complex validation logic)
        if not all([name, email, mobile_number, district]):
            return render(request, 'updation/update.html', {'error_message': 'Please fill in all the fields.'})

        if len(mobile_number) != 10 or not mobile_number.isdigit():
            return render(request, 'updation/update.html', {'error_message': 'Invalid mobile number.'})

        # Save the data to the database
        UpdateForm.objects.create(name=name, email=email, mobile_number=mobile_number, district=district)

        # Redirect to a success page after successful submission
        return redirect('home')

    else:
        return render(request,'login/login.html')
    
    


def otptest(request):
    if request.method == 'POST':

        
        
        
        """d1 = request.POST.get('d1')
        d2 = request.POST.get('d2')
        d3 = request.POST.get('d3')
        d4 = request.POST.get('d4')
        d5 = request.POST.get('d5')
        d6 = request.POST.get('d6')
        print(d1,d2,d3,d4,d5,d6)
        combined_otp = (d1+d2+d3+d4+d5+d6)
        print(combined_otp)"""
        return render(request,'updation/update.html')
    

    else:
        return render(request,'updation/update.html')
    
        
    
    


