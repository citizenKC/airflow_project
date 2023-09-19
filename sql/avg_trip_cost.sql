/* average trip cost per passenger_count */

SELECT passenger_count,
	   round(avg(total_amount)) as avg_trip_cost 
FROM yellow_taxi_data ytd
where passenger_count > 0
GROUP BY passenger_count

