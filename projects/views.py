from rest_framework import generics
from projects.serializers import PaymentListSerializer, PaymentSerializer
from rest_framework.response import Response
from rest_framework import status
        

class PaymentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = PaymentSerializer.Meta.model.objects.all()

    def post(self,request):
        # send information to serializer
        serializer = self.serializer_class(data=request.data)
        # serializer validations
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Payment successful'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

class PaymentRetrieveUpdateDestroyAPiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentListSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return  self.get_serializer().Meta.model.objects.filter(id = pk).first()  

    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            payment_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(payment_serializer.data, status = status.HTTP_200_OK)

        return Response({'message':'No payment found with this data'}, status = status.HTTP_400_BAD_REQUEST)        

    def put(self, request, pk=None):
        if self.get_queryset(pk):
            payment_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if payment_serializer.is_valid():
                payment_serializer.save()

                return Response(payment_serializer.data, status = status.HTTP_200_OK)
    
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'message':'No payment found with this data'}, status = status.HTTP_400_BAD_REQUEST)            

    def delete(self, request, pk=None):
        payment = self.get_queryset().filter(id = pk).first() # get instance
        if payment:
            payment.delete() 
            return Response({'message':'Deleted successfully!'}, status = status.HTTP_200_OK)

        return Response({'message':'No payment found with this data'}, status = status.HTTP_400_BAD_REQUEST)


            
