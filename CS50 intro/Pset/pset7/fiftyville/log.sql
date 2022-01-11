-- Keep a log of any SQL queries you execute as you solve the mystery.

--> CRIME SCENE DESCRIPTION : "the theft took place on July 28, 2020 and that it took place on Chamberlin Street":
SELECT description FROM crime_scene_reports WHERE year = 2020 AND month = 7 AND day = 28 AND street = "Chamberlin Street";

-- "Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse." 
-- "Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse."

--> TRANSCRIPTS AND WITNESSES :
SELECT DISTINCT(transcript) FROM interviews WHERE year = 2020 AND month = 7 AND day = 28 AND transcript LIKE "%courthouse%";
SELECT name FROM interviews WHERE transcript LIKE "%I saw the thief get into a car%";
SELECT name FROM interviews WHERE transcript LIKE "%Earlier this morning%";
SELECT name FROM interviews WHERE transcript LIKE "%the thief was leaving the courthouse%";

-- // Ruth // 
-- Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. 
-- If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.

-- // Eugene // 
-- I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, 
-- I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.

-- // Raymond //
-- As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. 
-- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.


--> LIST OF SUSPECT THAT LEFT COURTHOUSE AFTER 10:15 WITHIN 10min BY CAR :

SELECT * FROM people
JOIN courthouse_security_logs ON courthouse_security_logs.license_plate = people.license_plate
WHERE people.license_plate IN
(SELECT DISTINCT(courthouse_security_logs.license_plate) FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND activity = "exit")
ORDER BY name;

id | name | phone_number | passport_number | license_plate | id | year | month | day | hour | minute | activity | license_plate
243696 | Amber | (301) 555-4174 | 7526138472 | 6P58WS2 | 262 | 2020 | 7 | 28 | 10 | 18 | exit | 6P58WS2
467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8 | 263 | 2020 | 7 | 28 | 10 | 19 | exit | 4328GD8
396669 | Elizabeth | (829) 555-5269 | 7049073643 | L93JTIZ | 265 | 2020 | 7 | 28 | 10 | 21 | exit | L93JTIZ
686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X | 261 | 2020 | 7 | 28 | 10 | 18 | exit | 94KL13X
560886 | Evelyn | (499) 555-9472 | 8294398571 | 0NTHK55 | 267 | 2020 | 7 | 28 | 10 | 23 | exit | 0NTHK55
221103 | Patrick | (725) 555-4692 | 2963008352 | 5P2BI95 | 260 | 2020 | 7 | 28 | 10 | 16 | exit | 5P2BI95
398010 | Roger | (130) 555-0289 | 1695452385 | G412CB7 | 264 | 2020 | 7 | 28 | 10 | 20 | exit | G412CB7
514354 | Russell | (770) 555-1861 | 3592750733 | 322W7JE | 266 | 2020 | 7 | 28 | 10 | 23 | exit | 322W7JE


--> LIST OF SUSPECT THAT HAD WITHDRAWED SOME MONEY ON THAT DAY ON FIFER STREET'S ATM.

SELECT * FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE bank_accounts.account_number IN 
(SELECT bank_accounts.account_number FROM bank_accounts
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location LIKE "%Fifer Street%" AND transaction_type LIKE "%withdraw%")
ORDER BY name;

id | name | phone_number | passport_number | license_plate | account_number | person_id | creation_year
395717 | Bobby | (826) 555-1652 | 9878712108 | 30G67EN | 28296815 | 395717 | 2014
467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8 | 28500762 | 467400 | 2014
396669 | Elizabeth | (829) 555-5269 | 7049073643 | L93JTIZ | 25506511 | 396669 | 2014
686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X | 49610011 | 686048 | 2010
449774 | Madison | (286) 555-6063 | 1988161715 | 1106N58 | 76054385 | 449774 | 2015
458378 | Roy | (122) 555-4581 | 4408372428 | QX4YZN3 | 16153065 | 458378 | 2012
514354 | Russell | (770) 555-1861 | 3592750733 | 322W7JE | 26013199 | 514354 | 2012
438727 | Victoria | (338) 555-6650 | 9586786673 | 8X428L0 | 81061156 | 438727 | 2018


--> LIST OF SUSPECT, LEAVING FIFTYVILLE WITH THE EARLIEST TOMORROW FLIGHT

SELECT * FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE passengers.passport_number IN
(SELECT passengers.passport_number FROM passengers 
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.id = (SELECT id FROM flights WHERE month = 7 AND day = 29 AND hour = (SELECT min(hour) FROM flights WHERE month = 7 AND day = 29)))
ORDER BY name;

id | name | phone_number | passport_number | license_plate | flight_id | passport_number | seat
395717 | Bobby | (826) 555-1652 | 9878712108 | 30G67EN | 36 | 9878712108 | 7A
467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8 | 11 | 8496433585 | 5D
467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8 | 36 | 8496433585 | 7B
467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8 | 48 | 8496433585 | 7C
953679 | Doris | (066) 555-9701 | 7214083635 | M51FA04 | 36 | 7214083635 | 2A
651714 | Edward | (328) 555-1152 | 1540955065 | 130LD9Z | 36 | 1540955065 | 5C
686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X | 36 | 5773159633 | 4A
560886 | Evelyn | (499) 555-9472 | 8294398571 | 0NTHK55 | 36 | 8294398571 | 6C
449774 | Madison | (286) 555-6063 | 1988161715 | 1106N58 | 36 | 1988161715 | 6D
398010 | Roger | (130) 555-0289 | 1695452385 | G412CB7 | 36 | 1695452385 | 3B


