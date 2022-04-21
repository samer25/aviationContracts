# from datetime import datetime
# import json
#
# import stripe
# from django.conf import settings
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
#
# from board.models import RecruiterProfileModel
#
# stripe.api_key = settings.STRIPE_SECRET_KEY
#
#
# # @api_view(['POST'])
# # def check_session(request):
# # error = ''
# #
# # try:
# #     profile = RecruiterProfile.objects.filter(user__in=[request.user]).first()
# #     subscription = stripe.Subscription.retrieve(profile.stripe_subscription_id)
# #     product = stripe.Product.retrieve(subscription.plan.prodict)
# #     profile.plan_status = RecruiterProfile.PLAN_ACTIVE
# #     profile.plan_end_data = datetime.fromtimestamp(subscription.current_period_end)
# #     profile.membership = product.name
# #     profile.save()
# #
# #     return Response(status=status.HTTP_200_OK)
# #
# # except Exception:
# #     error = 'There something wrong. Please try again'
# #     return Response({'error': error})
#
#
# @api_view(['POST'])
# def create_checkout_session(request):
#     data = request.data
#     # print(data)
#     email = data['email']
#     payment_method_id = data['payment_method_id']
#     extra_msg = ''
#     # checking if customer with provided email already exists
#     customer_data = stripe.Customer.list(email=email).data
#     print(customer_data)
#
#     if len(customer_data) == 0:
#         # creating customer
#         customer = stripe.Customer.create(
#             email=email,
#             payment_method=payment_method_id,
#             invoice_settings={
#                 'default_payment_method': payment_method_id
#             }
#         )
#     else:
#         customer = customer_data[0]
#         extra_msg = "Customer already existed."
#     invoice = stripe.Invoice.upcoming(
#         customer=customer,
#     )
#     # print(invoice['period_end'])
#     # creating subscription
#     subscription = SubscriptionPlanModel.objects.get(recruiter=request.user.recruiter_profile)
#
#     subscription.plan_end_date = datetime.fromtimestamp(invoice['period_end'])
#     subscription.save()
#
#     stripe.Subscription.create(
#         customer=customer,
#         items=[
#             {
#                 'price': subscription.choice_plan_price_id
#             }
#         ]
#     )
#     return Response(status=status.HTTP_200_OK, data={'message': 'Success', 'data': {'customer_id': customer.id,
#                                                                                     'extra_msg': extra_msg}})
#
#
# @csrf_exempt
# def stripe_webhook(request):
#     webhook_secret = settings.STRIPE_WEBHOOK_KEY
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
#     request_data = json.loads(request.body)
#
#     if webhook_secret:
#         try:
#             event = stripe.Webhook.construct_event(
#                 payload=payload, sig_header=sig_header, secret=webhook_secret)
#             data = event['data']
#         except Exception as e:
#             return e
#         # Get the type of webhook event sent - used to check the status of PaymentIntents.
#         event_type = event['type']
#     else:
#         data = request_data['data']
#         event_type = request_data['type']
#     data_object = data['object']
#     # print(data)
#
#     # print('event ' + event_type)
#
#     if event_type == 'invoice.payment_succeeded':
#         print('🔔 Payment succeeded!')
#     elif event_type == 'customer.subscription.trial_will_end':
#         print('Subscription trial will end')
#     elif event_type == 'customer.subscription.created':
#         print('Subscription created %s', event.id)
#     elif event_type == 'customer.subscription.updated':
#         print('Subscription created %s', event.id)
#     elif event_type == 'customer.subscription.deleted':
#         # handle subscription canceled automatically based
#         # upon your subscription settings. Or if the user cancels it.
#         print('Subscription canceled: %s', event.id)
#
#     return HttpResponse(status=status.HTTP_200_OK)
