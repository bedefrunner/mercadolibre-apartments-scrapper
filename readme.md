The scrapper reads apartments from MercadoLibre (same as Portal Inmobiliario, because [Mecado Libre acquired them](http://www.economiaynegocios.cl/noticias/noticias.asp?id=118713)) and notifies all new apartments to a Whatsapp number through the Twilio API.

# How to run it
## 1. Clone the repo
```shell
$ git clone https://github.com/bedefrunner/mercadolibre-apartments-scrapper.git
$ cd mercadolibre-apartments-scrapper
```
## 2. Install requirements
```python
$ pip3 install -r requirements.txt
```
## 3. Replace the apartments URL
First, go to [Mercado Libre > apartments](https://www.mercadolibre.cl/c/inmuebles#menu=categories) and add the filters you want to your search. Every filter adds a new param to the URL. When you are comfortable with your filters, copy the URL and add replace the `URL` constant of class `MercadoLibreScrapper` with your URL.

If you want to run this crapper on a daily basis, I recommend to add the filter "publicados hoy", because there's no need to check for every apartment published in the history if you are checking them every day.

## 4. Setup your Twilio API credentias
To notify every new apartment to your Whatsapp number you will need to setup the Twilio API. I don't remember the exact steps, but it's something like this:
1. Create a free Twilio account. No need to pay for any plan.
2. Go to the [Twilio Console](https://console.twilio.com/).
3. Add your Whatsapp number as a Verified Caller ID in Phone Numbers > Manage > Verified Caller IDs. This step is necessary to be able to send a message to your Whatsapp. Documentation [here](https://support.twilio.com/hc/en-us/articles/223180048-How-to-Add-and-Remove-a-Verified-Phone-Number-or-Caller-ID-with-Twilio).
4. Connect to Twilio Whatsapp Sandbox in Messaging > Try it out > Send a Whatsapp message. After this step, you will be connected to Twilio sandbox and you will be able to use the Twilio API to send Whatsapp messages to your phone number.
    <details>
    <summary>Try sending a Whatsapp message using the Twilio API by executing this script 👇.</summary>

      ```python
        # COPY-PASTED FROM THE DOCUMENTATION https://www.twilio.com/docs/whatsapp/api#sending-notifications-with-whatsapp

        # Download the helper library from https://www.twilio.com/docs/python/install
        import os
        from twilio.rest import Client

        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
                                      from_='whatsapp:+14155238886',
                                      body='Hello, there!',
                                      to='whatsapp:+<your-whatsapp-number>'
                                  )

        print(message.sid)
      ```
    </details>
5. Create an .env file and add the following keys with their values:
    ```shell
    TWILIO_ACCOUNT_SID=...
    TWILIO_AUTH_TOKEN=...
    TWILIO_SENDER_WHATSAPP_NUMBER=...
    RECEIVER_WHATSAPP_NUMBER=...
    ```

**Important**: when Twilio doesn't receive any response to the messages it sends you to your Whatsapp, it assumes it spamming you and stops sending them. To avoid this, just reply to the messages (with anything) at least once per day.

## 5. Run it!
```shell
python3 main.py
```

# Not-database
You don't want the scrapper to notify you twice the same apartment, so you need some sort of "database" to keep track of the apartments you have already notify.

This code has no real database connection, but instead uses a .json file called `APARTMENTS_ALREADY_SEEN.json` that acts as a database table. Every time the scrapper finds an apartment, it does the following:
1. Checks if exists in this file
2. If it does, it doesn't notify it, because it assumes it was notified before.
3. If it doesn't, it notifies it and then adds it to this file.

It works just fine.

The only bad thing is that **with every deployment the .json file is overwritten with your local .json file**, deleting all of your records in production. In my case this wasn't a big problem because the URL had the filter of "publicados hoy", so all the apartments that were published before today were not going to be found by the scrapper anyway, and therefore not notified. But if this a real problem with your use case, you should consider connecting to a real DB.

# Recommended deployment in Wayscript
I recommend deploying this code with. It's a tool that allows you to write and deploy code very easily. Just go to https://www.wayscript.com/, create a free account and follow the instructions to start writing and deploying code.

The only bad thing is that they don't have a database add-on, so you can't create a database right there. I guess there are many online tools to create a remote DB and read/write to it via an API. But in my case I just created my super not-database that I explained before and worked fine.

## Schedule a task in Wayscript
It's also very easy to setup an scheduled task (cron job) in Wayscript, only a few clics are needed. You can read the documentation [here](https://docs.wayscript.com/quickstart-schedule-task/python/schedule-a-task).

👁️ Wayscript free trial allows you to make 100 invocations per month. This means you want your cron job to run no more than 3 times per day. If you updgrade to the paid plan, 10,000 invocations are allowed.