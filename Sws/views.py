from django.shortcuts import render, redirect
import requests, re
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

FASTAPI_URL = "http://127.0.0.1:8001"  # Twój FastAPI backend


# Create your views here.

def home(request):
    return render(request, "home.html")

def teams_from_api(request):
    try:
        response = requests.get(f"{FASTAPI_URL}/teams/")

        print("STATUS:", response.status_code)
        print("TEXT:", response.text)

        response.raise_for_status()
        teams = response.json()

        # 🔤➡️🔢 SORTOWANIE:
        # 1️⃣ Name A–Z
        # 2️⃣ Season ASC
        teams = sorted(
            teams,
            key=lambda t: (
                t.get("Name", "").lower(),
                int(t.get("Season", 0) or 0)
            )
        )

    except Exception as e:
        print("ERROR (Please start P_FastApi) :", e)
        teams = []

    return render(request, "teams_list.html", {"teams": teams})

def trophies_from_api(request):  # start P_FastApi
    try:
        response = requests.get(f"{FASTAPI_URL}/trophies/")

        # Debug: check what API returns
        print("STATUS:", response.status_code)
        print("TEXT:", response.text)

        response.raise_for_status()  # raise error if 400/500

        trophies = response.json()  # convert JSON → Python list

    except Exception as e:
        print("ERROR (Please start P_FastApi) :", e)
        trophies = []  # fallback to empty list

    # render template
    return render(request, "trophies_list.html", {"trophies": trophies})

@csrf_exempt
def create_team(request):
    if request.method == "POST":
        # Pobierz dane z formularza
        Name = request.POST.get("Name", "").strip()
        Description = request.POST.get("Description", "").strip()
        NationalityName = request.POST.get("NationalityName", "").strip()
        Season = request.POST.get("Season", "").strip()
        TopScorer = request.POST.get("TopScorer", "").strip()
        Picture = request.POST.get("Picture", "").strip()
        FinalResult = request.POST.get("FinalResult", "").strip()
        TrophyWin = request.POST.get("TrophyWin", "").strip()
    
        # Prosta walidacja
        if not Name:
            return JsonResponse({"success": False, "errors": {"Name": "Team name cannot be empty"}}, status=400)

        if not TrophyWin:
            TrophyModelId = None
        else:
            # Pobierz TrophyModelId z FastAPI (lub lokalnej bazy, jeśli masz endpoint /trophies)
            try:
                trophy_resp = requests.get(f"{FASTAPI_URL}/trophies/?name={TrophyWin}")
                if trophy_resp.status_code == 200 and trophy_resp.json():
                    TrophyModelId = trophy_resp.json()[0]["Id"]
                else:
                    TrophyModelId = None
            except Exception:
                TrophyModelId = None

        payload = {
            "Name": Name,
            "Description": Description,
            "NationalityName": NationalityName,
            "Season": Season,
            "TopScorer": TopScorer,
            "Picture": Picture,
            "FinalResult": FinalResult,
            "TrophyWin": TrophyWin,
            "TrophyModelId": TrophyModelId
        }

        try:
            response = requests.post(f"{FASTAPI_URL}/teams/", json=payload)
        except Exception as e:
            return JsonResponse({"success": False, "errors": {"server": str(e)}}, status=500)

        if response.status_code in (200, 201):
            return JsonResponse({"success": True})
        else:
            try:
                error_detail = response.json().get("detail", [])
            except Exception:
                error_detail = []

            errors = {}
            if isinstance(error_detail, list):
                for e in error_detail:
                    loc = e.get("loc", [])
                    key = loc[-1] if loc else "field"
                    errors[key] = e.get("msg", str(e))
            else:
                errors["error"] = str(error_detail)

            return JsonResponse({"success": False, "errors": errors}, status=response.status_code)

    return render(request, "team_create.html")

@csrf_exempt
def delete_team(request, team_id):
    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    try:
        response = requests.delete(f"{FASTAPI_URL}/teams/{team_id}")
    except Exception as e:
        return HttpResponse(f"Error connecting to API: {str(e)}", status=500)

    if response.status_code == 200:
        next_url = request.POST.get("next", "/teams/")
        return redirect(next_url)
    else:
        return HttpResponse(
            f"Error deleting teams:<br><br>{response.text}",
            status=response.status_code
        )
    
def team_detail_from_api(request, team_id):
    try:
        response = requests.get(f"{FASTAPI_URL}/teams/{team_id}")

        if response.status_code == 200:
            team = response.json()
            return render(request, "team_detail.html", {
                "team": team,
                "error": None
            })

        elif response.status_code == 404:
            return render(request, "team_detail.html", {
                "team": None,
                "error": f"Team with id {team_id} not found"
            })

        else:
            return render(request, "team_detail.html", {
                "team": None,
                "error": f"Unexpected error: {response.text}"
            })

    except Exception as e:
        return render(request, "team_detail.html", {
            "team": None,
            "error": f"Error connecting to API: {str(e)}"
        })
    
