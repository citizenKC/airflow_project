select case when payment_type = 1 then '1.Credit card'
			when payment_type = 2 then '2.Cash'
			when payment_type = 3 then '3.No charge'
			when payment_type  = 4 then '4.Dispute'
			when payment_type  = 5 then '5.Unknown'
			when payment_type  = 6 then '6.Voided trip' 
			else 'NULL-value' end paym_type,
	   count(*)
from yellow_taxi_data ytd 
group by payment_type
order by 1