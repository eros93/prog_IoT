Politecnico di Torino - DET
Lat: 45.063306
Lon: 7.660051

####################################
API FORMAT
####################################
JSON format of Weather Adaptor API.
Sent using MQTT protocol.

Example:
{"request": "tomorrow_forecast", "summary": "Partially cloudly in the afternoon", "sunrise":"1491109752", "sunset":"1491155932", "watering_flag":"True"}


watering_flag ==> "True": watering process in needed
			  ==> "False": watering process in NOT needed


####################################
ENRICO NOTES
####################################

DARK SKY API
Overview: https://darksky.net/dev/docs

Forecast request: https://darksky.net/dev/docs/forecast

Resonse Format: https://darksky.net/dev/docs/response

Example FORECAST request:
https://api.darksky.net/forecast/c61a2cd84bc2ec6fea75e59362e61c9c/45.063306,7.660051/?units=si

#NOT USED Library: https://github.com/ZeevG/python-forecast.io