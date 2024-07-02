from ReservationInfo import *
from Logger import Logger

import json
import requests
from enum import Enum

class HttpCode(Enum):
    """Http code enum
    """
    SUCCESS = 200
    RESERVATION_NOT_FOUND = 404


class SouthwestApi():
    def __init__(self, debug_level):
        self.url = "https://www.southwest.com/api/air-checkin/v1/air-checkin/page/air/check-in/review"
        self.logger = Logger(debug_level)

    def get_flight_time(self, reservation_number : str) -> int:
        """Gets the flight time for this reservation from southwest website in epoch time
        """
        # Todo
        return 0

    def check_in_flight(self, reservation : ReservationInfo) -> int:
        return self._post_info_to_southwest(reservation.first_name, reservation.last_name, reservation.reservation_number)

    def _post_info_to_southwest(self, first_name, last_name, reservation_number) -> int:
        """ Posts check in to southwest website
        """
        if not isinstance(first_name, str) or not isinstance(last_name, str) or not isinstance (reservation_number, str):
            self.logger._log2("Invalid first/last name or res number")

        form_data = {
            "clk": "HOME-BOOKING-WIDGET-AIR-CHANGE",
            "confirmationNumber": reservation_number,
            "formType": "CHANGE",
            "passengerFirstName": first_name,
            "passengerLastName": last_name,
            "application": "air-check-in",
            "site": "southwest"
        }
        form_data_bin = json.dumps(form_data).encode('utf-8')
        header = {
            "Sec-Fetch-Mode" : "cors",
            "Referer" : "https://www.southwest.com/air/check-in/review.html?confirmationNumber=HSUMAN&formType=CHANGE&passengerFirstName=Andy&passengerLastName=Hsu&clk=HOME-BOOKING-WIDGET-AIR-CHANGE",
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
            "Host" : "www.southwest.com",
            "Origin" : "https://www.southwest.com",
            "Sec-Fetch-Dest" : "empty",
            "Sec-Fetch-Site" : "same-origin",
            "Content-Length" : "192",
            "Connection" : "keep-alive",
            "Accept-Language" : "en-US,en;q=0.9",
            "Accept" : "application/json, text/javascript, */*; q=0.01",
            "Content-Type" : "application/json",
            "Accept-Encoding" : "gzip, deflate, br",
            "EE30zvQLWf-d" : "ADaAhIDBCKGBgQGAAYIQgISigaIAwBGAzPpCxg_33ocx3sD_CABVcXZWQmQeuf_____6FJsyAxTICh-5L7sfcPKeqne5dJg",
            "X-App-ID" : "air-check-in",
            "EE30zvQLWf-c" : "AOCR5m-QAQAAAlKFvkHrgizUkq4ulhFzICkXPmrcCs4NMmu65VVxdlZCZB65",
            "EE30zvQLWf-b" : "-ipjkvq",
            "EE30zvQLWf-a" : "pxoZ=1ERofsBSLXBw-iBAVlFNEUuebLIskZl5L3kVOdiXuEkH83H0Aq2gs5vuY1gA_eMNbbLNMj6vwvvulbxBBOSaFIZLWd7xnJnRcaoPRMORzuZZCg0-SSBobjEB7asJS4k0wjutT81H_Q93DDE4KlFJ04VpmUCaZqUTDqT5P5Zm3auo2Sf=ij5sQzAI3Jf4uPs8lGnWWkgHzbVrJ0C_bluAO3K=BIBhcpLuf6FUjT7qGU7E__ctRAY8lgVHGFGb0np4zKO3-RVRXe1sk_XoUbmDpd0BSHlwIo_Z_FtzteQ0c2OeGwSkChjbsPaxnjzJOnRlGRMa9haTnz8Kf3EgfwcxthiherrRwQY_PJPCvq66oQcQ3wnYcwzU5rq7U1hPLdo-ef-EV7qiRhlc9RbznM3idUj6QEYuPq6cQYRJLhcDNXtDl23KBxoS_Y25X7g-Zs8YKFmviSoe3LKEMrzI=xzZahXsBc=eAHO4vfWFCJlSba7pOCJLFpuedl9puc=ukRbHd6st23zfc5I6-BOjlGfTqSbI=xL7FTzNmQxzAdDY70nMkovEmWYo8_hc-ChuRaHkdTxl1OItHZqkVeYCgKTAt1kQF8hedI=gVTBHd51xws31nd9Hg0TZIar_6CmPf-YBKOL=0zwxkOx_alWo9Wi8K_OWRUz7Qf=ppBwh8z6q6h4PXmworx8XrNZkvsHQov2RHbMp=ttPrghwnW07KfIoMqreaV4_6h3OmSFzt=O=QQoTK42BTgA7G5zFvMn0oDYblNiURWbj5xwMxOT8rq2kzx1MWAlUP85-SkJr6Vzm58x-d1ZISZYjEkUdlsGbPEQqH1humRSg=8V5oLR=aCXihVRw8oFdzdn-h9hDumnT59fhS3P6tS9bcZr7P5MNCudHwJY5oJkmzgYbxLM4ODeeXTnIiRqvEh4Jgtrp0vesVP6aFSfu7Bx6AB5GGfUHGRjgbrdikfAPTr02PS0t4LQpvxG-m5fwWGz9mGro-kmQW-__IevmTfW3cN-1lPhegu82w_tZS5eM-VRAOrQ738p5N6E_4rDsXTSI-Tq0CuRbqXpnmvrkR_eB96nDpxB8v=rL46H4j6YTMl0p-OIC=Bi6H=lNHcZ_3vv3=sQi_s-o_m3HbZbvaoSSvZ7FiISVYxMS5e5g-8Oja07EQlM-mgSwUIAMk3hQjl9T9szCMojNFm_xiIikgu_nogW93iAPgzzc6x2M9T_6TxVnxmFdWW9tvimDC=Vl13d7ngAGqV9d476MXgDMwvgNR_W1o=ulLKAeHloQBaI=5dHQ1-widf6zOoKE=sjvd60_VDeKlEXVcqgRqqAjHhKmggTU7dkCNCqf8J4SHMw8UWI0cNkcSk7BAoL63-qwMgYAr0SAe==WZfWDWBtpdv_1rHnZJid3_0fo6ZuYPkcMNwVrgCQHhIWzVcK2bslAKb3F3rP8Ys=ch_3m0we0sfjJNZ5-aTNFs8-9Iid_5qvTsl2zG-7l=eVqZRZ--_xKEXKHcpZXD2IskdoDZfGjG5v4ZwwGz-Z9Pcaw_IK1gkv3hU82Z6xgm9pno_fWTmsPK2ornNmT2hS=KH68-HXo6Sno7H4vu1bZqo79cShTqGdm5VaL32=skT4KpEOWV=k_Vm-9HBPvopINU0c_tzQBBNAtuW-G6DtNsTVjiANRtUcQ-X15-BRx6XHZmjcXMtTgX0C7UFgeiw9xLbSPukNFf26R72RwWsdpjjxwRcBO24YkESdYwmjbH4IoRTVJCS6aKKGQRUaB1BNZHhXrxLAI6jfMc0AYcRQwbX=17iuo=d3uElZaKaWAe8GIfRhb-ICAWsrWQ671OJ3xnNejJFOgXF48ZNH3AacjLR9R9-C9ikoEbKhdLPbNca3rZ8T-qlvzMK1jwawpJR-1j=",
            "EE30zvQLWf-z" : "q",
            "X-Channel-ID" : "southwest",
            "ADRUM" : "isAjax:true",
            "X-API-Key" : "l7xx944d175ea25f4b9c903a583ea82a1c4c",
            "EE30zvQLWf-f" : "A4MG6W-QAQAArPuQUk9KF5j7l0Mt4hbNMT_JunfcqILGHWh-Lrqv0jUEPPbVAUXmmJD6KwsENeReCOfvosJeCA==",
            "X-User-Experience-ID" : "c8df4ad9-60f4-42e4-861f-0607ce9252bb",
        }

        response = None
        with requests.Session() as session:
            response = session.post(self.url, data=form_data_bin, headers=header)

        if response.ok:
            self.logger._log2('Form submitted successfully')
        else:
            self.logger._log2(f'Error Code: {response.status_code}')
            self.logger._log2(response.text)

        return response.status_code
    def _get_info_from_southwest(self):
        pass
