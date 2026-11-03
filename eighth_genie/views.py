from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
import os
import requests
from dotenv import load_dotenv

load_dotenv()
class IndexView(TemplateView):
   template_name = "index.html"	
def login_view(req):
   client_id = os.getenv("CLIENT_ID")
   redirect_uri = os.getenv("URI")
   ion_auth_url = f"https://ion.tjhsst.edu/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=read+write"
   return redirect(ion_auth_url)
def callback_view(req):
    code = req.GET.get("code")
    token_resp = requests.post("https://ion.tjhsst.edu/oauth/token/", data={
        "grant_type": "authorization_code",
        "code": code,
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("ION_CLIENT_SECRET"),
        "redirect_uri": os.getenv("URI"),
    })
    access_token = token_resp.json().get("access_token")
    if not access_token:
        return HttpResponse("Auth failed", status=400)

    headers = {"Authorization": f"Bearer {access_token}"}
    block = os.getenv("BLOCK")
    activity = os.getenv("ACTIVITY")

    activity_data = requests.get(
        f"https://ion.tjhsst.edu/api/activities/{activity}", headers=headers
    ).json()
    scheduled = activity_data["scheduled_on"][block]["roster"]["id"]

    signup = requests.post(
        "https://ion.tjhsst.edu/api/signups/user",
        json={
            "block": block,
            "activity": activity,
            "scheduled_activity": scheduled,
            "use_scheduled_activity": False,
            "force": False,
        },
        headers=headers,
    )
    print(signup.status_code, signup.text)
    return redirect("/")