@csrf_exempt
def edit_team(request, team_id):

    # to powinno byc z api
    trophies_list = ["ItalyCup", "ChampionsCup", "UefaCup", "ChampionLeague", "CwcCup", "PolishCup","SpanishCup","Loser"]
    team_names = ["Cesena", "Reggiana", "Udinese", "Gornik", "Siarka", "Perugia", "Stal", "ACMilan", "Juventus", "Betis", "WestHam", "Wolfsburg"]
    nationalities = ["Italy", "Polish"]

    if request.method == "POST":
        Name = request.POST.get("Name", "").strip()
        Description = request.POST.get("Description", "").strip()
        NationalityName = request.POST.get("NationalityName", "").strip()
        Season = request.POST.get("Season", "").strip()
        TopScorer = request.POST.get("TopScorer", "").strip()
        Picture = request.POST.get("Picture", "").strip()
        FinalResult = request.POST.get("FinalResult", "").strip()
        TrophyWin = request.POST.get("TrophyWin", "").strip()

        try:
            Season = int(Season)
        except:
            Season = None

        payload = {
            "Name": Name,
            "Description": Description,
            "NationalityName": NationalityName,
            "Season": Season,
            "TopScorer": TopScorer,
            "Picture": Picture,
            "FinalResult": FinalResult,
            "TrophyWin": TrophyWin
        }

        try:
            response = requests.put(f"{FASTAPI_URL}/teams/{team_id}", json=payload)
            response.raise_for_status()
            return JsonResponse({"success": True})
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except:
                error_detail = str(e)
            return JsonResponse({"success": False, "errors": error_detail}, status=response.status_code)
        except Exception as e:
            return JsonResponse({"success": False, "errors": str(e)}, status=500)

    # GET → pobierz drużynę
    try:
        response = requests.get(f"{FASTAPI_URL}/teams/{team_id}")
        if response.status_code == 200:
            team = response.json()
        else:
            team = {}
    except:
        team = {}

    return render(request, "team_edit.html", {
        "team": team,
        "trophies": trophies_list,
        "team_names": team_names,
        "nationalities": nationalities
    })

# @csrf_exempt
# def trophies_by_season(request, team_id):

#     try:
#         response = requests.get(f"{FASTAPI_URL}/teams/{team_id}/trophies_by_season")
#         response.raise_for_status()
#         data = response.json()
#         return JsonResponse(data, safe=False)
#     except Exception as e:
#         return JsonResponse({"error": f"Cannot fetch trophies: {e}"}, status=500)
    

@csrf_exempt
def trophies_by_season(request, team_id):
    try:
        response = requests.get(f"{FASTAPI_URL}/teams/{team_id}/trophies_by_season")
        response.raise_for_status()
        data = response.json()

        return render(request, "trophies_by_season.html", {
            "team_id": team_id,
            "seasons": data
        })

    except Exception as e:
        return render(request, "trophies_by_season.html", {
            "team_id": team_id,
            "error": f"Cannot fetch trophies: {e}",
            "seasons": []
        })


@csrf_exempt
def create_trophy(request):
    if request.method == "POST":
        # Pobierz dane z formularza
        Name = request.POST.get("Name", "").strip()
        Description = request.POST.get("Description", "").strip()
        Picture = request.POST.get("Picture", "").strip()
        TeamModelId = request.POST.get("TeamModelId", "").strip()

        # Walidacja
        errors = {}
        if not Name:
            errors["Name"] = "Trophy name cannot be empty"
        if not Description:
            errors["Description"] = "Description cannot be empty"
        if errors:
            return JsonResponse({"success": False, "errors": errors}, status=400)

        # Jeśli TeamModelId jest pusty, ustawiamy None
        try:
            TeamModelId = int(TeamModelId) if TeamModelId else None
        except ValueError:
            TeamModelId = None

        payload = {
            "Name": Name,
            "Description": Description,
            "Picture": Picture,
            "TeamModelId": TeamModelId
        }

        # Wywołanie FastAPI
        try:
            response = requests.post(f"{FASTAPI_URL}/trophies/", json=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except:
                error_detail = str(e)
            return JsonResponse({"success": False, "errors": error_detail}, status=response.status_code)
        except Exception as e:
            return JsonResponse({"success": False, "errors": str(e)}, status=500)

        # Sukces
        return JsonResponse({"success": True, "trophy": response.json()})

    # GET → renderowanie formularza
    return render(request, "trophy_create.html")


@csrf_exempt
def delete_trophy(request, trophy_id):
    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    try:
        response = requests.delete(f"{FASTAPI_URL}/trophies/{trophy_id}")
    except Exception as e:
        return HttpResponse(f"Error connecting to API: {str(e)}", status=500)

    if response.status_code == 200:
        # Możesz przekierować do listy trofeów
        next_url = request.POST.get("next", "/trophies/")
        return redirect(next_url)
    else:
        return HttpResponse(
            f"Error deleting trophy:<br><br>{response.text}",
            status=response.status_code
        )


@csrf_exempt
def edit_trophy(request, trophy_id):
    if request.method == "POST":
        # Pobierz dane z formularza
        Name = request.POST.get("Name", "").strip()
        Description = request.POST.get("Description", "").strip()
        Picture = request.POST.get("Picture", "").strip()
        TeamModelId = request.POST.get("TeamModelId", "").strip()

        # Walidacja i konwersja TeamModelId
        try:
            TeamModelId = int(TeamModelId) if TeamModelId else None
        except ValueError:
            TeamModelId = None

        payload = {
            "Name": Name,
            "Description": Description,
            "Picture": Picture,
            "TeamModelId": TeamModelId
        }

        try:
            response = requests.put(f"{FASTAPI_URL}/trophies/{trophy_id}", json=payload)
            response.raise_for_status()
            return JsonResponse({"success": True, "trophy": response.json()})
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except:
                error_detail = str(e)
            return JsonResponse({"success": False, "errors": error_detail}, status=response.status_code)
        except Exception as e:
            return JsonResponse({"success": False, "errors": str(e)}, status=500)

    # GET → pobierz trofeum z FastAPI
    try:
        response = requests.get(f"{FASTAPI_URL}/trophies/")
        response.raise_for_status()
        trophies = response.json()
        trophy = next((t for t in trophies if t["Id"] == trophy_id), None)
    except Exception as e:
        trophy = None

    return render(request, "trophy_edit.html", {
        "trophy": trophy
    })