-- > LIST OF SUSPECT, CALLING FOR LESS THAN A MINUTE THAT DAY
SELECT * FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE people.phone_number IN
(SELECT phone_calls.caller FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60)
ORDER BY name;

id | name | phone_number | passport_number | license_plate | id | caller | receiver | year | month | day | duration
395717 | Bobby | (826) 555-1652 | 9878712108 | 30G67EN | 279 | (826) 555-1652 | (066) 555-9701 | 2020 | 7 | 28 | 55
686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X | 245 | (367) 555-5533 | (022) 555-4052 | 2020 | 7 | 28 | 241
686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X | 236 | (367) 555-5533 | (344) 555-9601 | 2020 | 7 | 28 | 120
686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X | 233 | (367) 555-5533 | (375) 555-8161 | 2020 | 7 | 28 | 45
686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X | 285 | (367) 555-5533 | (704) 555-5790 | 2020 | 7 | 28 | 75
560886 | Evelyn | (499) 555-9472 | 8294398571 | 0NTHK55 | 251 | (499) 555-9472 | (717) 555-1342 | 2020 | 7 | 28 | 50
560886 | Evelyn | (499) 555-9472 | 8294398571 | 0NTHK55 | 224 | (499) 555-9472 | (892) 555-8872 | 2020 | 7 | 28 | 36
561160 | Kathryn | (609) 555-5876 | 6121106406 | 4ZY7I8T | 234 | (609) 555-5876 | (389) 555-5198 | 2020 | 7 | 28 | 60
907148 | Kimberly | (031) 555-6622 | 9628244268 | Q12B3Z3 | 261 | (031) 555-6622 | (910) 555-3251 | 2020 | 7 | 28 | 38
449774 | Madison | (286) 555-6063 | 1988161715 | 1106N58 | 284 | (286) 555-6063 | (310) 555-8568 | 2020 | 7 | 28 | 235
449774 | Madison | (286) 555-6063 | 1988161715 | 1106N58 | 254 | (286) 555-6063 | (676) 555-6554 | 2020 | 7 | 28 | 43
398010 | Roger | (130) 555-0289 | 1695452385 | G412CB7 | 221 | (130) 555-0289 | (996) 555-8899 | 2020 | 7 | 28 | 51
514354 | Russell | (770) 555-1861 | 3592750733 | 322W7JE | 255 | (770) 555-1861 | (725) 555-3243 | 2020 | 7 | 28 | 49
438727 | Victoria | (338) 555-6650 | 9586786673 | 8X428L0 | 281 | (338) 555-6650 | (704) 555-2131 | 2020 | 7 | 28 | 54

--> MERGE ALL LIST OF SUSPECT NAMES :

SELECT DISTINCT(name) FROM people
JOIN courthouse_security_logs ON courthouse_security_logs.license_plate = people.license_plate
WHERE people.license_plate IN
(SELECT DISTINCT(courthouse_security_logs.license_plate) FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND activity = "exit")
INTERSECT
SELECT DISTINCT(name) FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE bank_accounts.account_number IN 
(SELECT bank_accounts.account_number FROM bank_accounts
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location LIKE "%Fifer Street%" AND transaction_type LIKE "%withdraw%")
INTERSECT
SELECT DISTINCT(name) FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE passengers.passport_number IN
(SELECT passengers.passport_number FROM passengers 
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.id = (SELECT id FROM flights WHERE month = 7 AND day = 29 AND hour = (SELECT min(hour) FROM flights WHERE month = 7 AND day = 29)))
INTERSECT
SELECT DISTINCT(name) FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE people.phone_number IN
(SELECT phone_calls.caller FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60);

--> SUSPECTS NAMES ARE :

Ernest
Madison


--> SUSPECTS INFOS :

SELECT * FROM people WHERE name = "Ernest" OR name = "Madison";

id | name | phone_number | passport_number | license_plate
449774 | Madison | (286) 555-6063 | 1988161715 | 1106N58
686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X


--> THE FLIGHT THEY ARE BOTH TAKING :

SELECT * FROM flights WHERE month = 7 AND day = 29 AND hour = (SELECT min(hour) FROM flights WHERE month = 7 AND day = 29);

id | origin_airport_id | destination_airport_id | year | month | day | hour | minute
36 | 8 | 4 | 2020 | 7 | 29 | 8 | 20


--> FLIGHT DESTINATION:

SELECT DISTINCT(city) FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
WHERE destination_airport_id =
(SELECT destination_airport_id FROM flights WHERE month = 7 AND day = 29 AND hour = (SELECT min(hour) FROM flights WHERE month = 7 AND day = 29));

city

London


--> THE CALLS OF BOTH SUSPECTS ON THAT DAY:

SELECT * FROM phone_calls WHERE caller = "(286) 555-6063" OR caller = "(367) 555-5533" AND DAY = 28 AND duration < 60;

id | caller | receiver | year | month | day | duration
233 | (367) 555-5533 | (375) 555-8161 | 2020 | 7 | 28 | 45
254 | (286) 555-6063 | (676) 555-6554 | 2020 | 7 | 28 | 43


--> RECEIVER LOGS:

SELECT * FROM people WHERE phone_number = "(375) 555-8161" OR phone_number = "(676) 555-6554" ORDER BY name;

id | name | phone_number | passport_number | license_plate
864400 | Berthold | (375) 555-8161 |  | 4V16VO0
250277 | James | (676) 555-6554 | 2438825627 | Q13SVG6

--> SO THE COULD BE (Thief name) / ACCOMPLICE (name receiver) / LOCATION (Destination of flight) :

ERNEST / BERTHOLD / LONDON
MADISON / JAMES / LONDON

