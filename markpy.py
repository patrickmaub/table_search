import textwrap
def format_as_markdown_table(data):
    # Extract headers and rows
    headers = set()
    rows = set()
    for key in data.keys():
        if isinstance(key, tuple) and len(key) == 2:
            rows.add(key[0])  # row title
            headers.add(key[1])  # column title

    # Sort headers and rows to maintain consistent order
    headers = sorted(list(headers))
    rows = sorted(list(rows))

    # Start building the markdown table
    markdown_lines = ["|  | " + " | ".join(headers) + " |", "|---|" * (len(headers) + 1)]  # corrected line

    for row in rows:
        new_line = f"| {row} |"
        for header in headers:
            key = (row, header)
            if key in data and 'Response' in data[key] :
                if data[key]['Response'] is None:
                    new_line += " N/A |"
                    continue
                # Remove newlines and limit the response length
                response = ' '.join(data[key]['Response'].split())
                #response = textwrap.shorten(response, width=100, placeholder="...")
                new_line += f" {response} |"
            else:
                new_line += " N/A |"  # Indicate data not available/missing
        markdown_lines.append(new_line)

    # Join the lines and ensure proper formatting for markdown
    markdown_table = "\n".join(markdown_lines).replace("|---|", "|---")
    return markdown_table

# Test data
#data = {('Delta Airlines', 'Reimbursement Policy'): {'Response': 'If there is a flight cancellation or significant delay (>120 minutes), you will be rebooked on an alternative flight, or your ticket will be converted to an eCredit for future travel. However, in some instances, you may be eligible to request a refund* of any unused portion of your non-refundable ticket or for unused trip purchases if you choose not to travel. Please note that most tickets are nonrefundable and not all amenities are refundable; see their individual terms for details. Once submitted, we will do our best to process your request in a timely manner and update you on your refund eligibility.', 'URL': 'https://www.delta.com/us/en/change-cancel/cancel-flight', 'Content': None, 'Attempts': 0}, ('Delta Airlines', 'Cancellation and Delay Policy'): {'Response': 'If we have already canceled your flight, and you would like to request a refund to your original form of payment, please complete the Travel Disruptions form:', 'URL': 'https://www.delta.com/us/en/change-cancel/cancel-flight', 'Content': None, 'Attempts': 0}, ('Delta Airlines', 'Lost Baggage Policy'): {'Response': 'Please note that we are unable to reimburse the following:\n\nDelayed baggage expenses', 'URL': 'https://www.delta.com/us/en/change-cancel/cancel-flight', 'Content': None, 'Attempts': 0}, ('Delta Airlines', 'Cancellation and Delay Reimbursement Policy'): {'Response': 'If you incurred hotel, transportation and/or meal expenses due to a significant delay or cancellation that was within our control, please submit a reimbursement request.* Once submitted, we will review your request, determine eligibility and update you on the status.', 'URL': 'https://www.delta.com/us/en/change-cancel/cancel-flight', 'Content': None, 'Attempts': 0}, ('American Airlines', 'Reimbursement Policy'): {'Response': "We will reimburse you for the reasonable and necessary items you need immediately while away from home without your bags. To be reimbursed send this information to us within 30 days of your delay:\n\nYour 13-character file ID\nA copy of your ticket receipt and baggage claim checks\nYour original, dated, itemized receipts\n\nIf we can't find your bag, any expense reimbursement will be deducted from the final settlement amount.", 'URL': 'https://www.aa.com/i18n/travel-info/baggage/delayed-or-damaged-baggage.jsp', 'Content': None, 'Attempts': 0}, ('American Airlines', 'Cancellation and Delay Policy'): {'Response': 'Our Central Baggage Resolution Office will do everything they can to locate your bag. If they’re unsuccessful a final decision about your claim will be made in accordance with our:\n\nThis decision will be sent to you by email.', 'URL': 'https://www.aa.com/i18n/travel-info/baggage/delayed-or-damaged-baggage.jsp', 'Content': None, 'Attempts': 0}, ('American Airlines', 'Lost Baggage Policy'): {'Response': 'Our Central Baggage Resolution Office will do everything they can to locate your bag. If they’re unsuccessful a final decision about your claim will be made in accordance with our:\n\nThis decision will be sent to you by email.', 'URL': 'https://www.aa.com/i18n/travel-info/baggage/delayed-or-damaged-baggage.jsp', 'Content': None, 'Attempts': 0}, ('American Airlines', 'Cancellation and Delay Reimbursement Policy'): {'Response': "If we can't find your bag, any expense reimbursement will be deducted from the final settlement amount.", 'URL': 'https://www.aa.com/i18n/travel-info/baggage/delayed-or-damaged-baggage.jsp', 'Content': None, 'Attempts': 0}, ('Southwest Airlines', 'Reimbursement Policy'): {'Response': 'Southwest Airlines announced Tuesday afternoon it will reimburse expenses to those who had flight cancellations.', 'URL': 'https://abc7news.com/southwest-airlines-refund-flight-cancelled-travelers-rights/12624613/', 'Content': None, 'Attempts': 4}, ('Southwest Airlines', 'Cancellation and Delay Policy'): {'Response': 'Southwest Airlines offers a unique advantage to its passengers with the 24-hour risk-free cancellation policy. According to this policy, passengers are allowed to cancel their bookings within 24 hours of purchase without incurring any cancellation fees. This means that if you book a flight with Southwest and have second thoughts or need to change your travel plans within the first 24 hours, you can do so without any financial implications.', 'URL': 'https://www.linkedin.com/pulse/how-cancel-southwest-flight-cancellation-policy-refund-johnathen', 'Content': None, 'Attempts': 4}, ('Southwest Airlines', 'Lost Baggage Policy'): {'Response': 'Southwest Airlines takes great care to ensure that passengers’ bags reach the destination safely, without being exposed to any theft or damages. As happens in any section and due to any unforeseen circumstances, such as technical disruptions, human error, etc – in rarest of the rarest cases the damages, theft, or any delay may occur to the passenger’s luggage. In this context, we cover the Southwest lost and found situations where – Passengers are not receiving their baggage at the end of their journey Passengers receiving the baggage in the damaged condition Passengers receiving baggage after a considerable amount of time Passengers receiving the baggage with missing contents/articles Southwest Airlines lost and found also cover the instances where the passenger lost their belongings on the plane after your flight. Southwest Airlines Lost and Found Information and Tips Here are the certain tips that passengers must apply to travel in order to prevent Southwest lost baggage disruptions or avoid them with minimum loss – Southwest lost luggage department recommends not to include any valuable item (jewellery, cash, wallets), critical item (medicine, passport, photo ID), or fragile items (electronic devices, glassware, glasses. contact lenses) in your baggage that you deliver at check-in. As per Southwest lost and found policy, avoid travelling with your baggage that was damaged during previous travel. In the case where the damaged area gets enlarged, the baggage might get unusable or your belongings inside may get damaged. Use locks that are TSA-approved. In the case where your baggage is opened due to security reasons, your baggage will be prevented from getting damaged. Southwest baggage lost and found team recommends the inclusion of a paper note that mentions the passenger’s name and contact which will help the delivery of your baggage in the case when baggage tag comes off. If there is not plenty of room left in the overhead cabinet, at times, the carry-on baggage may be taken out of cabin baggage. In case the passenger does not want to take belongings out of cabin baggage, please notify the Southwest Airlines lost and found team about the situation. For making the lost and found application and following up the older application regarding all the baggage disruption, passengers need to approach Southwest airlines baggage claim and tracking team. Until the Southwest lost baggage application is concluded, passengers need to keep the baggage tag and the boarding pass. As per Southwest airlines lost and found policy, all the information, and documents provided by the passengers from the beginning due to the baggage disruption are processed within the scope of personal data protection. Southwest Lost and Found Locations You can find all the detailed information regarding the Southwest lost baggage disruption here – If the passengers’ baggage is not received at the destination or stopover point after the flight, they can apply to Southwest airlines lost and found department at the relevant airport. Here is the list of airports where Southwest lost and found office would be available regarding your lost baggage – Airport Offices Airport Codes Dallas Love Field Airport DAL Los Angeles International Airport LAX Chicago Midway International Airport MDW Oakland International Airport OAK San Diego International Airport SAN Baltimore International Airport BWI Denver International Airport DEN Phoenix International Airport PHX Houston Hobby International airport HOU Atlanta International Airport ATL Orlando International Airport MCO Las Vegas International Airport LAS Tampa International Airport TPA In addition, upon the passenger’s application, they would be provided a Property Irregularity Report (PIR) regarding their lost baggage with Southwest airlines. Passengers are also required to keep the baggage tag and the boarding pass for all further procedures until the baggage will be delivered to them. How to Apply For Southwest Lost Baggage? In the case where the baggage is not delivered to them, passengers must necessarily apply to the Southwest lost and found office at the destination airport or contact Southwest airlines customer service lost and found. The Southwest airlines lost baggage report must be issued for your belongings to be searched thoroughly and the process to be maintained and the relevant compensation would be offered in case the airline fails to locate your baggage. Southwest baggage lost and found office at the airport – It is the place where you must submit your documents and receive a PIR alongside the lost and found tracking number the moment you fail to receive baggage. Southwest lost and found online application – Online application is the alternative where passengers have left the airport without having a report issued, as they must apply for tracking the baggage. In the instance where the passengers leave the airport without reporting to the Southwest Airlines baggage claim desk, the pecuniary loss that may arise shall be under the responsibility of the affected passenger. In the case where the passenger is unable to locate their belongings at the baggage conveyors, the passenger must immediately escalate the concern at the Southwest lost baggage desk at the airport. Expanded Southwest Baggage Tracking Process Here is the detailed process to fill the Southwest airlines lost and found form – As per Southwest airlines baggage policy, the baggage would be tracked by Southwest airlines on the route passengers have travelled during the first five days. The search and screening shall be carried out through the Southwest baggage lost and found international tracking system as most of the luggage is identified within 24 hours and delivered to the passengers as soon as possible. In the rarest of the rarest cases, the unwanted delay may happen in the delivery of the checked bag due to operational reasons. For lost baggage that is unable to be identified within a period of 5 days, passengers would be asked to submit a detailed and priced list of the items covered in the lost baggage shall be requested for further detailed tracking of the baggage. In the case where passengers have not been responded to by the airline after 5 days, they may visit the Southwest baggage lost and found online tracking portal and must create a notification. In the message section passengers need to add the message alongside attaching the documents for the notification they have created. In the message, passengers need to add the details they will provide regarding the appearance and content of', 'URL': 'https://airlinespolicy.com/lost-and-found/southwest-lost-and-found/', 'Content': None, 'Attempts': 4}, ('Southwest Airlines', 'Cancellation and Delay Reimbursement Policy'): {'Response': 'You can almost always get compensation from Southwest Airlines for delayed or cancelled flights. The compensation usually comes in the form of LUV Vouchers, which can range from $75 to $200 per person. These vouchers can be used to book future flights with Southwest Airlines.', 'URL': 'https://katiestraveltricks.com/southwest-delayed-flight-compensation/', 'Content': None, 'Attempts': 4}, ('United Airlines', 'Reimbursement Policy'): {'Response': "United is not obliged to pay you the flight compensation described in B) Re-routing under comparable transport conditions to your final destination at the earliest opportunity or, at a later date if: final destination at the earliest opportunity or, at a later date\n1) You are informed of the cancellation of your flight at least two (2) at your convenience, subject to the availability of seats.\nweeks before the scheduled time of departure; or If we offer you a flight to an airport other than that for which\n2) You are informed of the cancellation between two (2) weeks and the booking was made (in case the town, city or region is\nseven (7) days before the scheduled time of departure and you are served by several airports), we will pay the cost of transferring\noffered re-routing, allowing you to depart no more than two (2) you from that alternative airport either to that for which the\nhours before the scheduled time of departure and to reach your booking was made or to another close-by destination agreed\nCustomer Care\n900 Grand Plaza Drive, Dept. NHCCR, Houston, Texas 77607 final destination less than four (4) hours after the scheduled time of with you.\nFax: 832-235-1806/800-214-0605 arrival; or 2) We will reimburse you in cash, by EFT, bank order or bank check or,\n3) You are informed of the cancellation less than seven (7) days with your written agreement, in a travel voucher.\nIn order for us to process your claim expeditiously, please\nbefore the scheduled time of departure and you are offered\nsupply your name, contact details (email address and/or C. Right to Care\nre-routing, allowing you to depart no more than one (1) hour\nmailing address), ticket number, flight number, booking\nbefore the scheduled time of departure and to reach your final If you are involuntarily denied boarding, your flight is cancelled,\nreference and details of the claim you are making. To make\ndestination less than two (2) hours after the scheduled time or your flight is delayed by more than two (2) hours beyond its\na claim for compensation, please contact United Customer of arrival. scheduled time of departure, United will offer you the following\nCare online at: united.com/feedback free of charge:\nIn addition, you may not be entitled to compensation if your flight\nNotice of Your Rights for Flights To and From the State of was cancelled because of special circumstances which were not under A) If the expected departure time of your new flight (if any) is the\nIsrael in the Event of a Flight Delay, Cancellation or Denied our control, and the cancellation could not have been prevented even same day as the departure date of your originally ticketed flight,\nboarding; or your Seat is Downgraded if we would have taken all reasonable measures possible to avoid the you are entitled to receive:\nThis Notice contains important information about your rights delay, or a labor strike. Meals and beverages commensurate with the expected waiting\nestablished under Israeli Aviation Services Law (Compensation and time; and\nDenied Boarding\nAssistance for Flight Cancellation and Change of Conditions), 5772- Before we deny boarding to any passenger, we will request volunteers Two telephone calls and sending of a notice by fax or e-mail,\n2012 (“Aviation Services Law”), in the event that your flight is delayed to surrender their seats in exchange for agreed upon compensation at your election.\nor cancelled, you are denied boarding or are downgraded. This\nor benefits. In the event that there are insufficient volunteers and B) If a stay of one (1) or more nights becomes necessary or a stay\nNotice explains your rights under the Aviation Services Law for flight\nyou are involuntarily denied boarding, you are entitled to the rights additional to that intended by you becomes necessary:\noperated by United Airlines.\ndefined under subsections A, B and C in the Description of Your Rights\nHotel accommodations; and\nYou may be entitled to benefits under Aviation Services Law if: section of this Notice.\nT (hra on tes lp oo rr t b the et rw le oe cn tt ioh ne ia ir yp oo ur t aa vn ed cp hl oa sc ee o tf a sc tc ao ym em lso ed wa ht eio rn\nYou have a confirmed reservation and United is the operating Downgrade o a f h n o e\ncarrier for the flight concerned; If we are unable to seat you in the boarding class for which you at a reasonable distance from the airport)\nYou have presented yourself at the check-in counter at the purchased your ticket, you may be entitled to compensation as\nairport at least ninety (90) minutes before the scheduled specified in subsection D in the Description of Your Rights section We may also limit or decline your right to care if provision of care\nflight time; of this Notice. would itself cause further delay.\nThe ticket for your travel was purchased at a fare available to the D. Right to Compensation in the event of a Downgrade\npublic, including a frequent flyer program. You are not entitled to Description of Your Rights\nthese rights if you are denied boarding on the grounds of health, A. Right to Compensation for which your ticket was purchased, and are only able to offer you a\nsafety, security or invalid travel documentation.\n1) If your flight is cancelled or delayed by at least eight (8) hours from seat in the cabin class lower than the class for which your ticket was\nFlight Delay the originally scheduled departure time, or you are involuntarily purchased, we will pay you the following compensation:\nIn the event that your flight is delayed by two (2) hours or more from its denied boarding, you are entitled to receive compensation from us A) Transfer from First Class to Business'''", 'URL': 'https://media.united.com/images/Media%20Database/SDL/travel/destination/international/CSM859-IL-Notice-of-Rights-English-2016-09-REV-ADA.pdf', 'Content': None, 'Attempts': 4}, ('United Airlines', 'Cancellation and Delay Policy'): {'Response': 'The United Airlines cancellation policy delivers its flyers with a 24 hour risk-free window, under which passengers can cancel their bookings for free and will be eligible for a complete refund, regardless of fare type. However, if you cancel your flight after 24 hours, then you have to pay a certain amount as a United Airlines cancel flight fee.', 'URL': 'https://www.flyingrules.com/cancellation-policy/united-airlines-cancellation-policy', 'Content': None, 'Attempts': 1}, ('United Airlines', 'Lost Baggage Policy'): {'Response': 'United Airlines allows you to claim reimbursement of reasonable expenses that you incur because of a baggage delay.', 'URL': 'https://www.nerdwallet.com/article/travel/delayed-baggage-compensation-broken-down-by-airline', 'Content': None, 'Attempts': 4}, ('United Airlines', 'Cancellation and Delay Reimbursement Policy'): {'Response': 'United Airlines commonly overbooks flights and passengers may qualify for compensation in certain circumstances.', 'URL': 'https://www.claimcompass.eu/en/airline-ratings/united-airlines/', 'Content': None, 'Attempts': 4}, ('JetBlue Airways', 'Reimbursement Policy'): {'Response': 'As long as you’ve booked travel at least seven days before the scheduled departure date, you’ll be eligible for a full refund for up to 24 hours from the time of booking. You’ll be charged no fees, and your refund will be given back to the original form of payment. This is policy mandated by the U.S. Department of Transportation and applies to all fares on all airlines.', 'URL': 'https://www.nerdwallet.com/article/travel/how-to-get-a-jetblue-refund', 'Content': None, 'Attempts': 4}, ('JetBlue Airways', 'Cancellation and Delay Policy'): {'Response': 'JetBlue Airlines will try its best to compensate you in the best possible way.', 'URL': 'https://www.iairtickets.com/jetblue-delay-compensation/', 'Content': None, 'Attempts': 4}, ('JetBlue Airways', 'Lost Baggage Policy'): {'Response': 'You can do this in two ways: With the JetBlue staff member while at the airport Via an online form', 'URL': 'https://donotpay.com/learn/jetblue-lost-luggage/', 'Content': None, 'Attempts': 4}, ('JetBlue Airways', 'Cancellation and Delay Reimbursement Policy'): {'Response': 'JetBlue Airlines processes all cancellations according to Jetblue flight cancellation policy, which determines the cancellation fee based on when the ticket is canceled and the reason for cancellation. Only when JetBlue cancels a flight will passengers be eligible to receive full refunds or credit vouchers. In cases where flights are delayed or canceled by the airline, passengers may receive special facilities such as complimentary food or drinks.', 'URL': 'https://www.linkedin.com/pulse/jetblue-airline-cancellation-policy-refund-rules-scarlett-johnathen', 'Content': None, 'Attempts': 0}}
#print (format_as_markdown_table(data))

