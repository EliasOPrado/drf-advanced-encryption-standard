### Advanced Encryption Standard - 256 (AES256) for python django


Example of application in an APIView.post:

```


class ApplicantPersonalDataAPIView(APIView):
    
    serializer_class = ApplicantPersonalDataSerializer
    queryset = ApplicantPersonalData.objects.all()
 
    def post(self, request):
        """
        Post encrypted data.
        """
 
        # get data from request
        data = request.data
        # from data fetch the applicant_id
        data_applicant_id = data['applicant_id']
        # insert the applicant_id into applicant to be rec into applicant_data
        applicant = Applicant.objects.get(id=data_applicant_id)
        # To create the form and get the serializer and add a form
        serializer = ApplicantPersonalDataSerializer(data=data)
        
        if serializer.is_valid():
            # Define the encryption key
            aes = AESCipher( settings.SECRET_KEY[:16], 32)
            
            applicant_data = ApplicantPersonalData.objects.create(
                # "applicant" added to recognize the queryset
                applicant_id = applicant,
                name = aes.encrypt(serializer.data['name']),
                document_type = aes.encrypt(serializer.data['document_type']),
                document_code = aes.encrypt(serializer.data['document_code']),
            )
            applicant_data.save()
 
            # data to be displayed on response.
            displayed_data ={
                'id':applicant_data.id,
                'applicant_id': applicant_data.applicant_id.id,
                'name': applicant_data.name,
                'document_type': applicant_data.document_type,
                'document_code': applicant_data.document_code,
            }
            return Response(displayed_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
```

url.py:

```
import....

urlpatterns =[
    path('path-to-data/', ApplicantPersonalDataAPIView.as_view())
}
```