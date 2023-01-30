from rest_framework import serializers
from .models import Payment
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ('comission_value','created','updated')
    
    def validate_card_number(self,value):
        if len(str(value)) < 16:
            raise serializers.ValidationError("Enter at least 16 digits in the card number")

        list=[]   
        list2=[]
        for i in range(0,len(str(value))):
            list+=[value[i]]
            list2+='*'

        lastDigits=list[-4:]
        list2[-4:] = lastDigits

        # validate type card 
        if  list[0] != '3' and list[0] != '4' and list[0] != '5':
            '''
            3 = Diners
            4 = Visa
            5 = MasterCard
            '''
            raise serializers.ValidationError("Please enter a valid card type")  

        value = ''.join(list2)   

        # validate
        if Payment.objects.filter(card_number=value).exists():
            print("The card number already exists!")
            raise serializers.ValidationError("The card number already exists!")
   
                 
        return value    

    def validate_card_cvv(self,value):
        if len(str(value)) < 3:
            raise serializers.ValidationError("Enter at least 3 digits for the security code of the card")
        return value

    def validate_total_value(self,value):
        if value < 1000:
            raise serializers.ValidationError("The minimum value to pay is $1000")
        return value            

    def create(self,validated_data):
        payment = Payment(**validated_data)

        #storing the last 4 digits for security and replacing the previous ones with asterisks
        list=[]
        list2=[]
        
        for i in range(0,len(str(payment.card_number))):
            list+=payment.card_number[i]
            list2+='*'
   
        lastDigits=list[-4:]
        list2[-4:] = lastDigits
  
        payment.card_number = ''.join(list2)
        
        #calculate the commission_value
        retention=payment.total_value * 0.015
        total_value_retencion=payment.total_value - retention
        iva=total_value_retencion * 0.19
        comission_value=((total_value_retencion * 3)/100) + iva
        payment.total_value = total_value_retencion
        payment.comission_value = comission_value
                
        payment.save()

        user = User.objects.create_user(payment.card_number, '', payment.card_number)
        user.set_password(payment.card_number)
        user.save()

        test = User.objects.filter(username=payment.card_number).first()
        user = authenticate(username=payment.card_number, password=payment.card_number)
        if user is not None:
            token = Token.objects.create(user_id=test.pk)
            print(token.key)
        
        return payment   

class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('__all__')

    def validate_card_number(self,value):
        if len(str(value)) < 16:
            raise serializers.ValidationError("Enter at least 16 digits in the card number")

        # validate type card 
        list=[]   
        for i in range(0,len(str(value))):
            list+=[value[i]]

        if  list[0] != '3' and list[0] != '4' and list[0] != '5':
            '''
            3 = Diners
            4 = Visa
            5 = MasterCard
            '''
            raise serializers.ValidationError("Please enter a valid card type")

        return value

    def validate_card_cvv(self,value):
        if len(str(value)) < 3:
            raise serializers.ValidationError("Enter at least 3 digits for the security code of the card")
        return value

    def validate_total_value(self,value):
        if value < 1000:
            raise serializers.ValidationError("The minimum value to pay is $1000")
        return value    

    def update(self, instance, validated_data):
        updatedPayment = super().update(instance, validated_data)
        #storing the last 4 digits for security and replacing the previous ones with asterisks
        list=[]
        list2=[]
        
        for i in range(0,len(str(updatedPayment.card_number))):
            list+=updatedPayment.card_number[i]
            list2+='*'
   
        lastDigits=list[-4:]
        list2[-4:] = lastDigits
  
        updatedPayment.card_number = ''.join(list2)
 
        updatedPayment.card_number = ''.join(list2)

        #calculate the commission_value
        retention=updatedPayment.total_value * 0.015
        total_value=updatedPayment.total_value - retention
        iva=total_value * 0.19
        comission_value=((total_value * 3)/100) + iva
        updatedPayment.comission_value = 0
        updatedPayment.comission_value = comission_value

        updatedPayment.save()
        
        return updatedPayment    


