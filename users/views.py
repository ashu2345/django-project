from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CredentialForm
from .models import Orders, CustomUser, CartOrders, Item
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
import imp
import random
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

# Create your views here.
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

def addFood(request,item_id):
    customer = CustomUser.objects.get(username__exact = request.user.username)
    item = Item.objects.get(pk = item_id)
    cartorder = CartOrders(customer = customer, item = item)
    cartorder.save()
    cartorders = customer.cartorders_set.all()
    return render(request,"users/cart.html",{'cartorders':cartorders})

def confirmOrder(request):
    customer = CustomUser.objects.get(username__exact = request.user.username)
    cartorders = customer.cartorders_set.all()
    totalprice = 0
    for cartorder in cartorders:
        totalprice += cartorder.item.price
    for cartorder in cartorders:
        order = Orders(customer = customer, item = cartorder.item)
        order.save()
    cartorders.delete()
    return render(request,"users/success.html",{'customer':customer, 'totalprice':totalprice})

def displayFood(request):
    customer = CustomUser.objects.get(username__exact = request.user.username)
    return render(request,'users/ordlist.html',{'customer':customer})

def deleteCartOrder(request, cart_id):
    customer = CustomUser.objects.get(username__exact = request.user.username)
    order = customer.cartorders_set.get(pk = cart_id)
    item_name = order.item.name
    order.delete()
    return render(request,"users/deleteorders.html",{'item_name':item_name})

def showCart(request):
    customer = CustomUser.objects.get(username__exact = request.user.username)
    cartorders = customer.cartorders_set.all()
    return render(request,"users/cart.html",{'cartorders':cartorders})

def paymentPortal(request):
    if request.method == "POST":
        form = CredentialForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['customer'] = CustomUser.objects.get(username__exact = request.user.username)
            print(data)
            amount = 0
            customer = CustomUser.objects.get(username__exact = request.user.username)
            for cartorder in customer.cartorders_set.all():
                amount += cartorder.item.price
            if authorize_credit_card(amount, data).messages.resultCode == "Ok":
                return HttpResponseRedirect(reverse("users:confirmOrder"))
    else:
        form = CredentialForm()
        return render(request,"users/paymentform.html",{'form':form})

# CONSTANTS = imp.load_source('modulename', 'constants.py')

def authorize_credit_card(amount, data):
    """
    Authorize a credit card (without actually charging it)
    """

    # Create a merchantAuthenticationType object with authentication details
    # retrieved from the constants file
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = '3t2LGu4AR2Nb'
    merchantAuth.transactionKey = '78eC2pb4J42cu2WL'

    # Create the payment data for a credit card
    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = str(data['credit_card'])
    creditCard.expirationDate = data['expiry']
    #creditCard.cardCode = data['cvv']

    # Add the payment data to a paymentType object
    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    # Create order information
    invoiceNum = str(random.randint(1,1000))
    order = apicontractsv1.orderType()
    order.invoiceNumber = invoiceNum
    order.description = "Food Items"

    # Set the customer's Bill To address
    zipcode = str(data['zipcode'])
    customerAddress = apicontractsv1.customerAddressType()
    customerAddress.firstName = data['customer'].firstname
    customerAddress.lastName = data['customer'].lastname
    customerAddress.company = data['company']
    customerAddress.address = data['address']
    customerAddress.city = data['city']
    customerAddress.state = data['state']
    customerAddress.zip = zipcode
    customerAddress.country = data['country']

    # Set the customer's identifying information
    custId = str(data['customer'].pk)
    customerData = apicontractsv1.customerDataType()
    customerData.type = "individual"
    customerData.id = custId
    customerData.email = data['customer'].email

    # Add values for transaction settings
    duplicateWindowSetting = apicontractsv1.settingType()
    duplicateWindowSetting.settingName = "duplicateWindow"
    duplicateWindowSetting.settingValue = "600"
    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(duplicateWindowSetting)

    # build the array of line items
    line_items = apicontractsv1.ArrayOfLineItem()

    # setup individual line items
    for cartitem in data['customer'].cartorders_set.all():
        itemId = str(cartitem.item.pk)
        temp_item = apicontractsv1.lineItemType()
        temp_item.itemId = itemId
        temp_item.name = cartitem.item.name
        temp_item.descr = cartitem.item.descr
        temp_item.quantity = 1
        temp_item.unitPrice = cartitem.item.price
        line_items.append(temp_item)


    # Create a transactionRequestType object and add the previous objects to it.
    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authOnlyTransaction"
    transactionrequest.amount = amount
    transactionrequest.payment = payment
    transactionrequest.order = order
    transactionrequest.billTo = customerAddress
    transactionrequest.customer = customerData
    transactionrequest.transactionSettings = settings
    transactionrequest.lineItems = line_items

    # Assemble the complete transaction request
    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId = "MerchantID-0001"
    createtransactionrequest.transactionRequest = transactionrequest
    # Create the controller
    createtransactioncontroller = createTransactionController(
        createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    if response is not None:
        # Check to see if the API request was successfully received and acted upon
        if response.messages.resultCode == "Ok":
            # Since the API request was successful, look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages') is True:
                print(
                    'Successfully created transaction with Transaction ID: %s'
                    % response.transactionResponse.transId)
                print('Transaction Response Code: %s' %
                      response.transactionResponse.responseCode)
                print('Message Code: %s' %
                      response.transactionResponse.messages.message[0].code)
                print('Description: %s' % response.transactionResponse.
                      messages.message[0].description)
            else:
                print('Failed Transaction.')
                if hasattr(response.transactionResponse, 'errors') is True:
                    print('Error Code:  %s' % str(response.transactionResponse.
                                                  errors.error[0].errorCode))
                    print(
                        'Error message: %s' %
                        response.transactionResponse.errors.error[0].errorText)
        # Or, print errors if the API request wasn't successful
        else:
            print('Failed Transaction.')
            if hasattr(response, 'transactionResponse') is True and hasattr(
                    response.transactionResponse, 'errors') is True:
                print('Error Code: %s' % str(
                    response.transactionResponse.errors.error[0].errorCode))
                print('Error message: %s' %
                      response.transactionResponse.errors.error[0].errorText)
            else:
                print('Error Code: %s' %
                      response.messages.message[0]['code'].text)
                print('Error message: %s' %
                      response.messages.message[0]['text'].text)
    else:
        print('Null Response.')

    return response